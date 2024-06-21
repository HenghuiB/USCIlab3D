# !/usr/bin/python
#
# Demonstrates how to project velodyne points to camera imagery. Requires a binary
# velodyne sync file, undistorted image, and assumes that the calibration files are
# in the directory.
#
# To use:
#
#    python project_vel_to_cam.py vel img cam_num
#
#       vel:  The velodyne binary file (timestamp.bin)
#       img:  The undistorted image (timestamp.tiff)
#   cam_num:  The index (0 through 5) of the camera
#
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


CAMERA_MATRIX = np.array([[633.3955, 0, 638.5496],
                          [0, 633.1321, 373.7600],
                          [0, 0, 1]], dtype=np.float32)

DIST_COEFFS = np.array([-0.0560, 0.0253, 0.0000, -0.000, 0.000000], dtype=np.float32)

def write_ply_point_cloud(filename, points, colors=None):
    header = '''ply
format ascii 1.0
element vertex {}
property float x
property float y
property float z
'''.format(len(points))

    if colors is not None:
        header += '''property uchar red
property uchar green
property uchar blue
'''
    header += '''end_header
'''

    with open(filename, 'w') as f:
        f.write(header)
        if colors is not None:
            for point, color in zip(points, colors):
                f.write('{} {} {} {} {} {}\n'.format(point[0], point[1], point[2], color[0], color[1], color[2]))
        else:
            for point in points:
                f.write('{} {} {}\n'.format(point[0], point[1], point[2]))

def generate_unique_colors(num_colors):
    colors = set()
    while len(colors) < num_colors:
        # Generate random hue, saturation, and lightness
        hue = random.random()
        saturation = random.uniform(0.5, 1.0)  # Adjust saturation to avoid dull colors
        lightness = random.uniform(0.4, 0.6)  # Adjust lightness to avoid overly dark or bright colors
        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        # Scale RGB values to 0-255
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        colors.add((r, g, b))
    return list(colors)


def most_frequent(lst):
    counts = Counter(lst)
    max_count = max(counts.values())
    most_common = [key for key, value in counts.items() if value == max_count]
    return random.choice(most_common)




def proj(pcd, img_path, mask, proj_dict):
    img = cv2.imread(img_path)
    cam_num = int(mask[3])
    print(img_path)
    if cam_num == 1:
        R = np.array([[0.997787, -0.0603672, -0.0278649],
        [-0.0302716, -0.0393293, -0.998767],
        [0.0591969, 0.997402, -0.0410699]])
        t = np.array([-0.0225125, 0.162101, -0.178768])
    elif cam_num == 2:
        R = np.array([[0.374325,0.926928,-0.0261801],
        [0.032223,-0.0412179,-0.99863],
        [-0.926738, 0.372969, -0.0452975]])
        t = np.array([-0.0220061, 0.162078, -0.178564])
    elif cam_num == 3:
        R = np.array([[-0.846798,-0.531271,-0.0261801],
        [-0.00192764,0.0522831,-0.99863],
        [0.531912, -0.845588, -0.0452975]])
        t = np.array([0.153234, 0.168518, -0.421818])
    elif cam_num == 4:
        R = np.array([[-0.780203,0.624979,-0.0261801],
        [0.048741, 0.0190146, -0.99863],
        [-0.623625,-0.780411, -0.0452975]])
        t = np.array([-0.100335, 0.167401, -0.25064])
    elif cam_num == 5:
        R = np.array([[0.25608, -0.966302, -0.0261801],
        [-0.0505004, 0.0136728, -0.99863],
        [0.965336, 0.257051,-0.0452975]])
        t = np.array([-0.0337689, 0.160828, -0.144208])
    
        
    points3D = pcd
    forwards = np.dot(R, points3D.T).T + t.reshape(1,3)
    # points3D = points3D[points3D[:,2]>0]
    forwards = np.where((forwards[:, 2] > 0))[0]
    # print(points3D.shape)
    points2D, _ = cv2.projectPoints(points3D, R, t, CAMERA_MATRIX, DIST_COEFFS)
    
    # masks = torch.load('/'.join(img_path.split('/')[:-1]) + '/masks.pt')
    masks = torch.load(f'./data/{mask}' + '/masks.pt')
    with open(join(join('./data/', mask), 'labels'), 'rb') as f:
        label = pickle.load(f)
    for index, (point2d, point3d) in enumerate(zip(points2D, points3D)):
        if (index in forwards) & (point2d[:, 0] >= 0) & (point2d[:, 1] >= 0) & \
        (point2d[:, 0] < img.shape[1]) & (point2d[:, 1] < img.shape[0]):
            for mask in range(masks.shape[0]):
                if masks[mask, 0, point2d[0][1].astype(int), point2d[0][0].astype(int)]:
                    if tuple(point3d) not in proj_dict.keys():
                        proj_dict[tuple(point3d)] = [label[mask]]
                    else:
                        proj_dict[tuple(point3d)].append(label[mask])





    return proj_dict

