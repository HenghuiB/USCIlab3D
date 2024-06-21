
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
import argparse
import pickle
import bisect

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
            with open('semantic_res.yaml', 'r+') as file:
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
                    file.seek(0)
                    file.truncate()
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



    pcd = o3d.t.geometry.PointCloud()

    pcd.point["positions"] = o3d.core.Tensor(points)
    pcd.point["intensity"] = o3d.core.Tensor(intensities)
    pcd.point["obj_id"] = o3d.core.Tensor(res_objs)
    pcd.point["instance_id"] = o3d.core.Tensor(res_instance)
    o3d.t.io.write_point_cloud(filename, pcd, write_ascii=True)

    print((len(points)-count*1.0)/len(points))
    return label_idx, color_idx, label_inverse


def generate_unique_rgb(existing_colors):
    while True:
        color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        if color not in existing_colors.values():
            return color

def proj(pcd, img_path, mask_path, proj_dict, instance_id, date, session, ex_dict):
    img = cv2.imread(img_path)
    cam_num = int(mask_path.split('/')[-1][3])
    print(img_path)
    Tr = ex_dict[date][session]['cam'+str(cam_num)]
    R = Tr[:3, :3]
    t = Tr[:3, 3]
    if cam_num == 1:
        CAMERA_MATRIX = np.array([[641.5821, 0, 634.7323],
                          [0, 641.0116, 366.3152],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0610, 0.0587, 0.0000, -0.000, 0.000000], dtype=np.float32)
    elif cam_num == 2:
        CAMERA_MATRIX = np.array([[653.7005, 0, 624.2886],
                          [0, 653.1886, 374.0093],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0303, 0.0774, 0.0000, -0.000, 0.000000], dtype=np.float32)
    elif cam_num == 3:
        CAMERA_MATRIX = np.array([[647.6335, 0, 641.4748],
                          [0, 647.0084, 374.8375],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0404, 0.0596, 0.0000, -0.000, 0.000000], dtype=np.float32)
    elif cam_num == 4:
        CAMERA_MATRIX = np.array([[666.9982, 0, 641.2684],
                          [0, 665.5787, 367.7312],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0155, 0.1116, 0.0000, -0.000, 0.000000], dtype=np.float32)
    elif cam_num == 5:
        CAMERA_MATRIX = np.array([[649.4308, 0, 639.5211],
                          [0, 648.6708, 366.2651],
                          [0, 0, 1]], dtype=np.float32)
        DIST_COEFFS = np.array([-0.0445, 0.0685, 0.0000, -0.000, 0.000000], dtype=np.float32)
    
        
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


