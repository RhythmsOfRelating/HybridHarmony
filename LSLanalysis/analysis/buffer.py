import logging
import time

from collections import deque
from pylsl import local_clock

BUFFER_WINDOW = 30 # seconds

class Buffer:
  def __init__(self, discovery):
    self.logger = logging.getLogger(__name__)
    self.discovery = discovery
    self.buffers_by_uid = {}
    self.trailing_timestamp = local_clock()
    self.trailing_stream = None

  def pull(self):
    self._clean_buffers()
    self._process_buffers()
    self._update_trailing_stream()

    if self.trailing_stream:
      self.logger.debug("{}: Waiting for trailing stream to receive samples since {}".format(self.trailing_stream.name, self.trailing_timestamp))
      self.trailing_stream.buffer.wait(1.0 / self.discovery.sample_rate)
    else:
      self.logger.debug("No streams available, waiting to continue")
      time.sleep(0.1)

  def _update_trailing_stream(self):
    trailing_timestamp = local_clock()
    trailing_stream = None

    for uid, buffer in self.buffers_by_uid.items():
      timestamp, _ = buffer[-1]
      if trailing_timestamp > timestamp:
        trailing_timestamp = timestamp
        trailing_stream = self.discovery.streams_by_uid[uid]

    self.trailing_timestamp = trailing_timestamp
    self.trailing_stream = trailing_stream

  def _process_buffers(self):
    for uid, stream in self.discovery.streams_by_uid.items():
      samples = stream.buffer.process(timeout=0.0)

      if len(samples) > 0:
        self.logger.debug("{}: Taking {} samples from buffer".format(stream.name, len(samples)))

        if uid not in self.buffers_by_uid:
          self.buffers_by_uid[uid] = deque(samples, maxlen=int(stream.info.nominal_srate() * BUFFER_WINDOW))
        else:
          self.buffers_by_uid[uid].extend(samples)

  def _clean_buffers(self):
    for uid in set(self.buffers_by_uid.keys()) - set(self.discovery.streams_by_uid.keys()):
      self.logger.debug("Cleaning stored buffer for device with uid {}".format(uid))
      del self.buffers_by_uid[uid]
