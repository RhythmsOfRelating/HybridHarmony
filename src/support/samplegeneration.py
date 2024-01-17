from threading import current_thread, Thread
import numpy as np
import random, sys, os
import string, time
from .xdf import load_xdf
from pylsl import local_clock, StreamInfo, StreamOutlet

RANDOM_CHN = 16

class SampleGeneration:
  def __init__(self, mode):
    self.mode = mode
    self.thread = None
    self.running = False
    # initialize
    self.outlets = []
    self.sample_rate = None
    self.num_streams = None
    if mode == "random":
        self.sample_rate = 60.0
        self.num_streams = 2
    self._outlet()

  def start(self):
    if self.thread:
      return False
    self.thread = Thread(target=self._update, daemon=True, name="SendingData")
    self.running = True
    self.thread.start()

    return True

  def stop(self):
    if not self.thread:
      return True

    self.running = False
    if current_thread() is not self.thread:
      self.thread.join()
    self.thread = None

    return True


  def _outlet(self):
      if self.mode == "random":
          colors = ['Purple', 'Orange', 'Green', 'Blue', 'Black', 'White']
          for num in range(self.num_streams):
              letters = string.digits
              id = ''.join(random.choice(letters) for i in range(4))
              uid = str(colors[num]) + '-' + id
              info = StreamInfo('EEG-{}'.format(uid), 'EEG', RANDOM_CHN, self.sample_rate, 'float32', uid)
              self.outlets.append(StreamOutlet(info))
      elif self.mode == "sample":
          # filepath = self.resource_path('support/session_2020_02_21_14_21_11_anticipation.xdf')  # TODO
          filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'session_2020_02_21_14_21_11_anticipation.xdf')
          raw_file = load_xdf(filepath, synchronize_clocks=False, dejitter_timestamps=False, verbose=False)[0]
          raw_file = [f for f in raw_file if 'EEG' in f['info']['name'][0]]
          # defining output streams
          for i, person in enumerate(raw_file):
              id = person['info']['source_id']
              info = StreamInfo(person['info']['name'][0], person['info']['type'][0],
                                int(person['info']['channel_count'][0]),
                                int(person['info']['nominal_srate'][0]), person['info']['channel_format'][0], id[0])
              # add channels
              try:
                  channels_to_add = [x['label'][0] for x in person['info']['desc'][0]['channels'][0]['channel']]
                  chns = info.desc().append_child("channels")
                  for label in channels_to_add:
                      ch = chns.append_child("channel")
                      ch.append_child_value("label", label)
                      ch.append_child_value("unit", "microvolts")
                      ch.append_child_value("type", "EEG")
              except:
                  pass
              self.outlets.append(StreamOutlet(info))
      elif self.mode == 'biosemi':
          filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'daisychained_biosemi.xdf')
          raw_file = load_xdf(filepath, synchronize_clocks=False, dejitter_timestamps=False, verbose=False)[0]
          person = raw_file[0]
          # defining output streams
          id = person['info']['source_id']
          info = StreamInfo(person['info']['name'][0], person['info']['type'][0],
                            int(person['info']['channel_count'][0]),
                            int(person['info']['nominal_srate'][0]), person['info']['channel_format'][0], id[0])
          # add channels
          channels_to_add = [x['label'][0] for x in person['info']['desc'][0]['channels'][0]['channel']]
          meta_channels = info.desc().append_child('channels')
          for channel in channels_to_add:
              meta_channels.append_child('channel') \
                  .append_child_value('label', channel) \
                  .append_child_value('unit', 'microvolts') \
                  .append_child_value('type', 'EEG')
          self.outlets.append(StreamOutlet(info))


  def _update(self):
    while self.running:
        if self.mode == 'random':
            ts = local_clock()
            for outlet in self.outlets:
                sample = list(np.random.rand(RANDOM_CHN))
                outlet.push_sample(sample, timestamp=ts)
            time.sleep(1.0 / self.sample_rate)
        elif self.mode == 'sample':
            # filepath = self.resource_path('support/session_2020_02_21_14_21_11_anticipation.xdf')  # TODO
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'session_2020_02_21_14_21_11_anticipation.xdf')
            raw_file = load_xdf(filepath, synchronize_clocks=False, dejitter_timestamps=False, verbose=False)[0]
            raw_file = [f for f in raw_file if 'EEG' in f['info']['name'][0]]
            # defining output streams
            data = []
            for i, person in enumerate(raw_file):
                id = person['info']['source_id']
                raw = person['time_series'].T
                data.append(raw)
            print("now sending data...")
            length = min([d.shape[1] for d in data])
            for i in range(length):
                ts = local_clock()
                for subject, outlet in enumerate(self.outlets):
                    outlet.push_sample(data[subject][:, i], timestamp=ts)
                time.sleep(0.004)
        elif self.mode == 'biosemi':
            # filepath = self.resource_path('support/session_2020_02_21_14_21_11_anticipation.xdf')  # TODO
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'daisychained_biosemi.xdf')
            raw_file = load_xdf(filepath, synchronize_clocks=False, dejitter_timestamps=False, verbose=False)[0]
            # defining output streams
            data = []
            for i, person in enumerate(raw_file):
                id = person['info']['source_id']
                raw = person['time_series'].T
                data.append(raw)
            print("now sending data...")
            length = min([d.shape[1] for d in data])
            for i in range(length):
                ts = local_clock()
                for subject, outlet in enumerate(self.outlets):
                    outlet.push_sample(data[subject][:, i], timestamp=ts)
                time.sleep(1/int(person['info']['nominal_srate'][0]))

  def resource_path(self, relative_path):
      if hasattr(sys, '_MEIPASS'):
          return os.path.join(sys._MEIPASS, relative_path)
      return os.path.join(os.path.abspath("."), relative_path)