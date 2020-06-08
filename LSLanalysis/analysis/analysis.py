import logging

from threading import current_thread, Thread
from .buffer import Buffer
from .correlation_perFreq import Correlation

class Analysis:
  def __init__(self, discovery):
    self.logger = logging.getLogger(__name__)
    self.discovery = discovery
    self.buffer = Buffer(discovery)
    self.thread = None
    self.running = False

  def start(self):
    if self.thread:
      return False

    self.thread = Thread(target=self._update, daemon=True, name="Buffering")
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

  def _update(self):
    while self.running:
      try:
        self.buffer.pull()
        self._calculate()
      except Exception as e:
        self.logger.warning("Error during analysis, skipped frame")
        self.logger.exception(e)

  def _calculate(self):
    # Make sure we have buffers to analyze
    if len(self.buffer.buffers_by_uid) == 0:
      return

    sample_rate = self.discovery.sample_rate
    channel_count = self.discovery.channel_count

    # Make sure we're still connected and have a sample rate
    if not sample_rate or not channel_count:
      return

    self.logger.info("Performing stream analysis")

    Correlation(
      sample_rate=sample_rate,
      channel_count=channel_count,
      buffers=self.buffer.buffers_by_uid
    ).run()

