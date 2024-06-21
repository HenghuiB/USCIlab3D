import sys
import struct
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random
import torch
import open3d as o3d
import cv2
import pickle, os
import colorsys
from collections import Counter
#from undistort import *
from os.path import join
import transforms3d.euler as euler
import bisect



def write_ply_point_cloud(filename, points, intensities, objs):


    pcd = o3d.t.geometry.PointCloud()

    pcd.point["positions"] = o3d.core.Tensor(points)
    pcd.point["intensity"] = o3d.core.Tensor(intensities)
    pcd.point["obj_id"] = o3d.core.Tensor(objs)
    o3d.t.io.write_point_cloud(filename, pcd)

def find_difference(sorted_list, target):
    pos = bisect.bisect_left(sorted_list, target)
    
    if pos == 0:
        closest = sorted_list[0]
    elif pos == len(sorted_list):
        closest = sorted_list[-1]
    else:
        before = sorted_list[pos - 1]
        after = sorted_list[pos]
        if abs(before - target) <= abs(after - target):
            closest = before
        else:
            closest = after

    difference = abs(closest - target)
    
    return closest, difference

def concat_e(a, b):
    if a.size == 0:
        return b
    return np.concatenate((a, b),axis=0)

def convert(pcd,pose):
    pose = [float(i) for i in pose.split(',')]
    pcd = o3d.t.io.read_point_cloud(pcd)
    intensity = pcd.point.intensity.numpy()   
    objs = pcd.point.obj_id.numpy()   
    pcd = pcd.point.positions.numpy()
    pcd = pcd[:, [1,2,0]]
    LiDAR_R = euler.euler2mat(pose[3], pose[4], pose[5], 'sxyz')
    LiDAR_T = np.array(pose[:3])
    pcd = np.dot(pcd,LiDAR_R.T)
    pcd = pcd + LiDAR_T
    return pcd, intensity, objs

def run(folder_path):
    pcd_path = join(join('/lab/tmpig13c/henghui/semantic_pcd/', folder_path.split('/')[-3], folder_path.split('/')[-2]))
    if not os.path.exists(pcd_path):
        print(f"Error: Folder '{folder_path}'pcd error.")
        return
    pcds = os.listdir(pcd_path)
    pcd_time = [int(i[:-3].replace('.','')) for i in pcds]
    tmp_pcd = dict(zip(pcd_time, pcds))
    pcd_time.sort()
    odo_path = join(folder_path,'all_odom', 'odometry.txt')
    with open(odo_path, 'r') as f:
        odo = f.read().splitlines() 
    odo_time = [int(i.split()[-1].replace('.','')) for i in odo]
    tmp_odo = dict(zip(odo_time, odo))
    odo_time.sort()
    points = np.array([])
    intensity = np.array([])
    objs = np.array([])
    for idx, t in enumerate(odo_time):
        pcd, diff = find_difference(pcd_time, t)
        print(diff)
        if diff<3:
            pcd = tmp_pcd[pcd]
            tmp_points, tmp_intensity, tmp_objs = convert(join(pcd_path, pcd, str(pcd)+'.pcd'), tmp_odo[t])
            points = concat_e(points, tmp_points)
            intensity = concat_e(intensity, tmp_intensity)
            objs = concat_e(objs, tmp_objs)
        if idx%10==0:
            if points.size!=0:
                write_ply_point_cloud(join('/lab/tmpig13c/henghui/semantic_sector/', str(idx)+'.pcd'), points, intensity, objs)
            points = np.array([])
            intensity = np.array([])
            objs = np.array([])
    



if __name__ == '__main__':
    # pose = [1.058397, 0.004454, 0.535451, 0.002097, -0.320148, -0.000217]
    # pose = [163.998657, 0.090200, -59.160156, 0.043270, 2.935366, -0.013241]
    # # pcd = convert('./construct/1680028206.815233469.pcd', pose)
    # pcd = convert('./construct/1680028619.564516068.pcd', pose)
    run('/lab/tmpig13b/kiran/bag_dump/2023_03_11/0/')

    # write_ply_point_cloud('point_cloud_dense3.ply', pcd)
