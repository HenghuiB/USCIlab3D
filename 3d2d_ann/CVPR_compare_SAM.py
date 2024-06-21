import sys
import struct
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random
import torch
import pickle
import colorsys
from collections import Counter
import collections
from IPython import embed
import os
import cv2
from os.path import join


r_mask = torch.load(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', 'p1'), 'masks.pt')).cpu().numpy()
with open(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', 'p1'), 'labels'), 'rb') as f:
    r_label = pickle.load(f)
r_img = cv2.imread(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', 'p1'), 'mask.jpg'))
# embed()
d = {}
for idx, l in enumerate(r_label):
    d[l[:-6]] = idx
    
for mask_f in ['p2', 'p3', 'p4', 'p5', 'p6']:
    total=0
    diff=0
    masks = torch.load(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'masks.pt')).cpu().numpy()
    with open(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'labels'), 'rb') as f:
        label = pickle.load(f)
    img = cv2.imread(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'mask.jpg'))
    for mask in range(masks.shape[0]):
        clabel = d[label[mask][:-6]]
        ooo = r_mask[clabel][0]
        now = masks[mask][0]
        diff+=np.sum(ooo != now)
        total+=ooo.shape[0]*ooo.shape[1]
        # cp = masks[mask][0]
        # for x in range(cp.shape[0]):
        #     for y in range(cp[x].shape[0]):
        #         if cp[x][y] == r_mask[d[label[mask][:-6]]][0][x][y]:
        #             continue
        #         else:
        #             diff+=1
        #         total+=1



        # indices = np.argwhere(masks[mask] == 1)
        # pixels_with_value_1 = [(x, y) for _, x, y in indices]
        # for tmp in pixels_with_value_1:
        #     color = r_img[r_mask[d[label[mask][:-6]]][0][1], r_mask[d[label[mask][:-6]]][0][0]]
        #     img[tmp[1], tmp[0]] = color
    print(diff/total)
    # cv2.imwrite(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'mask_s.jpg'), img)