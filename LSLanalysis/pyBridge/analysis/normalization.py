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
from osc4py3.as_allthreads import *
from osc4py3 import oscbuildparse
from osc4py3 import oscchannel as osch

current = os.path.dirname(__file__)

LAST_CALCULATION = local_clock()
ORDER = 5
WINDOW = 3

class Normalization:
    def __init__(self, buffers, mode, OSC_params, weight, manual_params, auto_params):
        self.logger = logging.getLogger(__name__)
        self.mode = mode
        self.buffers = buffers
        self.OSC_params = OSC_params
        self.weight = weight
        self.manual_params = manual_params
        self.auto_params = auto_params
        self._setup_outlet()
        # if OSC_params[0] is not None:
        #     self._setup_OSC()

    def _setup_OSC(self):
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
        sample_size = self.CONNECTIONS * len(self.freqParams)
        # first message is empty
        msg = oscbuildparse.OSCMessage("/Rvalues/me", ","+'f'*sample_size, [0]*sample_size)
        osc_send(msg, 'Rvalues')

    def _setup_outlet(self):
        self.sample_size = len(self.buffers.values())
        if self.sample_size == 0:
            return
        # TODO
        self.sample_size = 3
        info = StreamInfo('NormValues', 'Markers', self.sample_size, IRREGULAR_RATE, cf_float32, "RValues-{}".format(getpid()))
        info.desc().append_child_value("NormCorrelation", "R")
        
        mappings = info.desc().append_child("mappings")
        buffer_keys = list(self.buffers.keys())
        pair_index = [a for a in
                      list(product(np.arange(0, len(buffer_keys)), np.arange(0, len(buffer_keys))))
                      if a[0] < a[1]]

        for pair in pair_index:
            mappings.append_child("mapping") \
                .append_child_value("from", buffer_keys[pair[0]]) \
                .append_child_value("to", buffer_keys[pair[1]])

        return StreamOutlet(info)

    def run(self):
        global LAST_CALCULATION
        trailing_timestamp = self._find_trailing_timestamp()

        if trailing_timestamp != LAST_CALCULATION:
            # self.logger.warning('trailing timestamp %s, last calculation %s' % (trailing_timestamp, LAST_CALCULATION))

            LAST_CALCULATION = trailing_timestamp
            # analysis_window = self._select_analysis_window(trailing_timestamp)
            # all_analytic = np.array(list(analysis_window.values())).reshape(
            #     (len(analysis_window), 3, -1))

            # TODO
            rvalues = [1,2,3]
            if self.OUTLET:
                self.logger.warning("Sending {} norm values with timestamp {}".format(len(rvalues), trailing_timestamp))
                self.logger.warning(str(rvalues))
                self.OUTLET.push_sample(rvalues, timestamp=trailing_timestamp)

            # # sending OSC packets
            # if self.OSC_params[0] is not None:  # if sending OSC
            #     sample_size = self.CONNECTIONS * len(self.freqParams)
            #     msg = oscbuildparse.OSCMessage("/Rvalues/me", ","+'f'*sample_size, rvalues)
            #     osc_send(msg, 'Rvalues')
            #     osc_process()
        else:
            self.logger.debug("Still waiting for new data to arrive, skipping analysis")
            return

    def _clamp(self, n):
        return max(min(1, n), 0)

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



