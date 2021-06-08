"""
Correlation module calculating connectivity values from data
"""
import logging
import numpy as np
import os
from itertools import islice
from pylsl import local_clock
from scipy.signal import hilbert
from scipy.signal import lfilter
from scipy.stats import zscore
from astropy.stats import circmean
from itertools import product
from osc4py3.as_allthreads import *
from osc4py3 import oscbuildparse
from osc4py3 import oscchannel as osch
import warnings
warnings.filterwarnings("ignore")
current = os.path.dirname(__file__)

LAST_CALCULATION = local_clock()
ORDER = 5

class Correlation:
    def __init__(self, sample_rate, channel_count, mode, chn_type, corr_params, OSC_params, compute_pow, norm_params,
                 window_length, COEFFICIENTS, HANN, CONNECTIONS, OUTLET, OUTLET_POWER):
        """
        Class computing connectivity values

        :param sample_rate: sampling rate
        :param channel_count: channel count
        :param mode: connectivity mode. See notes for options.
        :param chn_type: compute all electrode pairs if 'all-to-all';
                         alternatively, compute only corresponding electrode pairs if 'one-to-one'
        :param corr_params: a list of three lists: frequency parameters, channel parameters, weight parameters
        :param OSC_params: OSC parameters for OSC transmission
        :param compute_pow: boolean variable determining whether to compute and transmit power values
        :param norm_params: a list of two numbers. min and max values for MinMax normalization
        :param COEFFICIENTS: band-pass filtering coefficients
        :param HANN: Hanning window coefficients
        :param CONNECTIONS: number of connections
        :param OUTLET: StreamOutlet object for connectivity value output
        :param OUTLET_POWER: StreamOutlet object for power value output

        Note:
        **supported connectivity measures**
          - 'envelope correlation': envelope correlation
          - 'power correlation': power correlation
          - 'plv': phase locking value
          - 'ccorr': circular correlation coefficient
          - 'coherence': coherence
          - 'imaginary coherence': imaginary coherence
        """
        self.logger = logging.getLogger(__name__)
        self.sample_rate = sample_rate
        self.window_length = window_length  # number of samples in the analysis window
        self.channel_count = channel_count
        self.freqParams, self.chnParams, self.weightParams = corr_params
        self.OSC_params = OSC_params
        self.compute_pow = compute_pow
        self.norm_min, self.norm_max = norm_params
        self.mode = mode
        self.chn_type = chn_type
        self.timestamp = None
        self.SAMPLE_RATE = self.sample_rate
        self.CHANNEL_COUNT = self.channel_count
        # read setup tools
        self.COEFFICIENTS = COEFFICIENTS
        self.HANN = HANN
        self.CONNECTIONS = CONNECTIONS
        self.OUTLET = OUTLET
        if self.compute_pow:
            self.OUTLET_POWER = OUTLET_POWER
        if OSC_params[0] is not None:
            self._setup_OSC()

    def run(self, buffers):
        """
        running the analysis
        :return: connectivity values
        """
        global LAST_CALCULATION
        trailing_timestamp = self._find_trailing_timestamp(buffers)

        if trailing_timestamp != LAST_CALCULATION:
            LAST_CALCULATION = trailing_timestamp
            # select data for analysis based on the last timestamp
            analysis_window = self._select_analysis_window(trailing_timestamp, buffers)
            # apply Hanning window
            # analysis_window = self._apply_window_weights(analysis_window)
            # band-pass filter and compute analytic signal
            analytic_matrix = self._calculate_all(analysis_window)
            # compute connectivity values
            rvalues = self._calculate_rvalues(analytic_matrix, self.mode)
            if self.compute_pow:
                power_values = self._calculate_power(analytic_matrix)
                self.OUTLET_POWER.push_sample(power_values, timestamp=trailing_timestamp)

            # sending LSL packets
            if self.OUTLET:
                self.logger.warning("Sending {} R values with timestamp {}".format(len(rvalues), trailing_timestamp))
                self.OUTLET.push_sample(rvalues, timestamp=trailing_timestamp)
            # sending OSC packets
            if self.OSC_params[0] is not None:  # if sending OSC
                sample_size = self.CONNECTIONS * len(self.freqParams)
                msg = oscbuildparse.OSCMessage("/Rvalues/me", ","+'f'*sample_size, rvalues)
                osc_send(msg, 'Rvalues')
                osc_process()
            return rvalues
        else:
            self.logger.debug("Still waiting for new data to arrive, skipping analysis")
            return

    def _clamp(self, n):
        """
        helper function to clamp a float variable between 0 and 1
        """
        return max(min(1, n), 0)

    def _apply_window_weights(self, analysis_window):
        """
        applying hanning window to data
        :param analysis_window: dictionary with EEG data streams
        :return: dictionary of the same shape after applying hanning window
        """
        for uid in analysis_window.keys():
            analysis_window[uid] = np.multiply(analysis_window[uid], self.HANN[:, None])
        self.logger.debug("Applying window weights with %s samples and %s channels." % analysis_window[uid].shape)
        return analysis_window

    def _setup_OSC(self):
        """
        setting up OSC outlet
        """
        # reading params
        IP = self.OSC_params[0]
        port = int(self.OSC_params[1])
        # Start the system.
        osc_startup()
        # Make client channels to send packets.
        try:
            osc_udp_client(IP, int(port), "Rvalues")
        except:
            osch.terminate_all_channels()
            osc_udp_client(IP, int(port), "Rvalues")
        # first message is empty (removed this bc it's causing OSC msg to be all zeros)
        # msg = oscbuildparse.OSCMessage("/Rvalues/me", ","+'f'*sample_size, [0]*sample_size)
        # osc_send(msg, 'Rvalues')

    def _calculate_power(self, analytic_matrix):
        """
        compute power values from analytic signals
        :param analytic_matrix: shape is (n_freq_bands, n_subjects, n_channel_count, n_sample_size). filtered analytic signal
        :return: a vector that can be reshaped into (n_freq_bands, n_subjects, n_channel_count). Power values
        """
        return np.nanmean(np.abs(analytic_matrix)**2, axis=3).reshape(-1)

    def _find_trailing_timestamp(self, buffers):
        trailing_timestamp = local_clock()

        for buffer in buffers.values():#self.buffers.values():
            timestamp, _ = buffer[-1]
            if trailing_timestamp > timestamp:
                trailing_timestamp = timestamp
        
        return trailing_timestamp

    def _select_analysis_window(self, trailing_timestamp, buffers):
        """
        construct the analysis window based on the timestamp from last window
        :param trailing_timestamp: timestamp from the last window
        :return: a dictionary containing data. each value is a matrix of size (n_sample_size, n_channel_count)
        """
        analysis_window = {}

        for uid, buffer in buffers.items():#self.buffers.items():

            # compute the sample start
            latest_sample_at, _ = buffer[-1]
            sample_offset = int(round((latest_sample_at - trailing_timestamp) * self.sample_rate))
            sample_start = len(buffer) - self.window_length - sample_offset
            if sample_start < 0:
                self.logger.info("Not enough data to process in buffer {}, using dummy data".format(uid))
                analysis_window[uid] = np.zeros((self.window_length, self.channel_count))
            else:
                # take data from buffer
                timestamped_window = list(islice(buffer, sample_start, sample_start + self.window_length))
                analysis_window[uid] = np.array([sample[1] for sample in timestamped_window])
        return analysis_window

    def _calculate_all(self, analysis_window):
        """
        compute analytic signal from the analysis window
        :param analysis_window: a dictionary containing data
        :return: a matrix of shape (n_freq_bands, n_subjects, n_channel_count, n_sample_size)
        """
        all_analytic = zscore(np.swapaxes(np.array(list(analysis_window.values())),1,2), axis=-1)  # shape = (n_sub, n_chn, n_times)
        all_analytic = np.array([hilbert(lfilter(coeff[0], coeff[1], all_analytic)) for c, coeff in enumerate(self.COEFFICIENTS)])
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
        """
        helper function for computing connectivity value.
        The result is a connectivity matrix of all possible electrode pairs between the dyad, including inter- and intra-brain connectivities.
        :param complex_signal: complex signal of shape (n_freq, 2, n_channel_count, n_sample_size). data for one dyad.
        :param mode: connectivity mode. see notes for details.
        :return: connectivity matrix of shape (n_freq, 2*n_channel_count, 2*channel_count)
        """
        n_ch, n_freq, n_samp = complex_signal.shape[2], complex_signal.shape[0], \
                               complex_signal.shape[3]

        complex_signal = complex_signal.reshape(n_freq, 2 * n_ch, n_samp)
        transpose_axes = (0, 2, 1)
        if mode.lower() == 'plv':
            phase = complex_signal / np.abs(complex_signal)
            c = np.real(phase)
            s = np.imag(phase)
            dphi = self._multiply_conjugate(c, s, transpose_axes=transpose_axes)
            con = abs(dphi) / n_samp

        elif mode.lower() == 'envelope correlation':
            env = np.abs(complex_signal)
            mu_env = np.mean(env, axis=2).reshape(n_freq, 2 * n_ch, 1)
            env = env - mu_env
            con = np.einsum('ilm,imk->ilk', env, env.transpose(transpose_axes)) / \
                  np.sqrt(np.einsum('il,ik->ilk', np.sum(env ** 2, axis=2), np.sum(env ** 2, axis=2)))

        elif mode.lower() == 'power correlation':
            env = np.abs(complex_signal) ** 2
            mu_env = np.mean(env, axis=2).reshape(n_freq, 2 * n_ch, 1)
            env = env - mu_env
            con = np.einsum('ilm,imk->ilk', env, env.transpose(transpose_axes)) / \
                  np.sqrt(np.einsum('il,ik->ilk', np.sum(env ** 2, axis=2), np.sum(env ** 2, axis=2)))

        elif mode.lower() == 'coherence':
            c = np.real(complex_signal)
            s = np.imag(complex_signal)
            amp = np.abs(complex_signal) ** 2
            dphi = self._multiply_conjugate(c, s, transpose_axes=transpose_axes)
            con = np.abs(dphi) / np.sqrt(np.einsum('il,ik->ilk', np.nansum(amp, axis=2),
                                                            np.nansum(amp, axis=2)))
            # self.logger.warning('con '+str(con[2,18:,0:18]))
        elif mode.lower() == 'imaginary coherence':
            c = np.real(complex_signal)
            s = np.imag(complex_signal)
            amp = np.abs(complex_signal) ** 2
            dphi = self._multiply_conjugate(c, s, transpose_axes=transpose_axes)
            con = np.abs(np.imag(dphi)) / np.sqrt(np.einsum('il,ik->ilk', np.nansum(amp, axis=2),
                                                            np.nansum(amp, axis=2)))

        elif mode.lower() == 'ccorr':
            angle = np.angle(complex_signal)
            mu_angle = circmean(angle, axis=2).reshape(n_freq, 2 * n_ch, 1)
            angle = np.sin(angle - mu_angle)

            formula = 'ilm,imk->ilk'
            con = np.einsum(formula, angle, angle.transpose(transpose_axes)) / \
                  np.sqrt(np.einsum('il,ik->ilk', np.sum(angle ** 2, axis=2), np.sum(angle ** 2, axis=2)))

        else:
            ValueError('Metric type not supported.')

        return con

    def _calculate_rvalues(self, analytic_matrix, mode):
        """
        computes connectivity value from the analytic signal
        :param analytic_matrix: analytic signal of shape (n_freq_bands, n_subjects, n_channel_count, n_sample_size)
        :param mode: connectivity mode. see notes for details.
        :return: a list of length = n_connections * n_freq. connectivity values
        """
        # compute all possible pair combinations
        pair_index = [a for a in
                      list(product(np.arange(0, analytic_matrix.shape[1]), np.arange(0, analytic_matrix.shape[1])))
                      if a[0] < a[1]]
        rvals = []
        # iterate for each combination
        for pair in pair_index:
            con = np.abs(self.compute_sync(analytic_matrix[:, pair, :, :], mode))
            # the connectivity matrix for the current pair. shape is (n_freq, n_ch, n_ch)
            con = con[:, 0:self.channel_count, self.channel_count:]
            if 'all-to-all' in self.chn_type:  # all to all correlation
                result = [np.nanmean(con[i, self.chnParams[freq]][:, self.chnParams[freq]], axis=(0, 1))
                          for i, freq in enumerate(self.freqParams.keys())]
            else:  # channel to channel correlation
                result = [np.nanmean(np.diagonal(con[i], axis1=0, axis2=1)[self.chnParams[freq]])
                          for i, freq in enumerate(self.freqParams.keys())]
            # adjust result according to weight parameters
            weights = list(self.weightParams.values())
            result = [r*weight for r, weight in zip(result, weights)]
            result = [self._clamp((r-minn)/(maxx-minn)) for r, minn, maxx in zip(result, self.norm_min, self.norm_max)]
            rvals.extend(result)

        return rvals  # a list of length n_connections * n_freq


