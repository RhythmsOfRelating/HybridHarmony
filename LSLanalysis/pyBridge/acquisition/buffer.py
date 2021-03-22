import logging

from collections import deque
from threading import Condition

class Buffer:
  def __init__(self, size=100):
    self.logger = logging.getLogger(__name__)
    self.condition = Condition()
    self.size = size
    self.samples = deque([], maxlen=size)

  def __len__(self):
    return len(self.samples)

  def __getitem__(self, idx):
       return self.samples[idx]

  def extend(self, samples):
    with self.condition:
      self.samples.extend(samples)
      self.condition.notify()

  def wait(self, timeout=None):
    if timeout == 0.0:
      return

    with self.condition:
      while len(self.samples) == 0:
        self.logger.debug("Waiting for buffer to fill with timeout {}s".format(timeout))

        if not self.condition.wait(timeout=timeout):
          self.logger.debug("Timeout expired after {}s, ignoring empty buffer and returning".format(timeout))
          # When wait returns false the timeout expired, break out of the while loop
          break

  def process(self, timeout=None):
    with self.condition:
      self.wait(timeout)
      processed_samples = list(self.samples)
      self.samples.clear()

    return processed_samples
