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

image1 = cv2.imread(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', 'p1'), 'mask_self.png'))


for mask_f in ['p1', 'p2', 'p3', 'p4', 'p6']:
    image2 = cv2.imread(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/test/', mask_f), 'mask_self.png'))
    difference = cv2.absdiff(image1, image2)
    gray_diff = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    num_different_pixels = np.count_nonzero(gray_diff)
    print(num_different_pixels / (1280*720))