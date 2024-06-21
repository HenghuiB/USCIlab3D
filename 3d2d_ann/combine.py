import numpy as np
import pickle
import sys
from os.path import join, basename
input = sys.argv[1]


all_labels = []
for i in range(6):
    with open(join(join(input, 'Cam'+str(i)), 'labels'), 'rb') as f:
        label = pickle.load(f)
        print(label)
    all_labels += label

all_labels = list(set(all_labels))
print(all_labels)
label_proj = []
for i in range(6):
    tmp = []
    with open(join(join(input, 'Cam'+str(i)), 'labels'), 'rb') as f:
        label = pickle.load(f)
        for idx in range(len(label)):
            tmp.append(all_labels.index(label[idx]))

    label_proj.append(tmp)

with open('labels_proj', 'wb') as f:
    pickle.dump(label_proj, f)