import time
from pylsl import StreamInfo, StreamOutlet, local_clock
import xdf

filepath = './session_2020_02_21_14_21_11_anticipation.xdf'

raw_file = xdf.load_xdf(filepath, synchronize_clocks=False, dejitter_timestamps=False, verbose=False)[0]
raw_file = [f for f in raw_file if 'EEG' in f['info']['name'][0]]

# defining output streams
outlets = []
data = []
for i, person in enumerate(raw_file):
    id = person['info']['source_id']
    raw = person['time_series'].T
    info = StreamInfo(person['info']['name'][0],person['info']['type'][0],int(person['info']['channel_count'][0]),
                    int(person['info']['nominal_srate'][0]), person['info']['channel_format'][0], id[0])
    outlets.append(StreamOutlet(info))
    data.append(raw)

print("now sending data...")
length = min([d.shape[1] for d in data])
for i in range(length):
    ts = local_clock()
    for subject, outlet in enumerate(outlets):
        outlet.push_sample(data[subject][:, i],timestamp=ts)
    time.sleep(0.004)
