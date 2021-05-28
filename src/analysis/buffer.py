"""
Buffer module is used in Analysis module to pull data from the Discovery object
"""
import logging
import time
from collections import deque
from pylsl import local_clock
import numpy as np
from scipy.stats import zscore

BUFFER_WINDOW = 20  # seconds

class Buffer:
  def __init__(self, discovery):
    """
    Class pulling and cleaning data from Discovery object
    :param discovery: Discovery object
    """
    self.logger = logging.getLogger(__name__)
    self.discovery = discovery
    self.buffers_by_uid = {}
    self.trailing_timestamp = local_clock()
    self.trailing_stream = None

  def pull(self):
    """
    Pull data chunks
    """
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
    """
    update the latest timestamp and the last LSL stream
    """
    trailing_timestamp = local_clock()
    trailing_stream = None

    # make sure the current timestamp is no earlier than the latest timestamp of each stream
    for uid, buffer in self.buffers_by_uid.items():
      timestamp, _ = buffer[-1]
      if trailing_timestamp > timestamp:
        trailing_timestamp = timestamp
        trailing_stream = self.discovery.streams_by_uid[uid]

    self.trailing_timestamp = trailing_timestamp
    self.trailing_stream = trailing_stream

  def _process_buffers(self):
    """
    retrieve samples from Discovery and save in a deque object
    """
    for uid, stream in self.discovery.streams_by_uid.items():
      samples = stream.buffer.process(timeout=0.0)
      if len(samples) > 0:
        self.logger.debug("{}: Taking {} samples from buffer".format(stream.name, len(samples)))
        # if uid is new, then create a new deque object
        if uid not in self.buffers_by_uid:
          self.buffers_by_uid[uid] = deque(samples, maxlen=int(stream.info.nominal_srate() * BUFFER_WINDOW))
        else:  # if uid already exists, simply save the samples
          self.buffers_by_uid[uid].extend(samples)

  def _clean_buffers(self):
    """
    remove streams if they are no longer available in Discovery
    """
    for uid in set(self.buffers_by_uid.keys()) - set(self.discovery.streams_by_uid.keys()):
      self.logger.debug("Cleaning stored buffer for device with uid {}".format(uid))
      del self.buffers_by_uid[uid]
