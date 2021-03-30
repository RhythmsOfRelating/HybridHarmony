import logging
from queue import Queue
from threading import current_thread, Thread
from collections import deque
from .buffer import Buffer
from .normalization import Normalization

class Analysis:
  def __init__(self, discovery, mode, OSC_params, weight, manual_params, auto_params):
    self.logger = logging.getLogger(__name__)
    self.thread = None
    self.running = False
    self.norm = None

    self.discovery = discovery
    self.mode = mode
    self.buffer = Buffer(discovery)
    self.OSC_params = OSC_params
    self.weight = weight
    self.manual_params = manual_params
    self.auto_params = auto_params

    self.mess = None

  def start(self):
    if self.thread:
      return False
    # start the thread
    # TODO
    # self.que = Queue()
    # self.thread = Thread(target=lambda self.que, arg1: self.que.put(self._update(arg1)), args=(self.que), daemon=True,name='Norm')
    self.thread = Thread(target=self._update, daemon=True, name="Norm")
    self.running = True
    self.thread.start()

    # create normalization object
    sample_rate = self.discovery.sample_rate
    channel_count = self.discovery.channel_count
    # Make sure we're still connected and have a sample rate
    if not sample_rate or not channel_count:
      self.logger.warning('connection broken.')
      return

    self.norm = Normalization(
      buffers=self.buffer.buffers_by_uid,
      mode=self.mode,
      OSC_params=self.OSC_params,
      weight=self.weight,
      manual_params=self.manual_params,
      auto_params=self.auto_params)

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
        # if len(self.buffer.buffers_by_uid) == 0:
        #   return
        self.norm.run()
      except Exception as e:
        self.logger.warning("Error during analysis, skipped frame")
        self.logger.exception(e)
