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
import time
import colorsys
from collections import Counter
#from undistort import *
from os.path import join
import transforms3d.euler as euler
import bisect
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth
import copy
from scipy.spatial.distance import cdist
import shutil
def write_ply_point_cloud(filename, points, intensities, objs, instance):



    pcd = o3d.t.geometry.PointCloud()

    pcd.point["positions"] = o3d.core.Tensor(points)
    pcd.point["intensity"] = o3d.core.Tensor(intensities)
    pcd.point["obj_id"] = o3d.core.Tensor(objs)
    pcd.point["instance_id"] = o3d.core.Tensor(instance)
    o3d.t.io.write_point_cloud(filename, pcd, write_ascii=True)

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

def convert(pcd_points,pose):
    pose = [float(i) for i in pose.split(',')]
    pcd_points = o3d.t.io.read_point_cloud(pcd_points)
    intensity = pcd_points.point.intensity.numpy()   
    objs = pcd_points.point.obj_id.numpy()
    instance_id = pcd_points.point.instance_id.numpy()
    pcd_points = pcd_points.point.positions.numpy()
    old_pos = np.copy(pcd_points)
    pcd_points = pcd_points[:, [1,2,0]]
    LiDAR_R = euler.euler2mat(pose[3], pose[4], pose[5], 'sxyz')
    LiDAR_T = np.array(pose[:3])
    pcd_points = np.dot(pcd_points,LiDAR_R.T)
    pcd_points = pcd_points + LiDAR_T
    return pcd_points, intensity, objs, instance_id, old_pos

def update_instance(points, objs, instance, new_points, new_objs, new_instance, oi_dict, start_iid):
    new_objs = new_objs.squeeze()
    new_instance = new_instance.squeeze()
    if instance.size==0:
        assert start_iid==0
        instance = new_instance
        tmp_dict = {}
        for i in range(len(new_instance)):
            if new_objs[i] == 0:
                continue
            if new_objs[i] not in tmp_dict.keys():
                tmp_dict[new_objs[i]] = {}
                tmp_dict[new_objs[i]][new_instance[i]] = [i]
            else:
                if new_instance[i] not in tmp_dict[new_objs[i]].keys():
                    tmp_dict[new_objs[i]][new_instance[i]] = [i]
                else:
                    tmp_dict[new_objs[i]][new_instance[i]].append(i)
        oi_dict = tmp_dict
    else:
        new_instance += start_iid
        tmp_dict = {}
        for i in range(len(new_instance)):
            if new_objs[i] == 0:
                continue
            if new_objs[i] not in tmp_dict.keys():
                tmp_dict[new_objs[i]] = {}
                tmp_dict[new_objs[i]][new_instance[i]] = [i]
            else:
                if new_instance[i] not in tmp_dict[new_objs[i]].keys():
                    tmp_dict[new_objs[i]][new_instance[i]] = [i]
                else:
                    tmp_dict[new_objs[i]][new_instance[i]].append(i)
        for obj, instances in tmp_dict.items():
            if obj in oi_dict.keys():
                exist_points = copy.deepcopy(oi_dict[obj])
                add_points = instances
                for ex_instance, ex_points in exist_points.items():
                    for a_instance, a_points in add_points.items():
                        # if np.min(cdist(points[ex_points],new_points[a_points]))>1:
                        #     continue
                        tmp = concat_e(points[ex_points], new_points[a_points])

                        point_cloud = o3d.geometry.PointCloud()
                        point_cloud.points = o3d.utility.Vector3dVector(points[ex_points])
                        labels = np.array(point_cloud.cluster_dbscan(eps=1, min_points=4, print_progress=False))
                        a_num_clusters = len(np.unique(labels)) - (1 if -1 in np.unique(labels) else 0)

                        if a_num_clusters == 0:
                            continue
                        point_cloud = o3d.geometry.PointCloud()
                        point_cloud.points = o3d.utility.Vector3dVector(new_points[a_points])
                        labels = np.array(point_cloud.cluster_dbscan(eps=1, min_points=4, print_progress=False))
                        b_num_clusters = len(np.unique(labels)) - (1 if -1 in np.unique(labels) else 0)

                        if b_num_clusters == 0:
                            continue

                        point_cloud = o3d.geometry.PointCloud()
                        point_cloud.points = o3d.utility.Vector3dVector(tmp)
                        labels = np.array(point_cloud.cluster_dbscan(eps=1, min_points=4, print_progress=False))
                        num_clusters = len(np.unique(labels)) - (1 if -1 in np.unique(labels) else 0)
                        # if num_clusters==1:
                        if num_clusters==max(a_num_clusters, b_num_clusters):
                            new_instance[a_points] = ex_instance
                            break
        oi_dict = tmp_dict
        new_instance[np.where(new_objs == 0)] = -1
    start_iid = np.max(new_instance)
    print(start_iid)
    return new_instance, oi_dict, start_iid

def run(folder_path):
    pcd_path = join(join('/lab/tmpig10c/POST/', folder_path.split('/')[-3], folder_path.split('/')[-2]))
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
    instance = np.array([])
    oi_dict={}
    start_iid = 0
    for idx, t in enumerate(odo_time):
        pcd, diff = find_difference(pcd_time, t)
        if diff<3:
            pcd = tmp_pcd[pcd]
            tmp_points, tmp_intensity, tmp_objs, tmp_instance, old_points = convert(join(pcd_path, pcd, str(pcd)+'.pcd'), tmp_odo[t])
            tmp_instance, oi_dict, start_iid = update_instance(points, objs, instance, tmp_points, tmp_objs, tmp_instance, oi_dict, start_iid)
            points = tmp_points
            intensity = tmp_intensity
            objs = tmp_objs
            instance = tmp_instance
            print(pcd)
            os.makedirs(os.path.join('/lab/tmpig10c/CDATA', folder_path.split('/')[-3], folder_path.split('/')[-2], pcd), exist_ok=True)
            write_ply_point_cloud(join('/lab/tmpig10c/CDATA', folder_path.split('/')[-3], folder_path.split('/')[-2], pcd, pcd+'.pcd'), old_points, tmp_intensity, tmp_objs, tmp_instance.reshape(-1, 1))
            image_src = os.path.join(pcd_path, pcd, 'imgs.txt')
            if os.path.exists(image_src):
                image_dst = os.path.join('/lab/tmpig10c/CDATA', folder_path.split('/')[-3], folder_path.split('/')[-2], pcd, 'imgs.txt')
                shutil.copy(image_src, image_dst)
                print(image_dst)




if __name__ == '__main__':

    run('/lab/tmpig13b/kiran/bag_dump/2023_08_08/0/')
#25:0808
#23 0713
#22 0711
#14 0705
#15 0627
#20 0703