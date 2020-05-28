import logging
import numpy as np

from os import getpid
from itertools import islice
from pylsl import local_clock, StreamInfo, StreamOutlet, IRREGULAR_RATE, cf_float32
from scipy.signal import hilbert
from scipy.signal import butter, lfilter

STREAM_COUNT = None
SAMPLE_RATE = None
CHANNEL_COUNT = None
KEY_LIST = []
LAST_CALCULATION = local_clock()

WINDOW = 3 # seconds
COEFFICIENTS = None
CONNECTIONS = None
HANN = None
ORDER = 5
OUTLET = None
BANDS = {
  'delta': (1, 4),
  'theta': (4, 8),
  'alpha': (8, 14),
  'beta':  (14, 20)
}

class Correlation:
  def __init__(self, sample_rate, channel_count, buffers):
    self.logger = logging.getLogger(__name__)
    self.sample_rate = sample_rate
    self.sample_size = int(self.sample_rate * WINDOW)
    self.channel_count = channel_count
    self.buffers = buffers

    self._setup()

  def _changed_since_last_run(self):
    if CHANNEL_COUNT != self.channel_count:
      return True

    if SAMPLE_RATE != self.sample_rate:
      return True

    if STREAM_COUNT != len(self.buffers):
      return True

    if KEY_LIST != list(self.buffers.keys()):
#      self.logger.warning("diff {} {}".format(KEY_LIST, list(self.buffers.keys())))
      return True

    return False

  def _setup(self):
    if not self._changed_since_last_run():
      return

    global STREAM_COUNT, SAMPLE_RATE, CHANNEL_COUNT
    global KEY_LIST
    global COEFFICIENTS, HANN, CONNECTIONS, OUTLET

    self.logger.info("Recalculating correlation constants for changed stream properties")
    STREAM_COUNT = len(self.buffers)
    SAMPLE_RATE = self.sample_rate
    CHANNEL_COUNT = self.channel_count
    KEY_LIST = list(self.buffers.keys())
    COEFFICIENTS = self._setup_coefficients()
    HANN = self._setup_hann()
    CONNECTIONS = self._setup_num_connections()
    OUTLET = self._setup_outlet()

  def _setup_outlet(self):
    sample_size = CONNECTIONS * CHANNEL_COUNT * len(BANDS)
    if sample_size == 0:
      return

    info = StreamInfo('RValues', 'Markers', sample_size, IRREGULAR_RATE, cf_float32, "RValues-{}".format(getpid()))
    info.desc().append_child_value("correlation", "R")

    mappings = info.desc().append_child("mappings")
    buffer_keys = list(self.buffers.keys())
    for buffer_idx in range(len(buffer_keys) - 1):
      compare_buffers = len(buffer_keys) - buffer_idx - 1
      compare_buffer_idx = 1
      while compare_buffer_idx <= compare_buffers:
        mappings.append_child("mapping") \
                .append_child_value("from", buffer_keys[buffer_idx]) \
                .append_child_value("to", buffer_keys[buffer_idx + compare_buffer_idx])

        compare_buffer_idx += 1

    return StreamOutlet(info)

  def _setup_coefficients(self):
    nyq = 0.5 * self.sample_rate
    min_band = 0.0 + 1.0e-10
    max_band = 1.0 - 1.0e-10
    coefficients = []
    for band in BANDS.values():
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
    return sum(list(range(1, len(self.buffers))))

  def run(self):
    global LAST_CALCULATION
    trailing_timestamp = self._find_trailing_timestamp()

    if trailing_timestamp != LAST_CALCULATION:
      LAST_CALCULATION = trailing_timestamp
      analysis_window = self._select_analysis_window(trailing_timestamp)
      self._apply_window_weights(analysis_window)
      rvalues = self._calculate_rvalues(analysis_window)

      if OUTLET:
        self.logger.debug("Sending {} R values with timestamp {}".format(len(rvalues), trailing_timestamp))
        OUTLET.push_sample(rvalues, timestamp=trailing_timestamp)
    else:
      self.logger.debug("Still waiting for new data to arrive, skipping analysis")
      return

  def _apply_window_weights(self, analysis_window):
    for uid in analysis_window.keys():
      for sample in range(self.sample_size):
        for channel in range(self.channel_count):
          analysis_window[uid][sample][channel] *= HANN[sample]

  def _calculate_rvalues(self, analysis_window):
    rvalues = []
    windows = list(analysis_window.keys())

    for channel in range(self.channel_count):
      for window_idx in range(len(windows) - 1):
        compare_windows = len(windows) - window_idx - 1
        compare_window_idx = 1
        while compare_window_idx <= compare_windows:
          r = self._calculate_envelope_correlation([
            np.array(analysis_window[windows[window_idx]][:,channel]),
            np.array(analysis_window[windows[window_idx+compare_window_idx]][:,channel])
          ])

          rvalues.extend(r)
          compare_window_idx += 1

    return rvalues

  def _calculate_envelope_correlation(self, signal):
    rvals = []

    for coeff in COEFFICIENTS:
      signal = lfilter(coeff[0], coeff[1], signal)

      analytic_signal = hilbert(signal)
      amplitude_envelope = np.abs(analytic_signal)

      rvals.append(np.corrcoef(amplitude_envelope)[0][1])

    return rvals

  def _find_trailing_timestamp(self):
    trailing_timestamp = local_clock()

    for buffer in self.buffers.values():
      timestamp, _ = buffer[-1]
      if trailing_timestamp > timestamp:
        trailing_timestamp = timestamp

    return trailing_timestamp

  def _select_analysis_window(self, trailing_timestamp):
    analysis_window = {}

    for uid, buffer in self.buffers.items():
      latest_sample_at, _ = buffer[-1]
      sample_offset = int(round((latest_sample_at - trailing_timestamp) * self.sample_rate))
      sample_start = len(buffer) - self.sample_size - sample_offset

      if sample_start < 0:
        self.logger.info("Not enough data to process in buffer {}, using dummy data".format(uid))
        analysis_window[uid] = np.zeros((self.sample_size, self.channel_count))
      else:
        timestamped_window = list(islice(buffer, sample_start, sample_start + self.sample_size))
        analysis_window[uid] = np.array([sample[1] for sample in timestamped_window])

    return analysis_window
