import sys
from scipy.signal import butter, lfilter
import numpy as np
from itertools import islice
from scipy.signal import hilbert
import json
sys.path.extend(['D:\\PycharmProjects\\hyperscanning_BCI\\LSLanalysis'])
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

analysis = Analysis(discovery)
analysis.start()

analysis.stop()


"""
check stream
"""
from pylsl import StreamInlet, resolve_stream

# first resolve an EEG stream on the lab network
print("looking for an EEG stream...")


streams = resolve_stream('type', 'Markers')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[1])

while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample,timestamp = inlet.pull_sample()
    print("got %s at time %s" % (sample[0], timestamp))



### testing OUTLET
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

sample_size = 3*3

info = StreamInfo('RValues', 'Markers', sample_size, IRREGULAR_RATE, cf_float32, "RValues-{}".format(getpid()))
info.desc().append_child_value("correlation", "R")

mappings = info.desc().append_child("mappings")
buffer_keys = ['orange','blue','black']
pair_index = [a for a in
              list(product(np.arange(0,len(buffer_keys)), np.arange(0, len(buffer_keys))))
              if a[0] < a[1]]

for pair in pair_index:
    mappings.append_child("mapping") \
        .append_child_value("from", buffer_keys[pair[0]]) \
        .append_child_value("to", buffer_keys[pair[1]])
    print(buffer_keys[pair[0]],buffer_keys[pair[1]])

outlet = StreamOutlet(info)
rvalues = [1,2,2,1,2,3,1,2,3]
outlet.push_sample(rvalues, timestamp=111111)