import numpy as np
import pickle
import sys,os
from os.path import join, basename
# input = sys.argv[1]

input = '/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/res/'

all_labels = []
for file in os.listdir(input):
    with open(join(join(input, file), 'labels'), 'rb') as f:
        label = pickle.load(f)
        label = [ll[:-6] for ll in label]
        # print(label)
    all_labels += label

all_labels = list(set(all_labels))
print(all_labels)
label_proj = {}
for file in os.listdir(input):
    tmp = []
    with open(join(join(input, file), 'labels'), 'rb') as f:
        label = pickle.load(f)
        label = [ll[:-6] for ll in label]
        for idx in range(len(label)):
            tmp.append(all_labels.index(label[idx]))

    label_proj[file] = tmp
print(label_proj)
with open('labels_proj', 'wb') as f:
    pickle.dump(label_proj, f)
