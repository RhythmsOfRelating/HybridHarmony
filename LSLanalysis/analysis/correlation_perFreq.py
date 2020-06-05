import logging
import json
import numpy as np

from os import getpid
import os
import math
from itertools import islice
from pylsl import local_clock, StreamInfo, StreamOutlet, IRREGULAR_RATE, cf_float32
from scipy.signal import hilbert
from scipy.signal import butter, lfilter

current = os.path.dirname(__file__)
PATH_TOPO = os.path.join(current, 'topo.json')
PATH_SELECT = os.path.join(current, 'select.json')

STREAM_COUNT = None
SAMPLE_RATE = None
CHANNEL_COUNT = None
LAST_CALCULATION = local_clock()

WINDOW = 3  # seconds
COEFFICIENTS = None
CONNECTIONS = None
HANN = None
ORDER = 5
OUTLET = None
OUTLET_POWER = None
BANDS = {
    'delta': (1, 4),
    'theta': (4, 8),
    'alpha': (8, 14),
    'beta':  (14, 20)
}
CHOOSE_CHANNELS = None


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
        
        return False
    
    def _setup(self):
        if not self._changed_since_last_run():
            return
        
        global STREAM_COUNT, SAMPLE_RATE, CHANNEL_COUNT
        global COEFFICIENTS, HANN, CONNECTIONS, OUTLET, OUTLET_POWER, CHOOSE_CHANNELS
        
        self.logger.info("Recalculating correlation constants for changed stream properties")
        STREAM_COUNT = len(self.buffers)
        SAMPLE_RATE = self.sample_rate
        CHANNEL_COUNT = self.channel_count
        COEFFICIENTS = self._setup_coefficients()
        HANN = self._setup_hann()
        CONNECTIONS = self._setup_num_connections()
        OUTLET = self._setup_outlet()
        OUTLET_POWER = self._setup_outlet_power()
        CHOOSE_CHANNELS = self._setup_electrodes()

    def _setup_outlet(self):

        sample_size = CONNECTIONS * len(BANDS)
        
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

    # phoebe edit
    def _setup_outlet_power(self):
        sample_size =  STREAM_COUNT * CHANNEL_COUNT * len(BANDS)
        if sample_size == 0:
            return
        info = StreamInfo('Powervals', 'Markers', sample_size, IRREGULAR_RATE, cf_float32, "Pvals-{}".format(getpid()))
        info.desc().append_child_value('subjects', '_'.join(list(self.buffers.keys())))
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
            # phoebe edit
            envelope_matrix = self._calculate_all(analysis_window)
            rvalues = self._calculate_rvalues(envelope_matrix)
            power_values = self._calculate_power(envelope_matrix)
            
            if OUTLET:
                self.logger.debug("Sending {} R values with timestamp {}".format(len(rvalues), trailing_timestamp))
                OUTLET.push_sample(rvalues, timestamp=trailing_timestamp)
            if OUTLET_POWER:
                # phoebe edit
                OUTLET_POWER.push_sample(power_values, timestamp=trailing_timestamp)

        else:
            self.logger.debug("Still waiting for new data to arrive, skipping analysis")
            return

    def _apply_window_weights(self, analysis_window):
        for uid in analysis_window.keys():
            analysis_window[uid] = np.multiply(analysis_window[uid], HANN[:, None])
        self.logger.debug("Applying window weights with %s samples and % channels." % analysis_window[uid].shape)

    # phoebe edit: using envelop matrix to calculate both rvals and powers (so to avoid calculate hilbert transform twice)
    def _calculate_power(self, envelope_matrix):
        return np.mean(envelope_matrix, axis=3).reshape(-1)
    
    def _calculate_rvalues(self, envelope_matrix):

        rvalues = []
        
        for window_idx in range(len(envelope_matrix) - 1):
            compare_windows = len(envelope_matrix) - window_idx - 1
            compare_window_idx = 1
            while compare_window_idx <= compare_windows:
                # for each frequency, compute corr for all electrodes, and average over selected ones
                for freq, freq_name in enumerate(list(BANDS.keys())):
                    rval_freq = []
                    for electrode in range(CHANNEL_COUNT):
                        r = np.corrcoef([envelope_matrix[window_idx, electrode, freq, :],
                                         envelope_matrix[compare_window_idx, electrode, freq, :]])[0][1]
                        rval_freq.append(r)
                    rval_freq = np.array(rval_freq)
                    rvalues.append(np.mean(rval_freq[CHOOSE_CHANNELS[freq_name]]))
                compare_window_idx += 1

        return rvalues  # n_connections x n_freq

    def _calculate_envelope(self, signal, coeff):  # phoebe edit
        
        signal = lfilter(coeff[0], coeff[1], signal)
        
        analytic_signal = hilbert(signal)
        amplitude_envelope = np.abs(analytic_signal)
        
        return amplitude_envelope
    
    # phoebe edit: calculating for all subjects, the envelope matrix (n_subject x n_channels x n_freq x n_samples)
    def _calculate_all(self, analysis_window):
        all_envelope = np.empty((len(analysis_window), int(self.channel_count), len(COEFFICIENTS), int(self.sample_rate * WINDOW)))  # n_persons x n_channels x n_freq x n_samples
        for i, current_window in enumerate(analysis_window.keys()):
            for channel in range(self.channel_count):
                for c, coeff in enumerate(COEFFICIENTS):
                    envelope = self._calculate_envelope(analysis_window[current_window][:,channel], coeff)
                    all_envelope[i, channel, c, :] = envelope
        return all_envelope
    
    # read json files and choose electrodes for each freq band, saved as a dict
    def _setup_electrodes(self):
        device = None

        if self.channel_count == 32:
            device = 'liveamp32'
        elif self.channel_count == 16:
            device = 'liveamp16'
        elif self.channel_count == 14:
            device = 'epoc+'
        elif self.channel_count == 4:
            device ='muse'
        else:
            self.logger.warning('device type not recognized, channel count is ' + str(self.channel_count) + '\n' +
                                'Using average of all channels.')
        if device:
            with open(PATH_TOPO, 'r') as f:
                topo = json.load(f)[device]
            with open(PATH_SELECT, 'r') as f:
                select = json.load(f)[device]
            choose = {key: [topo[electrode]-1 for electrode in val]
                      for key, val in select.items()}
        else:
            choose = {key:np.arange(0, self.channel_count, 1) for key in BANDS.keys()}  # other device types - use all channels

        return choose



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
