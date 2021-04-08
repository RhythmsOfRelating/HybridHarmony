import logging

from threading import current_thread, Thread
from pylsl import resolve_bypred, LostError, TimeoutError

from .stream import Stream

class Discovery:
  def __init__(self, **options):
    self.logger = logging.getLogger(__name__)
    self.options = options
    self.sample_rate = None
    self.channel_count = None
    self.streams_by_uid = {}
    self.running = False
    self.thread = None

  def start(self):
    if self.thread:
      return False

    self.thread = Thread(target=self._refresh, daemon=True, name="normDiscovery")
    self.running = True
    self.thread.start()

    return True

  def stop(self):
    if not self.thread:
      return True

    self.running = False
    if current_thread() is not self.thread:
      self.thread.join()
    self.thread = None

    return True

  def streams(self):
    return list(self.streams_by_uid.values())

  def _refresh(self):
    while self.running:
      self._resolve()

  def _resolve(self):
    streams_info = resolve_bypred("name='RValues'", 0, 2.5)
    streams_active = []

    self.logger.debug("Found {} available streams".format(len(streams_info)))

    for stream_info in streams_info:
      uid = stream_info.source_id() if stream_info.source_id() else stream_info.uid()
      streams_active.append(uid)

      if uid not in self.streams_by_uid:
        if self._validate_stream_signature(stream_info):
          self._connect_to(uid, stream_info)

      if uid in self.streams_by_uid:
        if self.streams_by_uid[uid].running == False:
          self._disconnect_from({uid})

    self._disconnect_from(list(set(self.streams_by_uid.keys()) - set(streams_active)))

  def _validate_stream_signature(self, stream_info):
    if self.sample_rate and self.sample_rate != stream_info.nominal_srate():
      return False

    if self.channel_count and self.channel_count != stream_info.channel_count():
      return False

    return True

  def _connect_to(self, uid, stream_info):
    stream = None
    try:
      self.logger.info("{}: Discovered {} rvalues, connecting".format(stream_info.name(), stream_info.channel_count()))
      stream = Stream(uid, stream_info, **self.options)
      stream.start()
      self.logger.warning("{}: Connected".format(stream_info.name()))
    except (LostError, TimeoutError):
      self.logger.warning("{}: Could not connect".format(stream_info.name()))

    if stream:
      if len(self.streams_by_uid) == 0:
        self.sample_rate = stream.sample_rate
        self.channel_count = stream.channel_count
        self.logger.info("{}: Elected master stream at {}hz with {} channels".format(stream.name, stream.sample_rate, stream.channel_count))

      self.streams_by_uid[uid] = stream

  def _disconnect_from(self, inactive_uids):
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
