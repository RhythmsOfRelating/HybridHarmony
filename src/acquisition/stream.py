"""
Stream module for retrieving and saving LSL stream data
"""
import logging
from .buffer import Buffer
from threading import current_thread, Thread
from pylsl import local_clock, StreamInlet, proc_threadsafe, proc_ALL, LostError, TimeoutError
import traceback
import xml.etree.ElementTree as ET

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
    self.channel_names = None
    self.info = stream_info
    self.inlet = StreamInlet(stream_info, 360, 20, False, proc_ALL if correct_timestamps else proc_threadsafe)
    self.buffer = Buffer(size=int(stream_info.nominal_srate() * BUFFER_WINDOW))
    self.running = False
    self.thread = None
    self.created_at = local_clock()
    self.updated_at = local_clock()
    self.logger = logging.getLogger(__name__)
    # channel names
    try:
      chns_to_add = ['Trig1', 'A1_Box1', 'A2_Box1', 'A3_Box1', 'A4_Box1', 'A5_Box1', 'A6_Box1', 'A7_Box1', 'A8_Box1', 'A9_Box1', 'A10_Box1', 'A11_Box1', 'A12_Box1', 'A13_Box1', 'A14_Box1', 'A15_Box1', 'A16_Box1', 'A17_Box1', 'A18_Box1', 'A19_Box1', 'A20_Box1', 'A21_Box1', 'A22_Box1', 'A23_Box1', 'A24_Box1', 'A25_Box1', 'A26_Box1', 'A27_Box1', 'A28_Box1', 'A29_Box1', 'A30_Box1', 'A31_Box1', 'A32_Box1', 'EX1_Box1', 'EX2_Box1', 'EX3_Box1', 'EX4_Box1', 'EX5_Box1', 'EX6_Box1', 'EX7_Box1', 'EX8_Box1', 'AUX1_Box1', 'AUX2_Box1', 'AUX3_Box1', 'AUX4_Box1', 'AUX5_Box1', 'AUX6_Box1', 'AUX7_Box1', 'AUX8_Box1', 'AUX9_Box1', 'AUX10_Box1', 'AUX11_Box1', 'AUX12_Box1', 'AUX13_Box1', 'AUX14_Box1', 'AUX15_Box1', 'AUX16_Box1', 'A1_Box2', 'A2_Box2', 'A3_Box2', 'A4_Box2', 'A5_Box2', 'A6_Box2', 'A7_Box2', 'A8_Box2', 'A9_Box2', 'A10_Box2', 'A11_Box2', 'A12_Box2', 'A13_Box2', 'A14_Box2', 'A15_Box2', 'A16_Box2', 'A17_Box2', 'A18_Box2', 'A19_Box2', 'A20_Box2', 'A21_Box2', 'A22_Box2', 'A23_Box2', 'A24_Box2', 'A25_Box2', 'A26_Box2', 'A27_Box2', 'A28_Box2', 'A29_Box2', 'A30_Box2', 'A31_Box2', 'A32_Box2', 'EX1_Box2', 'EX2_Box2', 'EX3_Box2', 'EX4_Box2', 'EX5_Box2', 'EX6_Box2', 'EX7_Box2', 'EX8_Box2', 'AUX1_Box2', 'AUX2_Box2', 'AUX3_Box2', 'AUX4_Box2', 'AUX5_Box2', 'AUX6_Box2', 'AUX7_Box2', 'AUX8_Box2', 'AUX9_Box2', 'AUX10_Box2', 'AUX11_Box2', 'AUX12_Box2', 'AUX13_Box2', 'AUX14_Box2', 'AUX15_Box2', 'AUX16_Box2', 'A1_Box3', 'A2_Box3', 'A3_Box3', 'A4_Box3', 'A5_Box3', 'A6_Box3', 'A7_Box3', 'A8_Box3', 'A9_Box3', 'A10_Box3', 'A11_Box3', 'A12_Box3', 'A13_Box3', 'A14_Box3', 'A15_Box3', 'A16_Box3', 'A17_Box3', 'A18_Box3', 'A19_Box3', 'A20_Box3', 'A21_Box3', 'A22_Box3', 'A23_Box3', 'A24_Box3', 'A25_Box3', 'A26_Box3', 'A27_Box3', 'A28_Box3', 'A29_Box3', 'A30_Box3', 'A31_Box3', 'A32_Box3', 'EX1_Box3', 'EX2_Box3', 'EX3_Box3', 'EX4_Box3', 'EX5_Box3', 'EX6_Box3', 'EX7_Box3', 'EX8_Box3', 'AUX1_Box3', 'AUX2_Box3', 'AUX3_Box3', 'AUX4_Box3', 'AUX5_Box3', 'AUX6_Box3', 'AUX7_Box3', 'AUX8_Box3', 'AUX9_Box3', 'AUX10_Box3', 'AUX11_Box3', 'AUX12_Box3', 'AUX13_Box3', 'AUX14_Box3', 'AUX15_Box3', 'AUX16_Box3', 'A1_Box4', 'A2_Box4', 'A3_Box4', 'A4_Box4', 'A5_Box4', 'A6_Box4', 'A7_Box4', 'A8_Box4', 'A9_Box4', 'A10_Box4', 'A11_Box4', 'A12_Box4', 'A13_Box4', 'A14_Box4', 'A15_Box4', 'A16_Box4', 'A17_Box4', 'A18_Box4', 'A19_Box4', 'A20_Box4', 'A21_Box4', 'A22_Box4', 'A23_Box4', 'A24_Box4', 'A25_Box4', 'A26_Box4', 'A27_Box4', 'A28_Box4', 'A29_Box4', 'A30_Box4', 'A31_Box4', 'A32_Box4', 'EX1_Box4', 'EX2_Box4', 'EX3_Box4', 'EX4_Box4', 'EX5_Box4', 'EX6_Box4', 'EX7_Box4', 'EX8_Box4', 'AUX1_Box4', 'AUX2_Box4', 'AUX3_Box4', 'AUX4_Box4', 'AUX5_Box4', 'AUX6_Box4', 'AUX7_Box4', 'AUX8_Box4', 'AUX9_Box4', 'AUX10_Box4', 'AUX11_Box4', 'AUX12_Box4', 'AUX13_Box4', 'AUX14_Box4', 'AUX15_Box4', 'AUX16_Box4']
      self.channel_names = chns_to_add
    except Exception:
      traceback.print_exc()

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
