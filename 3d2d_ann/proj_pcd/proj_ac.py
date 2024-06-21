
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import torch
import open3d as o3d
import cv2
import pickle, os
import colorsys
from collections import Counter
#from undistort import *
from os.path import join
import argparse
import json
import shutil
import yaml, random
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth
import fcntl
parser = argparse.ArgumentParser()
parser.add_argument('--pcd', type=str)
parser.add_argument('--imgs', type=str)
parser.add_argument('--output', type=str)
args = parser.parse_args()



def write_ply_point_cloud(filename, points, intensities, proj_dict, label_idx, color_idx, label_inverse):

    res_objs = []
    res_intensities = []
    res_instance = []
    count=0

    pending_point = {}
    for idx, (point, intensity) in enumerate(zip(points, intensities)):
        point = tuple(point)
        if point in proj_dict.keys():
            obj = proj_dict[point]
            obj_len = len(set(sublist[2] for sublist in obj))
            obj = sorted(obj, key=lambda x: float(x[0][-5:-1]))[-1]
            obj_name = obj[0][:-6]
            instance_id = obj[1]
            if obj_name == '':
                obj_name = 'unlabeled'
                instance_id = -1
            else:
                if obj_len>1:
                    lb_name = [name[0][:-6] for name in proj_dict[point]]
                    if obj_name in lb_name[1:]:
                        if obj_name in pending_point.keys():
                            pending_point[obj_name].append(idx)
                        else:
                            pending_point[obj_name] = [idx]
        else:
            obj_name = 'unlabeled'
            instance_id = -1
        if obj_name == 'unlabeled':
            count+=1
        if obj_name in label_inverse:
            obj_idx = label_inverse[obj_name]
        else:
            with open('semantic.yaml', 'r+') as file:
                fcntl.flock(file, fcntl.LOCK_EX)
                data_loaded = yaml.safe_load(file)
                label_idx = data_loaded['labels']
                color_idx = data_loaded['color_map']
                label_inverse = {}
                for key,value in label_idx.items():
                    label_inverse[value] = key
                if obj_name in label_inverse:
                    obj_idx = label_inverse[obj_name]
                else:
                    obj_idx = max(label_idx.keys())+1
                    label_idx[obj_idx] = obj_name
                    label_inverse[obj_name] = obj_idx
                    color_idx[obj_idx] = generate_unique_rgb(color_idx)
                    data = {'labels':label_idx, 'color_map':color_idx}
                    yaml.dump(data, file, default_flow_style=False)
                fcntl.flock(file, fcntl.LOCK_UN)

        res_objs.append([obj_idx])
        res_intensities.append(intensity[0])
        res_instance.append([instance_id])
    res_instance = np.array(res_instance)
    for key,value in pending_point.items():
        tmp = points[value]
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(tmp)
        labels = np.array(point_cloud.cluster_dbscan(eps=1, min_points=4, print_progress=False))
        num_clusters = len(np.unique(labels)) - (1 if -1 in np.unique(labels) else 0)
        if num_clusters==1:
            res_instance[value] = res_instance[value[0]]

        # most_frequent_label = label_counts.most_common(1)[0][0]
        # points = tmp[np.where(labels == most_frequent_label)[0]]
        
        # bandwidth = estimate_bandwidth(tmp, quantile=0.6, n_samples=len(tmp))
        # if bandwidth <= 0:
        #     continue
        # ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        # ms.fit(tmp)

        # labels = ms.labels_
        # if len(np.unique(labels))==1:
        #     res_instance[value] = res_instance[value[0]]


    pcd = o3d.t.geometry.PointCloud()

    pcd.point["positions"] = o3d.core.Tensor(points)
    pcd.point["intensity"] = o3d.core.Tensor(intensities)
    pcd.point["obj_id"] = o3d.core.Tensor(res_objs)
    pcd.point["instance_id"] = o3d.core.Tensor(res_instance)
    o3d.t.io.write_point_cloud(filename, pcd, write_ascii=True)

    print((len(points)-count*1.0)/len(points))
    return label_idx, color_idx, label_inverse


def generate_unique_rgb(existing_colors):
    # existing_colors = set(existing_colors)
    while True:
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        if color not in existing_colors.values():
            return color

