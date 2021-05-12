import logging
from threading import current_thread, Thread
from collections import deque
from os import getpid
from .buffer import Buffer
from .correlation_perFreq import Correlation
from multiprocessing import Queue
from pylsl import local_clock, StreamInfo, StreamOutlet, IRREGULAR_RATE, cf_float32
from scipy.signal import butter
from itertools import product
from osc4py3.as_allthreads import *
from osc4py3 import oscbuildparse
from osc4py3 import oscchannel as osch
import numpy as np
ORDER = 5
WINDOW = 3

class Analysis:
  def __init__(self, discovery, mode, chn_type, corr_params, OSC_params, compute_pow, window_params, norm_params):
    self.logger = logging.getLogger(__name__)
    self.discovery = discovery
    self.mode = mode
    self.chn_type = chn_type
    self.corr_params = corr_params
    self.freqParams = corr_params[0]
    self.buffer = Buffer(discovery)
    self.OSC_params = OSC_params
    self.compute_pow = compute_pow
    self.window_size, self.window_lag = window_params[0], window_params[1]
    self.norm_params = norm_params
    self.thread = None
    self.running = False
    self.corr = None
    self.que = Queue(maxsize=1000)

    self.buffer.pull()  # initial pull in order to setup connections
    self.sample_rate = self.discovery.sample_rate
    self.channel_count = self.discovery.channel_count
    self.sample_size = int(self.sample_rate * WINDOW)
    self.STREAM_COUNT = len(self.buffer.buffers_by_uid)
    self.COEFFICIENTS = self._setup_coefficients()
    self.HANN = self._setup_hann()
    self.CONNECTIONS = self._setup_num_connections()
    self.OUTLET = self._setup_outlet()
    if self.compute_pow:
      self.OUTLET_POWER = self._setup_outlet_power()
    else:
      self.OUTLET_POWER = None

  def start(self):
    if self.thread:
      return False
    self.thread = Thread(
      target=self._update,
      name="analysis",
      args=[self.que],
    )
    # self.thread = Thread(target=lambda q, args1: q.put(self._update()),
    #                      args=(self.que, None), daemon=True, name="Buffering")
    # self.thread = Thread(target=self._update, daemon=True, name="Buffering")
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

  def _update(self, que):
    while self.running:
      try:
        self.buffer.pull()
        r = self._calculate()
        if r:
          que.put(r)
      except Exception as e:
        self.logger.warning("Error during analysis, skipped frame "+str(e))
        self.logger.exception(e)


  def _calculate(self):
    # Make sure we have buffers to analyze
    if len(self.buffer.buffers_by_uid) == 0:
      return
    # create correlation object
    self.sample_rate = self.discovery.sample_rate
    self.channel_count = self.discovery.channel_count
    # Make sure we're still connected and have a sample rate
    if not self.sample_rate or not self.channel_count:
      self.logger.warning('connection broken.')
      return
    self.corr = Correlation(
      sample_rate=self.sample_rate,
      channel_count=self.channel_count,
      buffers=self.buffer.buffers_by_uid,
      mode=self.mode,
      chn_type=self.chn_type,
      corr_params=self.corr_params,
      OSC_params=self.OSC_params,
      compute_pow=self.compute_pow,
      norm_params=self.norm_params,
      COEFFICIENTS=self.COEFFICIENTS,
      HANN=self.HANN,
      CONNECTIONS=self.CONNECTIONS,
      OUTLET=self.OUTLET, OUTLET_POWER=self.OUTLET_POWER)
    r = self.corr.run()
    return r

  # helper functions to set up

  def _setup_outlet(self):
    sample_size = self.CONNECTIONS * len(self.freqParams)
    if sample_size == 0:
      return

    info = StreamInfo('RValues', 'Markers', sample_size, IRREGULAR_RATE, cf_float32, "RValues-{}".format(getpid()))
    info.desc().append_child_value("correlation", "R")

    mappings = info.desc().append_child("mappings")
    buffer_keys = list(self.buffer.buffers_by_uid.keys())
    pair_index = [a for a in
                  list(product(np.arange(0, len(buffer_keys)), np.arange(0, len(buffer_keys))))
                  if a[0] < a[1]]

    for pair in pair_index:
      mappings.append_child("mapping") \
        .append_child_value("from", buffer_keys[pair[0]]) \
        .append_child_value("to", buffer_keys[pair[1]])

    return StreamOutlet(info)

  # phoebe edit
  def _setup_outlet_power(self):
    sample_size = self.STREAM_COUNT * self.channel_count * len(self.freqParams)
    self.logger.warning('power sample size is %s %s %s' % (self.STREAM_COUNT, self.channel_count, len(self.freqParams)))
    if sample_size == 0:
      return
    info = StreamInfo('Powervals', 'Markers', sample_size, IRREGULAR_RATE, cf_float32, "Pvals-{}".format(getpid()))
    info.desc().append_child_value('subjects', '_'.join(list(self.buffer.buffers_by_uid.keys())))
    return StreamOutlet(info)

  def _setup_coefficients(self):
    nyq = 0.5 * self.sample_rate
    min_band = 0.0 + 1.0e-10
    max_band = 1.0 - 1.0e-10
    coefficients = []
    for band in self.freqParams.values():
      low_band = max(min_band, min(max_band, band[0] / nyq))
      high_band = max(min_band, min(max_band, band[1] / nyq))
      low, high = butter(ORDER, [low_band, high_band], btype='band')
      coefficients.append([low, high])

    return coefficients

  def _setup_hann(self):
    denom = self.sample_size - 1
    hann = []
    for n in range(self.sample_size):
      hann.append(.5 * (1 - np.cos((2 * np.pi * n) / denom)))

    return np.array(hann)

  def _setup_num_connections(self):
    return sum(list(range(1, len(self.buffer.buffers_by_uid))))
