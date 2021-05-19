"""
Stream module for retrieving and saving LSL stream data
"""
import logging
from .buffer import Buffer
from threading import current_thread, Thread
from pylsl import local_clock, StreamInlet, proc_threadsafe, proc_ALL, LostError, TimeoutError

# maximum buffer window
BUFFER_WINDOW = 10  # seconds

class Stream:
  """
  Class representing an LSL stream inlet and saving incoming data to a Buffer object
  """
  def __init__(self, uid, stream_info, discard_timestamps=False, correct_timestamps=False):
    """
    :param uid: stream ID
    :param stream_info: stream information
    :param discard_timestamps: whether to discard the original timestamps and use local clock instead
    :param correct_timestamps: determines post-processing flags. refer to pylsl for more info
    """
    self.uid = uid
    self.name = stream_info.name()
    self.sample_rate = stream_info.nominal_srate()
    self.sample_time = 1.0 / stream_info.nominal_srate()
    self.discard_timestamps = discard_timestamps
    self.channel_count = stream_info.channel_count()
    self.info = stream_info
    self.inlet = StreamInlet(stream_info, 360, 20, False, proc_ALL if correct_timestamps else proc_threadsafe)
    self.buffer = Buffer(size=int(stream_info.nominal_srate() * BUFFER_WINDOW))
    self.running = False
    self.thread = None
    self.created_at = local_clock()
    self.updated_at = local_clock()
    self.logger = logging.getLogger(__name__)

  def start(self):
    """
    start the thread
    """
    if self.thread:
      return False

    self.thread = Thread(target=self.pull, daemon=True, name=self.name)
    self.running = True
    self.thread.start()

    return True

  def stop(self):
    """
    stop the thread
    """
    if not self.thread:
      return True

    self.running = False
    if current_thread() is not self.thread:
      self.thread.join()
    self.thread = None

    return True

  def _generate_timestamps(self, num_samples):
    """
    function to generate timestamps based on local clock
    :param num_samples: number of samples
    :return: timestamps
    """
    current_timestamp = local_clock()
    timestamps = [current_timestamp]
    for n in range(num_samples):
      timestamps.insert(0, current_timestamp - self.sample_time * n)

    return timestamps

  def pull(self):
    """
    pull samples from the LSL stream inlet and save to Buffer
    """
    try:
      self.info = self.inlet.info(1.0)

      while self.running:
        try:
          # pull data chunks from the inlet
          samples, original_timestamps = self.inlet.pull_chunk(timeout=0.05)
          num_samples = len(samples)

          if num_samples > 0:
            timestamps = self._generate_timestamps(num_samples) if self.discard_timestamps else original_timestamps  # determining timestamps
            self.logger.debug("{}: Retrieved chunk with {} samples from stream".format(self.name, len(samples)))
            self.updated_at = timestamps[-1]
            self.buffer.extend(zip(timestamps, samples))  # save to buffer
        except TimeoutError:
          self.logger.debug("{}: No data in stream".format(self.name))
    except (LostError, TimeoutError):
      self.logger.warning("{}: Lost stream, disconnecting".format(self.name))
      self.stop()
    except Exception as e:
      self.logger.warning("{}: Error in stream, disconnecting".format(self.name))
      self.logger.exception(e)
      self.stop()