def run(date, session, data_path, curr, total):
    folder_path = join('/lab/tmpig13b/kiran/bag_dump/', date, session)
    img_path = join('/lab/tmpig21d/u/henghui/bag_dump/', date, session, 'all_imgs/')
    odo_path = join(folder_path,'all_odom', 'odometry.txt')
    with open(odo_path, 'r') as f:
        odo = f.read().splitlines() 
    odo_time = [int(i.split()[-1].replace('.','')) for i in odo]
    odo_time.sort()
    if not os.path.exists(img_path):
        print(f"Error: Folder '{folder_path}'img error.")
        return
    pcd_path = join(folder_path, 'all_pcl/')
    pcds = os.listdir(pcd_path)
    pcd_time = [int(i[:-7].replace('.','')) for i in pcds]
    tmp_pcd = dict(zip(pcd_time, pcds))
    pcd_time.sort()
    json_path = join(folder_path, 'sync_data.json')

    if not os.path.exists(json_path) or not os.path.exists(pcd_path):
        print(f"Error: Folder '{folder_path}'sync error.")
        return
    with open('./extrinsic', 'rb') as file:
        ex_dict = pickle.load(file)
    with open(json_path, "r") as json_file:
        sync_data = json.load(json_file)
    reverse_sync = []
    for tmp in sync_data:
        reverse_sync.append({value: key for key, value in tmp.items()})

    pcd_img_dict = {}
    cam1_pcd_dict = {}
    for idx, t in enumerate(odo_time):
        pcd, diff = find_difference(pcd_time, t)
        if diff>2:
            continue
        file_name = tmp_pcd[pcd]
        five_imgs = find_closest_file(file_name, reverse_sync)
        pcd_img_dict[file_name] = ['' for q in range(5)]
        for v_img in five_imgs:
            camera, _ = v_img.split("_", 1)
            pcd_img_dict[file_name][int(camera[-1])-1] = v_img
            if int(camera[-1]) == 1:
                cam1_pcd_dict[v_img] = file_name
    print(folder_path.split('/'))
    SAM_path =  join(data_path, date, session, 'NEW_SAM/')
    if not os.path.exists(SAM_path):
        print(f"Error: Folder '{folder_path}'SAM error.")
        return
    print(SAM_path)
    SAM_res = os.listdir(SAM_path)
    CAM1_res = [i for i in SAM_res if i[3]=='1']

    if os.path.exists('semantic_res.yaml'):
        with open('semantic_res.yaml', 'r') as file:
            data_loaded = yaml.safe_load(file)
            label_idx = data_loaded['labels']
            color_idx = data_loaded['color_map']
    else:
        label_idx = {0:"unlabeled"}
        color_idx = {0:[0,0,0]}
    label_inverse = {}
    for key,value in label_idx.items():
        label_inverse[value] = key

    total_length = len(CAM1_res)
    part_length = total_length // total
    start_index = (curr - 1) * part_length
    end_index = curr * part_length if curr < total else total_length


    for cam1 in CAM1_res[start_index:end_index]:
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

        pcd = o3d.t.io.read_point_cloud(join(pcd_path, pcd_name))
        intensity = pcd.point.intensity.numpy()   
        pcd = pcd.point.positions.numpy()
        
        proj_dict = {}
        instance = 0
        
        if os.path.exists(join('/lab/tmpig10c/odo_res', date, session, pcd_name[:-4], pcd_name)):
            continue
        if os.path.exists(join('/lab/tmpig10c/data_res', date, session, pcd_name[:-4], pcd_name)):
            os.makedirs(join('/lab/tmpig10c/odo_res', date, session), exist_ok=True)
            shutil.copytree(join('/lab/tmpig10c/data_res', date, session, pcd_name[:-4]), join('/lab/tmpig10c/odo_res', date, session, pcd_name[:-4]))
            continue

        for img_name in pcd_img_dict[pcd_name]:
            proj_dict, instance = proj(pcd, join(img_path, img_name), join(SAM_path, img_name[:-4]), proj_dict, instance, date, session, ex_dict)
        os.makedirs(join('/lab/tmpig10c/odo_res', date, session, pcd_name[:-4]), exist_ok=True)
        label_idx, color_idx, label_inverse = write_ply_point_cloud(join('/lab/tmpig10c/odo_res', date, session, pcd_name[:-4], pcd_name), pcd, intensity, proj_dict, label_idx, color_idx, label_inverse)
        with open(join('/lab/tmpig10c/odo_res', date, session, pcd_name[:-4], 'imgs.txt'), 'w') as imagef:
            for img_name in pcd_img_dict[pcd_name]:
                imagef.write(img_name)
                imagef.write('\n')
                # shutil.copy(join(img_path, img_name), join('/lab/tmpig10c/data_res', date, session, pcd_name[:-4], img_name))

if __name__ == '__main__':
    # run('/lab/tmpig13b/kiran/bag_dump/2023_03_11/0/')
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=str)
    parser.add_argument('--session', type=str)
    parser.add_argument('--data_path', type=str)
    parser.add_argument('--curr', type=int)
    parser.add_argument('--total', type=int)
    args = parser.parse_args()
    # run('2023_03_11', '0', '/lab/tmpig13c/henghui/SAM/', curr, )
    run(args.date, args.session, args.data_path, args.curr, args.total)