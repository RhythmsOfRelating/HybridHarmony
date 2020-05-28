import sys
from scipy.signal import butter, lfilter
import numpy as np
from itertools import islice
from scipy.signal import hilbert
import json
sys.path.extend(['C:\\Users\\Phoebe Chen\\Downloads\\harmonic-dissonance\\LSLanalysis'])
from acquisition import Discovery
from analysis import Analysis
from analysis.buffer import Buffer
PATH_TOPO = './LSLanalysis/analysis/topo.json'
PATH_SELECT = './LSLanalysis/analysis/select.json'

ORDER = 5
WINDOW = 3
BANDS = {
    'delta': (1, 4),
    'theta': (4, 8),
    'alpha': (8, 14),
    'beta':  (14, 20)
}


discovery = Discovery(
discard_timestamps=True,
correct_timestamps=False
)
discovery.start()

def _setup_coefficients(sample_rate):
    nyq = 0.5 * sample_rate
    min_band = 0.0 + 1.0e-10
    max_band = 1.0 - 1.0e-10
    coefficients = []
    for band in BANDS.values():
        low_band = max(min_band, min(max_band, band[0] / nyq))
        high_band = max(min_band, min(max_band, band[1] / nyq))
        low, high = butter(ORDER, [low_band, high_band], btype='band')
        coefficients.append([low, high])

    return coefficients


def _setup_hann(sample_size):
    denom = sample_size - 1
    hann = []
    for n in range(sample_size):
        hann.append(.5 * (1 - np.cos((2 * np.pi * n) / denom)))

    return np.array(hann)


def _setup_num_connections(buffers):
    return sum(list(range(1, len(buffers))))

def _select_analysis_window(buffers, sample_size, channel_count):
    analysis_window = {}

    for uid, buffer in buffers.items():
        latest_sample_at, _ = buffer[-1]
        # sample_offset = int(round((latest_sample_at - trailing_timestamp) * sample_rate))
        # sample_start = len(buffer) - sample_size - sample_offset
        sample_start = 0

        if sample_start < 0:
            analysis_window[uid] = np.zeros((sample_size, channel_count))
        else:
            timestamped_window = list(islice(buffer, sample_start, sample_start + sample_size))
            analysis_window[uid] = np.array([sample[1] for sample in timestamped_window])

    return analysis_window

def _setup_electrodes(channel_count):
    device = None

    if channel_count == 32:
        device = 'liveamp32'
    elif channel_count == 16:
        device = 'liveamp16'
    elif channel_count == 14:
        device = 'epoc+'
    elif channel_count == 4:
        device ='muse'

    if device:
        with open(PATH_TOPO, 'r') as f:
            topo = json.load(f)[device]
        with open(PATH_SELECT, 'r') as f:
            select = json.load(f)[device]
        choose = {key: [topo[electrode]-1 for electrode in val]
                  for key, val in select.items()}
    else:
        choose = {key:np.arange(0, channel_count, 1) for key in BANDS.keys()}  # other device types - use all channels
    return choose



sample_rate = discovery.sample_rate
channel_count = discovery.channel_count
sample_size = int(sample_rate * WINDOW)

buffer = Buffer(discovery)
buffer.pull()
buffers = buffer.buffers_by_uid  # input for correlation
stream_count = len(buffers)

COEFFICIENTS = _setup_coefficients(sample_rate)
HANN = _setup_hann(sample_size)
CONNECTIONS = _setup_num_connections(buffers)

# parameters
CHOOSE_CHANNELS = _setup_electrodes(channel_count)


def _apply_window_weights(analysis_window, sample_size, channel_count):
    for uid in analysis_window.keys():
        for sample in range(sample_size):
            for channel in range(channel_count):
                analysis_window[uid][sample][channel] *= HANN[sample]
    return analysis_window

def _apply_window_weights2(analysis_window, sample_size, channel_count):
    for uid in analysis_window.keys():
        analysis_window[uid]=np.multiply(analysis_window[uid], HANN[:,None])
    return analysis_window


def _calculate_envelope(signal, coeff):  # phoebe edit

    signal = lfilter(coeff[0], coeff[1], signal)

    analytic_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytic_signal)

    return amplitude_envelope


def _calculate_all(analysis_window, sample_rate, channel_count):
    all_envelope = np.empty((len(analysis_window), int(channel_count), len(COEFFICIENTS),
                             int(sample_rate * WINDOW)))  # n_persons x n_channels x n_freq x n_samples
    for i, current_window in enumerate(analysis_window.keys()):
        for channel in range(channel_count):
            for c, coeff in enumerate(COEFFICIENTS):
                envelope = _calculate_envelope(analysis_window[current_window][:, channel], coeff)

                all_envelope[i, channel, c, :] = envelope
    return all_envelope

def _calculate_rvalues(envelope_matrix, channel_count):

    rvalues = []

    for window_idx in range(len(envelope_matrix) - 1):
        compare_windows = len(envelope_matrix) - window_idx - 1
        compare_window_idx = 1
        while compare_window_idx <= compare_windows:
            # for each frequency, compute corr for all electrodes, and average over selected ones
            for freq, freq_name in enumerate(list(BANDS.keys())):
                rval_freq = []
                for electrode in range(channel_count):
                    r = np.corrcoef([envelope_matrix[window_idx, electrode, freq, :],
                                     envelope_matrix[compare_window_idx, electrode, freq, :]])[0][1]
                    rval_freq.append(r)
                rval_freq = np.array(rval_freq)
                rvalues.append(np.mean(rval_freq[CHOOSE_CHANNELS[freq_name]]))
            compare_window_idx += 1

    return rvalues  # n_connections x n_freq


# run
analysis_window = _select_analysis_window(buffers, sample_size, channel_count)
analysis_window1 = _apply_window_weights(analysis_window, sample_size, channel_count)
analysis_window2 = _apply_window_weights2(analysis_window, sample_size, channel_count)

# phoebe edit
envelope_matrix = _calculate_all(analysis_window, sample_rate, channel_count)
rvalues = _calculate_rvalues(envelope_matrix, channel_count)
power_values = _calculate_power(envelope_matrix)

list(analysis_window.values())[0].shape

