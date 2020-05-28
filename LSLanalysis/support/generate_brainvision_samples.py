import time
import os

from mne.io import read_raw_brainvision


from pylsl import StreamInfo, StreamOutlet, local_clock

files = []
names = []
path = './support'
for file in os.listdir(path):
    if file.endswith(".vhdr"):
        files.append(os.path.join(path, file))
        names.append(file.split('.')[0])

# defining output streams
outlets = []
data = []

for file, name in zip(files, names):
    raw = read_raw_brainvision(file).get_data()
    info = StreamInfo('EEG-{}'.format(name),
                            'EEG', raw.shape[0], 250, 'float32', name)
    outlets.append(StreamOutlet(info))
    data.append(raw)
                   

print("now sending data...")
length = min([d.shape[1] for d in data])
for i in range(length):
    ts = local_clock()
    for subject, outlet in enumerate(outlets):
        outlet.push_sample(data[subject][:, i],timestamp=ts)
    time.sleep(0.004)
