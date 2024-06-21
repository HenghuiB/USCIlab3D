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

def get_key_image(images):
    images =[os.path.join(args.data, img) for img in images]
    if len(images)<=1:
        with open('error_log_sync.txt', 'a') as error_file:
            error_file.write(f"{args.data}\n")
        sys.exit(1)
        
    color = np.random.randint(0,255,(100,3))
    old_frame = cv2.imread(images[0])
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_RGB2GRAY)
    mask = np.zeros_like(old_frame)
    mask_features = np.zeros_like(old_gray)
    # mask_features[:,0:20] = 1
    # mask_features[:,620:640] = 1
    mask_features[:,:] = 1
    mask_features[:,:] = 1
    feature_params = dict( maxCorners = 100,qualityLevel = 0.3,minDistance = 3,blockSize = 7,mask = mask_features)
    lk_params = dict( winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    def init_new_features(gray_frame):
        corners = cv2.goodFeaturesToTrack(gray_frame, **feature_params)
        return corners
    def calculateDistance(x1,y1,x2,y2):  
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        return dist  
    corners = init_new_features(old_gray)
    for tmp_idx, img in enumerate(images):
        cam_moved = False
        frame = cv2.imread(img)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, corners, None, **lk_params)
        good_new = p1
        good_old = corners
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            distance = calculateDistance(a,b,c,d)
            if distance>10:
                cam_moved = True
                old_gray = frame_gray.copy()
                corners = init_new_features(old_gray)
            else:
                old_gray = frame_gray.copy()
                corners = good_new.reshape(-1,1,2)
            a,b = int(a), int(b)
            c,d = int(c), int(d)
            mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        mask = np.zeros_like(old_frame)
        if corners is None:
            corners = init_new_features(old_gray)
        if cam_moved is True:
            it = np.random.rand(1)[0]
            return img, tmp_idx
    return None, None
        



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

file_names_all = [[] for i in range(5)]

for fn in os.listdir(img_path):
    if ".jpg" in fn:
        file_names_all[int(fn[3])-1].append(fn)

for i in range(5):
    file_names_all[i] = sorted(file_names_all[i])    


lens = [len(i) for i in file_names_all]

for tmp_len in lens:
    if tmp_len == 0:
        with open('error_log_sync.txt', 'a') as error_file:
            error_file.write(f"empty {args.data}\n")
        sys.exit(1)
    if has_big_difference(lens, max(lens) * 0.1):
        with open('error_log_sync.txt', 'a') as error_file:
            error_file.write(f"difference {args.data} {lens}\n")
        sys.exit(1)

res = []
move_idx=[]
cam1_flag = None
for i in range(5):
    key_res = get_key_image(file_names_all[i])
    move_img, cam_idx = basename(key_res[0]), key_res[1]
    move_idx.append(cam_idx)
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
print(move_idx)
if has_big_difference(move_idx, max(lens) * 0.1):
    with open('error_log_sync.txt', 'a') as error_file:
        error_file.write(f"move detect not right {args.data} {move_idx}\n")
    sys.exit(1)
with open(target_path+'sync_data.json', "w") as json_file:
    json.dump(res, json_file, indent=4)
            
