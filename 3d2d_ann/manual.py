# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import math  
import sys
import argparse
from scipy.spatial.distance import cosine
import cv2
import json
from os.path import basename

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
parser.add_argument('--target', type=str)
args = parser.parse_args()

def has_big_difference(numbers, threshold):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) > threshold:
                return True
    return False





img_path = args.data
if not os.path.exists(img_path):
    with open('error_log_sync.txt', 'a') as error_file:
        error_file.write(f"not exist {args.data}\n")
    sys.exit(1)
target_path = args.target
if img_path[-1]!='/':
    img_path+='/'
if target_path[-1]!='/':
    target_path+='/'


if not os.path.exists(target_path+'manual.txt'):
    sys.exit(1)
with open(target_path+'manual.txt', 'r') as f:
    key_imgs = f.read().strip()
key_imgs = key_imgs[1:-1].split(', ')


file_names_all = [[] for i in range(5)]

for fn in os.listdir(img_path):
    if ".jpg" in fn:
        file_names_all[int(fn[3])-1].append(fn)

for i in range(5):
    file_names_all[i] = sorted(file_names_all[i])    


lens = [len(i) for i in file_names_all]

print('ssss')

res = []
key_list = []
move_idx=[]
cam1_flag = None
for i in range(5):
    move_img = key_imgs[i][1:-1]
    print(move_img)
    key_list.append(move_img)
    if not move_img:
        with open('error_log_sync.txt', 'a') as error_file:
            error_file.write(f"not moving {args.data}\n")
        sys.exit(1)
    tmp_dict={}
    move_time = int(move_img[5:-4])
    if i == 0:
        cam1_flag = move_time
    for img in file_names_all[i]:
        img_time = int(img[5:-4])
        # if img_time>move_time:
        tmp_dict[img] = img_time-move_time+cam1_flag
        # else:
        #     tmp_dict[img] = None
    res.append(tmp_dict)

with open(target_path+'sync_data.json', "w") as json_file:
    json.dump(res, json_file, indent=4)
print(target_path)

## qian 3 ge