def proj(pcd, img_path, mask_path, proj_dict, instance_id):
    img = cv2.imread(img_path)
    cam_num = int(mask_path.split('/')[-1][3])
    print(img_path)
    CAMERA_MATRIX = np.array([[633.3955, 0, 638.5496],
                          [0, 633.1321, 373.7600],
                          [0, 0, 1]], dtype=np.float32)
    DIST_COEFFS = np.array([-0.0560, 0.0253, 0.0000, -0.000, 0.000000], dtype=np.float32)
    if cam_num == 1:
        R = np.array([[0.996972, -0.0722819, -0.0286596],
        [-0.030787, -0.0284948,  -0.999119],
        [0.0714016, 0.996978, -0.0306341]])
        t = np.array([0.0101957, -0.0118579, -0.0786262])
        CAMERA_MATRIX = np.array([[633.3955, 0, 638.5496],
                          [0, 633.1321, 373.7600],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0560, 0.0253, 0.0000, -0.000, 0.000000], dtype=np.float32)
    elif cam_num == 2:
        R = np.array([[0.364303, 0.930796, -0.0299967],
        [0.0221934, -0.0408783, -0.998917],
        [-0.931016, 0.363244, -0.0355499]])
        t = np.array([0.0220358, -0.00875454, -0.0944989])
        CAMERA_MATRIX = np.array([[630.8010, 0, 626.5921],
                          [0, 630.6018, 372.1486],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0610, 0.0708, 0.0000, -0.000, 0.000000], dtype=np.float32)
    elif cam_num == 3:
        R = np.array([[-0.850471, -0.525887, -0.0119176],
        [-0.00215739,0.026143,-0.999655],
        [0.0310208,-0.850153, -0.0233685]])
        t = np.array([0.153234, -0.0136081, -0.280648])
        CAMERA_MATRIX = np.array([[628.5559, 0, 644.4944],
                          [0, 627.9042, 371.4139],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0729, 0.1014, 0.0000, -0.000, 0.000000], dtype=np.float32)
    elif cam_num == 4:
        R = np.array([[-0.776079, 0.630406, -0.0171011],
        [0.00111168, -0.0257493, -0.999668],
        [-0.630636, -0.77584, 0.0192826]])
        t = np.array([-0.00934934, -0.0204035, -0.178968])
        CAMERA_MATRIX = np.array([[630.0727, 0, 642.9044],
                          [0, 629.5730, 360.8640],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0635, 0.0718, 0.0000, -0.000, 0.000000], dtype=np.float32)
    elif cam_num == 5:
        R = np.array([[0.25674, -0.966435, -0.00949949],
        [-0.0315747, 0.00143649, -0.9995],
        [0.965965,0.25691, -0.0301462]])
        t = np.array([-0.0663521, -0.0174611, 0.141484])
        CAMERA_MATRIX = np.array([[638.3315, 0, 639.1726],
                          [0, 638.1820, 366.2761],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0607, 0.0808, 0.0000, -0.000, 0.000000], dtype=np.float32)
    
        
    points3D = pcd
    forwards = np.dot(R, points3D.T).T + t.reshape(1,3)
    forwards = np.where((forwards[:, 2] > 0))[0]
    points2D, _ = cv2.projectPoints(points3D, R, t, CAMERA_MATRIX, DIST_COEFFS)
    
    masks = torch.load(join(mask_path, 'masks.pt'), map_location=torch.device('cpu'))
    with open(join(mask_path, 'labels'), 'rb') as f:
        label = pickle.load(f)
    assert (len(points2D)==len(points3D))
    points2D = points2D.astype(int)
    pixel_dict = {tuple(loc[0]): idx for idx, loc in enumerate(points2D)}
    for idx, mask in enumerate(masks):
        if len(label[idx])<=6:
            continue
        non_zero_indices = torch.nonzero(mask[0]).numpy()
        # coordinates = [(width.item(), height.item()) for height, width in non_zero_indices]
        # coordinates = zip(non_zero_indices[1], non_zero_indices[0])
        # points=[]
        tmp = []
        for i in range(len(non_zero_indices)):
            coordinate = (non_zero_indices[i][1], non_zero_indices[i][0])
            if coordinate in pixel_dict.keys():
                point3d = points3D[pixel_dict[coordinate]]
                tmp.append(point3d)
        tmp = np.array(tmp)
        if len(tmp) < 1:
            continue

        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(tmp)
        labels = np.array(point_cloud.cluster_dbscan(eps=8, min_points=1, print_progress=False))
        label_counts = Counter(labels)
        if -1 in label_counts:
            del label_counts[-1]
        if not label_counts:
            continue

        # bandwidth = estimate_bandwidth(tmp, quantile=0.8, n_samples=len(tmp))
        # if bandwidth <= 0:
        #     continue
        # ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        # ms.fit(tmp)

        # labels = ms.labels_

        most_frequent_label = label_counts.most_common(1)[0][0]
        points = tmp[np.where(labels == most_frequent_label)[0]]
        for point3d in points:
            if tuple(point3d) not in proj_dict.keys():
                proj_dict[tuple(point3d)] = [(label[idx], instance_id, cam_num)]
            else:
                proj_dict[tuple(point3d)].append((label[idx],instance_id, cam_num))
        instance_id+=1

            
    return proj_dict, instance_id


