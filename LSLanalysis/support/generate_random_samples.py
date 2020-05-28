import time
import uuid
import argparse

parser = argparse.ArgumentParser(description='Stream Random LSL data')
parser.add_argument('--num-streams', metavar='N', dest='num_streams', type=int, default=2, choices=range(2,7), help='Set number of random EEG streams')
args = parser.parse_args()

from random import random as rand
from pylsl import local_clock, StreamInfo, StreamOutlet

outlets = []
sample_rate = 60.0
num_streams = args.num_streams
colors = ['Purple', 'Orange', 'Green', 'Blue', 'Black', 'White']

for num in range(num_streams):
  uid = str(colors[num]) + '-' + str(uuid.uuid4())
  info = StreamInfo('EEG-{}'.format(uid), 'EEG', 32, sample_rate, 'float32', uid)
  outlets.append(StreamOutlet(info))

while True:
  ts = local_clock()
  for outlet in outlets:
    sample = [rand()]*32
    outlet.push_sample(sample, timestamp=ts)

  time.sleep(1.0 / sample_rate)
