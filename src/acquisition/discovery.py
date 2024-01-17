"""
Discovery Module for LSL stream discovery and data retrieval
"""
import logging
from threading import current_thread, Thread
from pylsl import resolve_bypred, LostError, TimeoutError, resolve_streams
from .stream import Stream

class Discovery:
  """
  Class representing the available LSL stream information and incoming data
  """
  def __init__(self, **options):
    """
    :param options: additional arguments for creating Stream object
    """
    self.logger = logging.getLogger(__name__)
    self.options = options
    self.sample_rate = None
    self.channel_count = None
    self.channel_names = None
    self.streams_by_uid = {}
    self.running = False
    self.thread = None

  def start(self):
    """
    Start the thread to resolve LSL streams
    """
    if self.thread:
      return False

    self.thread = Thread(target=self._refresh, daemon=True, name="Discovery")
    self.running = True
    self.thread.start()

    return True

  def stop(self):
    """
    Stop LSL stream search
    """
    if not self.thread:
      return True

    self.running = False
    if current_thread() is not self.thread:
      self.thread.join()
    self.thread = None

    return True

  def streams(self):
    """
    :return: a list of Stream objects
    """
    return list(self.streams_by_uid.values())

  def _refresh(self):
    while self.running:
      self._resolve()

  def _resolve(self):
    """
    Search for available EEG streams on LSL and connect to them by saving them as Stream objects
    """
    # resolve EEG streams and retrieve their information
    streams_info = resolve_bypred("type='EEG'", 0, 2.5)
    streams_active = []
    self.logger.debug("Found {} available streams".format(len(streams_info)))

    # iterate for each stream
    for stream_info in streams_info:
      # uid = stream_info.source_id() if stream_info.source_id() else stream_info.uid()  # retrieve 'source_id'
      uid = stream_info.source_id() + ' | ' + stream_info.uid()
      streams_active.append(uid)

      # if the current stream has not been saved, then connect to the current stream
      if uid not in self.streams_by_uid:
        if self._validate_stream_signature(stream_info):
          self._connect_to(uid, stream_info)

      # if the current stream is already saved, but is not running, then disconnect
      if uid in self.streams_by_uid:
        if self.streams_by_uid[uid].running == False:
          self._disconnect_from({uid})

    self._disconnect_from(list(set(self.streams_by_uid.keys()) - set(streams_active)))

  def _validate_stream_signature(self, stream_info):
    """
    checking if the input stream's sampling rate and channel count match those of the previous stream
    :param stream_info: current stream information
    """
    if self.sample_rate and self.sample_rate != stream_info.nominal_srate():
      return False
    if self.channel_count and self.channel_count != stream_info.channel_count():
      return False
    return True

  def _connect_to(self, uid, stream_info):
    """
    Connect to the stream using the stream information
    :param uid: the stream ID, i.e., 'source_id'
    :param stream_info: stream information
    """
    stream = None
    try:
      self.logger.info("{}: Discovered at {}hz with {} channels, connecting".format(stream_info.name(), stream_info.nominal_srate(), stream_info.channel_count()))
      # create the Stream object using retrieved stream information
      stream = Stream(uid, stream_info, **self.options)
      stream.start()  # start the Stream thread
      self.logger.warning("{}: Connected".format(stream_info.name()))
    except (LostError, TimeoutError):
      self.logger.warning("{}: Could not connect".format(stream_info.name()))

    if stream:
      if len(self.streams_by_uid) == 0:
        self.sample_rate = stream.sample_rate
        self.channel_count = stream.channel_count
        self.channel_names = stream.channel_names
        self.logger.info("{}: Elected master stream at {}hz with {} channels".format(stream.name, stream.sample_rate, stream.channel_count))

      self.streams_by_uid[uid] = stream

  def _disconnect_from(self, inactive_uids):
    """
    Disconnect from streams using their IDs
    :param inactive_uids: inactive streams' IDs
    """
    for uid in inactive_uids:
      if self.streams_by_uid[uid].running:
        self.logger.info("{}: Disconnected, killing thread".format(self.streams_by_uid[uid].name))
        self.streams_by_uid[uid].stop()
      else:
        self.logger.info("{}: Killed, cleaning up".format(self.streams_by_uid[uid].name))
        del self.streams_by_uid[uid]

    if len(self.streams_by_uid) == 0:
      self.sample_rate = None
      self.channel_count = None