def find_closest_file(input_filename, reverse_sync):
    input_filename = input_filename[:-4]
    input_filename = input_filename.replace('.','')
    input_filename = int(input_filename)
    closest_filenames=[]
    for cam_sync in reverse_sync:
        closest_filename=None
        times = cam_sync.keys()
        closest_difference = 10**100
        for time in times:
            difference = abs(input_filename - time)
            if difference < closest_difference:
                closest_difference = difference
                closest_filename = cam_sync[time]
        closest_filenames.append(closest_filename)
    return closest_filenames


def run(folder_path):
    img_path = join(folder_path, 'all_imgs/')
    if not os.path.exists(img_path):
        print(f"Error: Folder '{folder_path}'img error.")
        return
    pcl_path = join(folder_path, 'all_pcl/')
    json_path = join(folder_path, 'sync_data.json')

    if not os.path.exists(json_path) or not os.path.exists(pcl_path):
        print(f"Error: Folder '{folder_path}'sync error.")
        return
    
    with open(json_path, "r") as json_file:
        sync_data = json.load(json_file)
    reverse_sync = []
    for tmp in sync_data:
        reverse_sync.append({value: key for key, value in tmp.items()})
    files = os.listdir(pcl_path)
    # files = ['1678561638.452518463.pcd']
    files.sort()
    print('start')
    pcd_img_dict = {}
    cam1_pcd_dict = {}
    for i, file_name in enumerate(files):
        five_imgs = find_closest_file(file_name, reverse_sync)
        pcd_img_dict[file_name] = ['' for q in range(5)]
        for v_img in five_imgs:
            camera, _ = v_img.split("_", 1)
            pcd_img_dict[file_name][int(camera[-1])-1] = v_img
            if int(camera[-1]) == 1:
                cam1_pcd_dict[v_img] = file_name
    print(folder_path.split('/'))
    SAM_path =  join(join('/lab/tmpig13c/henghui/SAM/', folder_path.split('/')[-3], folder_path.split('/')[-2]), 'NEW_SAM/')
    if not os.path.exists(SAM_path):
        print(f"Error: Folder '{folder_path}'SAM error.")
        return
    print(SAM_path)
    SAM_res = os.listdir(SAM_path)
    CAM1_res = [i for i in SAM_res if i[3]=='1']

    if os.path.exists('semantic.yaml'):
        with open('semantic.yaml', 'r') as file:
            data_loaded = yaml.safe_load(file)
            label_idx = data_loaded['labels']
            color_idx = data_loaded['color_map']
    else:
        label_idx = {0:"unlabeled"}
        color_idx = {0:[0,0,0]}
    label_inverse = {}
    for key,value in label_idx.items():
        label_inverse[value] = key

    for cam1 in CAM1_res[(len(CAM1_res)//3)*1:]:
        if cam1+'.jpg' not in cam1_pcd_dict.keys():
            continue
        pcd_name = cam1_pcd_dict[cam1+'.jpg']
        flag = 0
        for img_name in pcd_img_dict[pcd_name]:
            if not os.path.exists(join(SAM_path,img_name[:-4], 'grounded_sam_output.jpg')):
                flag = 1
                break
        if flag == 1:
            continue

        pcd = o3d.t.io.read_point_cloud(join(pcl_path, pcd_name))
        intensity = pcd.point.intensity.numpy()   
        pcd = pcd.point.positions.numpy()
        
        proj_dict = {}
        instance = 0
        for img_name in pcd_img_dict[pcd_name]:
            proj_dict, instance = proj(pcd, join(img_path, img_name), join(SAM_path, img_name[:-4]), proj_dict, instance)
        os.makedirs(join('/lab/tmpig13d/henghui/ins', pcd_name[:-4]), exist_ok=True)
        label_idx, color_idx, label_inverse = write_ply_point_cloud(join('/lab/tmpig13d/henghui/ins', pcd_name[:-4], pcd_name), pcd, intensity, proj_dict, label_idx, color_idx, label_inverse)
        for img_name in pcd_img_dict[pcd_name]:
            shutil.copy(join(img_path, img_name), join('/lab/tmpig13d/henghui/ins', pcd_name[:-4], img_name))

if __name__ == '__main__':
    run('/lab/tmpig13b/kiran/bag_dump/2023_03_11/0/')