from threading import current_thread, Thread
from random import random as rand
import random
import string, time
from pylsl import local_clock, StreamInfo, StreamOutlet

class SampleGeneration:
  def __init__(self, mode):
    self.mode = mode
    self.thread = None
    self.running = False
    # initialize
    self.outlets = []
    self.sample_rate = 60.0
    self.num_streams = 2

  def start(self):
    if self.thread:
      return False
    self.thread = Thread(target=self._update, daemon=True, name="SendingData")
    self.running = True
    self.thread.start()

    colors = ['Purple', 'Orange', 'Green', 'Blue', 'Black', 'White']

    for num in range(self.num_streams):
        letters = string.digits
        id = ''.join(random.choice(letters) for i in range(4))
        uid = str(colors[num]) + '-' + id
        info = StreamInfo('EEG-{}'.format(uid), 'EEG', 32, self.sample_rate, 'float32', uid)
        self.outlets.append(StreamOutlet(info))

    return True

  def stop(self):
    if not self.thread:
      return True

    self.running = False
    if current_thread() is not self.thread:
      self.thread.join()
    self.thread = None

    return True

  def _update(self):
    while self.running:
        ts = local_clock()
        for outlet in self.outlets:
            sample = [rand()] * 32
            outlet.push_sample(sample, timestamp=ts)

        time.sleep(1.0 / self.sample_rate)