if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud('./data/1687658158.585821629.pcd')
    pcd = np.asarray(pcd.points)

    colors = np.zeros((pcd.shape[0], 3))
    with open('labels_proj', 'rb') as f:
        label_proj = pickle.load(f)
    # color_label = generate_unique_colors(max(max(sublist) for sublist in label_proj.values())+1)
    color_label = generate_unique_colors(100)

    proj_dict = {}

    proj_dict = proj(pcd, './data/cam1_1687658158576471586.jpg', 'cam1_dense', proj_dict)
    proj_dict = proj(pcd, './data/cam2_1687658158698299126.jpg', 'cam2_dense', proj_dict)
    proj_dict = proj(pcd, './data/cam3_1687658158598990500.jpg', 'cam3_dense', proj_dict)
    proj_dict = proj(pcd, './data/cam4_1678271610326525362.jpg', 'cam4_dense', proj_dict)
    proj_dict = proj(pcd, './data/cam5_1687658159795117737.jpg', 'cam5_dense', proj_dict)

    color_path = 'obj_color_index.pkl'
    if os.path.exists(color_path):
        with open(color_path, 'rb') as f:
            color_dict = pickle.load(f)
    else:
        color_dict = {'MAX_INDEX':0}

    co_path = 'color_obj.pkl'
    if os.path.exists(co_path):
        with open(co_path, 'rb') as f:
            co_dict = pickle.load(f)
    else:
        co_dict = {}


    for point, obj in proj_dict.items():
        obj = sorted(obj, key=lambda x: float(x[-5:-1]))[-1][:-6]
        if obj not in color_dict.keys():
            color_dict[obj] = color_dict['MAX_INDEX']
            c = color_dict['MAX_INDEX']
            color_dict['MAX_INDEX'] +=1
        else:
            c = color_dict[obj]
        colors[np.where((pcd == point).all(axis=1))[0][0]] = np.array(color_label[c])
        co_dict[obj] = np.array(color_label[c])
        # if len(obj) == 1:
        #     obj = obj[0]
        #     # print(obj[0], color_label[obj[0]])
        #     # print(obj[1], color_label[obj[0][obj[1]]])
        #     colors[np.where((pcd == point).all(axis=1))[0][0]] = np.array(color_label[label_proj[obj[0]][obj[1]]])

        # else:
        #     tmp_vote = []
        #     for c in obj:
        #         tmp_vote.append(color_label[label_proj[c[0]][c[1]]])
        #     colors[point] = np.array(most_frequent(tmp_vote))
            
    # points_xyz = pcd[:3, :].T
    with open(color_path, 'wb') as f:
        pickle.dump(color_dict, f)
    with open(co_path, 'wb') as f:
        pickle.dump(co_dict, f)
    write_ply_point_cloud('point_cloud_dense.ply', pcd, colors.astype(int))
