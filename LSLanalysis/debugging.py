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

"""
OSC
"""
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
from osc4py3 import oscchannel as osch
IP = '192.168.0.4'
port = '2781'
# Start the system.
osc_startup()
# Make client channels to send packets.
try:
    osc_udp_client(IP, int(port), "Rvalues")
except:
    osch.terminate_all_channels()
    osc_udp_client(IP, int(port), "Rvalues")
sample_size = 4
# first message is empty
msg = oscbuildparse.OSCMessage("/Rvalues/me", "," + 'f' * sample_size, [0] * sample_size)
osc_send(msg, 'Rvalues')
# while True:
#     msg = oscbuildparse.OSCMessage("/Rvalues/me", "," + 'f' * sample_size, [0] * sample_size)
#     osc_send(msg, 'Rvalues')
#     osc_process()

"""
receiving OSC
"""

def handlerfunction(s, x, y):
    # Will receive message data unpacked in s, x, y
    pass

def handlerfunction2(address, s, x, y):
    # Will receive message address, and message data flattened in s, x, y
    pass

# Start the system.
osc_startup()

# Make server channels to receive packets.
osc_udp_server("192.168.0.0", 3721, "aservername")
osc_udp_server("0.0.0.0", 3724, "anotherserver")

# Associate Python functions with message address patterns, using default
# argument scheme OSCARG_DATAUNPACK.
osc_method("/test/*", handlerfunction)
# Too, but request the message address pattern before in argscheme
osc_method("/test/*", handlerfunction2, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)

# Periodically call osc4py3 processing method in your event loop.
finished = False
while not finished:
    # …
    osc_process()
    # …

# Properly close the system.
osc_terminate()