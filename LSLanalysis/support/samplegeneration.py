from threading import current_thread, Thread
from random import random as rand
import random, sys, os
import string, time
from .xdf import load_xdf
from pylsl import local_clock, StreamInfo, StreamOutlet

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
              info = StreamInfo('EEG-{}'.format(uid), 'EEG', 32, self.sample_rate, 'float32', uid)
              self.outlets.append(StreamOutlet(info))
      else:
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
              self.outlets.append(StreamOutlet(info))


  def _update(self):
    while self.running:
        if self.mode == 'random':
            ts = local_clock()
            for outlet in self.outlets:
                sample = [rand()] * 32
                outlet.push_sample(sample, timestamp=ts)
            time.sleep(1.0 / self.sample_rate)
        else:
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

  def resource_path(self, relative_path):
      if hasattr(sys, '_MEIPASS'):
          return os.path.join(sys._MEIPASS, relative_path)
      return os.path.join(os.path.abspath("."), relative_path)