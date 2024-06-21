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

from PIL import Image
def generate_color(word):
    # Generate a unique color based on the hash value of the word
    color = hash(word) % 0xFFFFFF  # Using a 24-bit color space
    return color




# r_mask = torch.load(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', 'p1'), 'masks.pt')).cpu().numpy()
# with open(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', 'p1'), 'labels'), 'rb') as f:
#     r_label = pickle.load(f)
# d = {}
# for idx, l in enumerate(r_label):
#     d[l[:-6]] = idx
    
for mask_f in ['p1', 'p2', 'p3', 'p4', 'p6']:
    tmp={}
    masks = torch.load(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'masks.pt')).cpu().numpy()
    with open(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'labels'), 'rb') as f:
        label = pickle.load(f)
    for mask in range(masks.shape[0]):
        indices = np.argwhere(masks[mask] == 1)
        pixels_with_value_1 = [(x, y) for _, x, y in indices]
        for pixel in pixels_with_value_1:
            if (pixel[1],pixel[0]) in tmp.keys():
                tmp[(pixel[1],pixel[0])]+=[label[mask]]
            else:
                tmp[(pixel[1],pixel[0])]=[label[mask]]

    image = Image.new('RGB', (masks.shape[3], masks.shape[2]), 'black')
    pixels = image.load()

    for o_key,o_value in tmp.items():
        obj = sorted(o_value, key=lambda x: float(x[-5:-1]))[-1]
        color = generate_color(obj[:-6])
        pixels[o_key[0], o_key[1]] = (color >> 16, (color >> 8) & 0xFF, color & 0xFF)
    image.save(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'mask_self.png'))
        # for tmp in pixels_with_value_1:
        #     color = r_img[r_mask[d[label[mask][:-6]]][0][1], r_mask[d[label[mask][:-6]]][0][0]]
        #     img[tmp[1], tmp[0]] = color
    # cv2.imwrite(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'mask_s.jpg'), img)