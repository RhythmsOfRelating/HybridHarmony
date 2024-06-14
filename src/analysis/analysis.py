"""
Analysis module performing connectivity analysis
"""
import logging
from threading import current_thread, Thread
from os import getpid
from .buffer import Buffer
from .correlation_perFreq import Correlation
from multiprocessing import Queue
from pylsl import local_clock, StreamInfo, StreamOutlet, IRREGULAR_RATE, cf_float32
from scipy.signal import butter
from itertools import product
import numpy as np
from itertools import islice
from scipy.stats import zscore
ORDER = 5
WINDOW = 3

class Analysis:
  def __init__(self, discovery, mode, chn_type, corr_params, OSC_params, compute_pow, window_params, norm_params):
    """
    Class performing connectivity analysis
    :param discovery: Discovery object for retrieving incoming data chunks
    :param mode: connectivity analysis mode. Refer to notes for supported modes
    :param chn_type: compute all electrode pairs if 'all-to-all';
                      alternatively, compute only corresponding electrode pairs if 'one-to-one'
    :param corr_params: a list of three lists: frequency parameters, channel parameters, weight parameters
    :param OSC_params: OSC parameters for OSC transmission
    :param compute_pow: boolean variable determining whether to compute and transmit power values
    :param window_params: (deprecated) analysis window size
    :param norm_params: a list of two. min and max values for MinMax normalization

    Note:
      **supported connectivity measures**
          - 'envelope correlation': envelope correlation
          - 'power correlation': power correlation
          - 'plv': phase locking value
          - 'ccorr': circular correlation coefficient
          - 'coherence': coherence
          - 'imaginary coherence': imaginary coherence
    """
    # setting up parameters
    self.logger = logging.getLogger(__name__)
    self.discovery = discovery
    self.mode = mode
    self.chn_type = chn_type
    self.corr_params = corr_params
    self.freqParams = corr_params[0]
    self.buffer = Buffer(discovery)
    self.OSC_params = OSC_params
    self.compute_pow = compute_pow
    self.window_size = window_params
    self.norm_params = norm_params
    self.thread = None
    self.running = False
    self.corr = None
    self.que = Queue(maxsize=1000)
    #self.sr = self.discover.sample_rate
    self.buffer.pull()  # pull data (once) in order to set up the following information
    self.sample_rate = self.discovery.sample_rate
    self.channel_count = self.discovery.channel_count
    self.window_length = int(self.sample_rate * self.window_size)  # number of samples in the analysis window
    self.STREAM_COUNT = len(self.buffer.buffers_by_uid)  # number of streams
    self.COEFFICIENTS = self._setup_coefficients()  # band-pass filtering coefficients
    self.HANN = self._setup_hann()  # Hanning window coefficients
    self.CONNECTIONS = self._setup_num_connections()  # number of connections
    self.OUTLET = self._setup_outlet()  # connectivity value outlet
    self.OUTLET_TRIGGER = self._setup_outlet_trigger()  # trigger outlet
    if self.compute_pow:  # if sending power values, then set up power value outlet
      self.OUTLET_POWER = self._setup_outlet_power()
    else:
      self.OUTLET_POWER = None

    # create the correlation object with all parameters (besides the incoming data)
    self.corr = Correlation(
      sample_rate=self.sample_rate,
      channel_count=self.channel_count,
      mode=self.mode,
      chn_type=self.chn_type,
      corr_params=self.corr_params,
      OSC_params=self.OSC_params,
      compute_pow=self.compute_pow,
      norm_params=self.norm_params,
      window_length=self.window_length,
      COEFFICIENTS=self.COEFFICIENTS,
      HANN=self.HANN,
      CONNECTIONS=self.CONNECTIONS,
      OUTLET=self.OUTLET, OUTLET_POWER=self.OUTLET_POWER,
      OUTLET_TRIGGER=self.OUTLET_TRIGGER)

  def start(self):
    """
    Start thread for analysis, while saving the output of self._update to the que parameter
    """
    if self.thread:
      return False
    self.thread = Thread(
      target=self._update,
      name="analysis",
      args=[self.que],
      daemon=True  # does this solve thread quiting issue?
    )
    self.running = True
    self.thread.start()

    return True

  def stop(self):
    """
    Stop the analysis
    """
    if not self.thread:
      return True

    self.running = False
    if current_thread() is not self.thread:
      self.thread.join()
    self.thread = None

    return True

  def trigger(self, id):
    self.corr.send_trigger(id)

  def _update(self, que):
    """
    Continuously pull data samples and perform connectivity analysis, and then save the result to que
    :param que: Queue object to save connectivity values
    """
    while self.running:
      try:
        self.buffer.pull()
        # self.logger.warning(str(list(self.buffer.buffers_by_uid.keys())))
        # samples0 = list(islice(self.buffer.buffers_by_uid[list(self.buffer.buffers_by_uid.keys())[0]],0,10))
        # samples1 = list(islice(self.buffer.buffers_by_uid[list(self.buffer.buffers_by_uid.keys())[1]], 0, 10))
        # self.logger.warning(samples0)
        # self.logger.warning(samples1)
        r = self._calculate()
        if r:
          que.put(["{:.4f}".format(a_float) for a_float in r])
      except Exception as e:
        self.logger.warning("Error during analysis, skipped frame "+str(e))
        self.logger.exception(e)

  def _calculate(self):
    """
    compute connectivity values by calling the Correlation object
    """
    # Make sure we have buffers to analyze
    if len(self.buffer.buffers_by_uid) == 0:
      return
    self.sample_rate = self.discovery.sample_rate
    self.channel_count = self.discovery.channel_count
    # Make sure we're still connected and have a sample rate
    if not self.sample_rate or not self.channel_count:
      self.logger.warning('connection broken.')
      return
    # running correlation with incoming data
    r = self.corr.run(self.buffer.buffers_by_uid)
    return r

  # helper functions to set up
  def _setup_outlet(self):
    """
    Setting up LSL outlet for connectivity values
    :return: StreamOutlet object
    """
    sample_size = self.CONNECTIONS * len(self.freqParams)
    if sample_size == 0:
      return

    # basic info
    info = StreamInfo('RValues', 'Markers', sample_size, IRREGULAR_RATE, cf_float32, "RValues-{}".format(getpid()))
    info.desc().append_child_value("correlation", "R")
    mappings = info.desc().append_child("mappings")
    # in the 'mapping' field, save the IDs of the pair in each connection
    buffer_keys = list(self.buffer.buffers_by_uid.keys())
    pair_index = [a for a in
                  list(product(np.arange(0, len(buffer_keys)), np.arange(0, len(buffer_keys))))
                  if a[0] < a[1]]
    for pair in pair_index:
      mappings.append_child("mapping") \
        .append_child_value("from", buffer_keys[pair[0]]) \
        .append_child_value("to", buffer_keys[pair[1]])

    return StreamOutlet(info)

  def _setup_outlet_trigger(self):
    """
    Setting up LSL outlet for triggers
    :return: StreamOutlet object
    """
    info = StreamInfo(name='TriggerStream', type='Markers', channel_count=1, channel_format='int32',
                      source_id= "Triggers-{}".format(getpid()))
    return StreamOutlet(info)

  def _setup_outlet_power(self):
    """
    Setting up LSL outlet for power values
    :return: StreamOutlet object
    """
    sample_size = self.STREAM_COUNT * self.channel_count * len(self.freqParams)
    self.logger.warning('power sample size is %s %s %s' % (self.STREAM_COUNT, self.channel_count, len(self.freqParams)))
    if sample_size == 0:
      return
    info = StreamInfo('Powervals', 'Markers', sample_size, IRREGULAR_RATE, cf_float32, "Pvals-{}".format(getpid()))
    info.desc().append_child_value('subjects', '_'.join(list(self.buffer.buffers_by_uid.keys())))  # the list of subjects' IDs
    return StreamOutlet(info)

  def _setup_coefficients(self):
    """
    set up band-pass filtering coefficients
    :return: a list of butterworth filter parameters
    """
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
    """
    set up Hanning window
    :return: Hanning coefficients
    """
    denom = self.window_length - 1
    hann = []
    for n in range(self.window_length):
      hann.append(.5 * (1 - np.cos((2 * np.pi * n) / denom)))

    return np.array(hann)

  def _setup_num_connections(self):
    """
    calculate the number of connections given the number of streams (subjects)
    :return: number of connections
    """
    return sum(list(range(1, len(self.buffer.buffers_by_uid))))
