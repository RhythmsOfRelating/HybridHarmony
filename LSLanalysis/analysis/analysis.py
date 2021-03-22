import logging
from threading import current_thread, Thread
from collections import deque
from .buffer import Buffer
from .correlation_perFreq import Correlation

class Analysis:
  def __init__(self, discovery, mode, chn_type, corr_params, OSC_params, compute_pow, window_params, norm_params):
    self.logger = logging.getLogger(__name__)
    self.discovery = discovery
    self.mode = mode
    self.chn_type = chn_type
    self.corr_params = corr_params
    self.buffer = Buffer(discovery)
    self.OSC_params = OSC_params
    self.compute_pow = compute_pow
    self.window_size, self.window_lag = window_params[0], window_params[1]
    self.norm_params = norm_params
    self.thread = None
    self.running = False
    self.corr = None

  def start(self):
    if self.thread:
      return False

    self.thread = Thread(target=self._update, daemon=True, name="Buffering")
    self.running = True
    self.thread.start()

    # create correlation object
    sample_rate = self.discovery.sample_rate
    channel_count = self.discovery.channel_count
    # Make sure we're still connected and have a sample rate
    if not sample_rate or not channel_count:
      self.logger.warning('connection broken.')
      return

    self.corr = Correlation(
      sample_rate=sample_rate,
      channel_count=channel_count,
      buffers=self.buffer.buffers_by_uid,
      mode=self.mode,
      chn_type=self.chn_type,
      corr_params=self.corr_params,
      OSC_params=self.OSC_params,
      compute_pow=self.compute_pow,
      norm_params=self.norm_params)

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
    self.corr.run()
