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
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth
import copy
from scipy.spatial.distance import cdist

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

def convert(pcd,pose):
    pose = [float(i) for i in pose.split(',')]
    pcd = o3d.t.io.read_point_cloud(pcd)
    intensity = pcd.point.intensity.numpy()   
    objs = pcd.point.obj_id.numpy()
    instance_id = pcd.point.instance_id.numpy()
    pcd = pcd.point.positions.numpy()
    pcd = pcd[:, [1,2,0]]
    LiDAR_R = euler.euler2mat(pose[3], pose[4], pose[5], 'sxyz')
    LiDAR_T = np.array(pose[:3])
    pcd = np.dot(pcd,LiDAR_R.T)
    pcd = pcd + LiDAR_T
    return pcd, intensity, objs, instance_id

def update_instance(points, objs, instance, new_points, new_objs, new_instance, oi_dict, start_iid):
    new_objs = new_objs.squeeze()
    new_instance = new_instance.squeeze()
    if instance.size==0:
        assert start_iid==0
        instance = new_instance
        tmp_dict = {}
        for i in range(len(new_instance)):
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
                # print(len(exist_points.keys()))
                # print(len(add_points.keys()))
                for ex_instance, ex_points in exist_points.items():
                    for a_instance, a_points in add_points.items():
                        # if np.min(cdist(points[ex_points],new_points[a_points]))>0.8:
                        #     continue
                        tmp = concat_e(points[ex_points], new_points[a_points])
                        point_cloud = o3d.geometry.PointCloud()
                        point_cloud.points = o3d.utility.Vector3dVector(tmp)
                        labels = np.array(point_cloud.cluster_dbscan(eps=0.8, min_points=4, print_progress=True))

                        add_len = len(points)
                        num_clusters = len(np.unique(labels)) - (1 if -1 in np.unique(labels) else 0)
                        if num_clusters==1:
                            new_instance[a_points] = ex_instance
                            oi_dict[obj][ex_instance] += [add_len+i for i in a_points]
                        else:
                            oi_dict[obj][a_instance] = [add_len+i for i in a_points]
            else:
                add_len = len(points)
                for tmp_i, tmp_p in tmp_dict[obj].items():
                    oi_dict[obj] = {}
                    oi_dict[obj][tmp_i] = [add_len+i for i in tmp_p]
    return new_instance, oi_dict



def run(folder_path):
    pcd_path = join(join('/lab/tmpig13d/henghui/semantic_pcd/', folder_path.split('/')[-3], folder_path.split('/')[-2]))
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
    for idx, t in enumerate(odo_time):
        pcd, diff = find_difference(pcd_time, t)
        if diff<3:
            pcd = tmp_pcd[pcd]
            tmp_points, tmp_intensity, tmp_objs, tmp_instance = convert(join(pcd_path, pcd, str(pcd)+'.pcd'), tmp_odo[t])
            tmp_instance,oi_dict = update_instance(points, objs, instance, tmp_points, tmp_objs, tmp_instance, oi_dict)
            # points = concat_e(points, tmp_points)
            # intensity = concat_e(intensity, tmp_intensity)
            # objs = concat_e(objs, tmp_objs)
            # instance = concat_e(instance, tmp_instance)


    



if __name__ == '__main__':

    run('/lab/tmpig13b/kiran/bag_dump/2023_03_11/0/')
