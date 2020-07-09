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
from astropy.stats import circmean
from itertools import product

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

            analytic_matrix = self._calculate_all(analysis_window)
            rvalues = self._calculate_rvalues(analytic_matrix)
            power_values = self._calculate_power(analytic_matrix)
            
            if OUTLET:
                self.logger.debug("Sending {} R values with timestamp {}".format(len(rvalues), trailing_timestamp))
                OUTLET.push_sample(rvalues, timestamp=trailing_timestamp)
            if OUTLET_POWER:
                OUTLET_POWER.push_sample(power_values, timestamp=trailing_timestamp)

        else:
            self.logger.debug("Still waiting for new data to arrive, skipping analysis")
            return

    def _apply_window_weights(self, analysis_window):
        for uid in analysis_window.keys():
            analysis_window[uid] = np.multiply(analysis_window[uid], HANN[:, None])
        self.logger.debug("Applying window weights with %s samples and % channels." % analysis_window[uid].shape)

    def _calculate_power(self, analytic_matrix):
        return np.nanmean(np.abs(analytic_matrix)**2, axis=3).reshape(-1)
    
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

    def _calculate_analytic(self, signal, coeff):
        signal = lfilter(coeff[0], coeff[1], signal)
        analytic_signal = hilbert(signal)
        return analytic_signal

    def _calculate_all(self, analysis_window):
        all_analytic = np.array(list(analysis_window.values())).reshape((len(analysis_window), self.channel_count, -1))

        all_analytic = np.array([self._calculate_analytic(all_analytic, coeff) for c, coeff in enumerate(COEFFICIENTS)])

        return all_analytic

    # helper function
    def _multiply_conjugate(self, real: np.ndarray, imag: np.ndarray, transpose_axes: tuple) -> np.ndarray:
        """
        Helper function to compute the product of a complex array and its conjugate.
        It is designed specifically to collapse the last dimension of a four-dimensional array.
        Arguments:
            real: the real part of the array.
            imag: the imaginary part of the array.
            transpose_axes: axes to transpose for matrix multiplication.
        Returns:
            product: the product of the array and its complex conjugate.
        """
        formula = 'ilm,imk->ilk'
        product = np.einsum(formula, real, real.transpose(transpose_axes)) + \
                  np.einsum(formula, imag, imag.transpose(transpose_axes)) - 1j * \
                  (np.einsum(formula, real, imag.transpose(transpose_axes)) - \
                   np.einsum(formula, imag, real.transpose(transpose_axes)))

        return product

    def compute_sync(self, complex_signal: np.ndarray, mode: str) -> np.ndarray:

        n_ch, n_freq, n_samp = complex_signal.shape[2], complex_signal.shape[0], \
                               complex_signal.shape[3]

        # calculate all epochs at once, the only downside is that the disk may not have enough space
        complex_signal = complex_signal.reshape(n_freq, 2 * n_ch, n_samp)
        transpose_axes = (0, 2, 1)
        if mode.lower() == 'plv':
            phase = complex_signal / np.abs(complex_signal)
            c = np.real(phase)
            s = np.imag(phase)
            dphi = self._multiply_conjugate(c, s, transpose_axes=transpose_axes)
            con = abs(dphi) / n_samp

        elif mode.lower() == 'envelope_corr':
            env = np.abs(complex_signal)
            mu_env = np.mean(env, axis=2).reshape(n_freq, 2 * n_ch, 1)
            env = env - mu_env
            con = np.einsum('ilm,imk->ilk', env, env.transpose(transpose_axes)) / \
                  np.sqrt(np.einsum('il,ik->ilk', np.sum(env ** 2, axis=2), np.sum(env ** 2, axis=2)))

        elif mode.lower() == 'pow_corr':
            env = np.abs(complex_signal) ** 2
            mu_env = np.mean(env, axis=3).reshape(n_freq, 2 * n_ch, 1)
            env = env - mu_env
            con = np.einsum('ilm,imk->ilk', env, env.transpose(transpose_axes)) / \
                  np.sqrt(np.einsum('il,ik->ilk', np.sum(env ** 2, axis=2), np.sum(env ** 2, axis=2)))

        elif mode.lower() == 'coh':
            c = np.real(complex_signal)
            s = np.imag(complex_signal)
            amp = np.abs(complex_signal) ** 2
            dphi = self._multiply_conjugate(c, s, transpose_axes=transpose_axes)
            con = np.abs(dphi) / np.sqrt(np.einsum('nil,nik->nilk', np.nansum(amp, axis=3),
                                                   np.nansum(amp, axis=3)))

        elif mode.lower() == 'imaginary_coh':
            c = np.real(complex_signal)
            s = np.imag(complex_signal)
            amp = np.abs(complex_signal) ** 2
            dphi = self._multiply_conjugate(c, s, transpose_axes=transpose_axes)
            con = np.abs(np.imag(dphi)) / np.sqrt(np.einsum('il,ik->ilk', np.nansum(amp, axis=2),
                                                            np.nansum(amp, axis=2)))

        elif mode.lower() == 'ccorr':
            angle = np.angle(complex_signal)
            mu_angle = circmean(angle, axis=3).reshape(n_freq, 2 * n_ch, 1)
            angle = np.sin(angle - mu_angle)

            formula = 'ilm,imk->ilk'
            con = np.einsum(formula, angle, angle.transpose(transpose_axes)) / \
                  np.sqrt(np.einsum('il,ik->ilk', np.sum(angle ** 2, axis=2), np.sum(angle ** 2, axis=2)))

        else:
            ValueError('Metric type not supported.')

        return con

    def _calculate_rvalues(self, analytic_matrix, mode):
        pair_index = [a for a in
                      list(product(np.arange(0, analytic_matrix.shape[1]), np.arange(0, analytic_matrix.shape[1])))
                      if a[0] < a[1]]
        rvals = []
        for pair in pair_index:
            con = self.compute_sync(analytic_matrix[:, pair, :, :], mode)
            # the connectivity matrix for the current pair. shape is (n_freq, n_ch, n_ch)
            con = con[:, 0:self.channel_count, self.channel_count:]
            # TODO: average certain channels based on frequency bands. Question: how do we organize channel info?
            rvals.append(np.nanmean(con, axis=(1, 2)))

        return np.array(rvals)  # (n_connections, n_freq)


