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