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
import pickle
import colorsys
from collections import Counter
#from undistort import *


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

def convert(x_s, y_s, z_s):

    scaling = 0.005 # 5 mm
    offset = -100.0

    x = x_s * scaling + offset
    y = y_s * scaling + offset
    z = z_s * scaling + offset

    return x, y, z

def load_vel_hits(filename):

    f_bin = open(filename, "rb")

    hits = []

    while True:

        x_str = f_bin.read(2)
        if x_str == b'': # eof
            break
        x = struct.unpack('<H', x_str)[0]
        y = struct.unpack('<H', f_bin.read(2))[0]
        z = struct.unpack('<H', f_bin.read(2))[0]
        i = struct.unpack('B', f_bin.read(1))[0]
        l = struct.unpack('B', f_bin.read(1))[0]

        x, y, z = convert(x, y, z)

        # Load in homogenous
        hits += [[x, y, z, 1]]

    f_bin.close()
    hits = np.asarray(hits)
    return hits.transpose()

def ssc_to_homo(ssc):

    # Convert 6-DOF ssc coordinate transformation to 4x4 homogeneous matrix
    # transformation

    sr = np.sin(np.pi/180.0 * ssc[3])
    cr = np.cos(np.pi/180.0 * ssc[3])

    sp = np.sin(np.pi/180.0 * ssc[4])
    cp = np.cos(np.pi/180.0 * ssc[4])

    sh = np.sin(np.pi/180.0 * ssc[5])
    ch = np.cos(np.pi/180.0 * ssc[5])

    H = np.zeros((4, 4))

    H[0, 0] = ch*cp
    H[0, 1] = -sh*cr + ch*sp*sr
    H[0, 2] = sh*sr + ch*sp*cr
    H[1, 0] = sh*cp
    H[1, 1] = ch*cr + sh*sp*sr
    H[1, 2] = -ch*sr + sh*sp*cr
    H[2, 0] = -sp
    H[2, 1] = cp*sr
    H[2, 2] = cp*cr

    H[0, 3] = ssc[0]
    H[1, 3] = ssc[1]
    H[2, 3] = ssc[2]

    H[3, 3] = 1

    return H

def project_vel_to_cam(hits, cam_num):

    # Load camera parameters
    K = np.loadtxt('./data/lt_dataset/K_cam%d.csv' % (cam_num), delimiter=',')
    x_lb3_c = np.loadtxt('./data/lt_dataset/x_lb3_c%d.csv' % (cam_num), delimiter=',')

    # Other coordinate transforms we need
    x_body_lb3 = [0.035, 0.002, -1.23, -179.93, -0.23, 0.50]

    # Now do the projection
    T_lb3_c = ssc_to_homo(x_lb3_c)
    T_body_lb3 = ssc_to_homo(x_body_lb3)

    T_lb3_body = np.linalg.inv(T_body_lb3)
    T_c_lb3 = np.linalg.inv(T_lb3_c)

    T_c_body = np.matmul(T_c_lb3, T_lb3_body)

    hits_c = np.matmul(T_c_body, hits)
    hits_im = np.matmul(K, hits_c[0:3, :])
    return hits_im

def proj(hits_body, img, cam_num, proj_dict):


    # Load velodyne points
    

    # Load image
    image = mpimg.imread(img)

    masks = torch.load('/'.join(img.split('/')[:-1]) + '/masks.pt')

    cam_num = int(cam_num)

    hits_image = project_vel_to_cam(hits_body, cam_num)

    x_im = hits_image[0, :]/hits_image[2, :]
    y_im = hits_image[1, :]/hits_image[2, :]
    z_im = hits_image[2, :]

    # idx_infront = z_im>0
    # x_im = x_im[idx_infront]
    # y_im = y_im[idx_infront]
    # z_im = z_im[idx_infront]

    indices = np.where((x_im > 0) & (x_im < 1616) & (y_im > 0) & (y_im < 1232) & (z_im>0))[0]
    for point in indices:
        pixel = (round(x_im[point]), round(y_im[point]))
        if pixel[1]>=1232:
            pixel=(pixel[0],1231)
        if pixel[0]>=1616:
            pixel=(1615, pixel[1])
        pixel_lebel=-1
        for mask in range(masks.shape[0]):
            # print(masks[mask, 0])
            # condition = masks[mask, 0] == True
            # true_indices = torch.nonzero(condition)
            # print(true_indices.shape)
            # print(mask)
            # condition = masks[1, 0] == True
            # true_indices = torch.nonzero(condition)
            # print(true_indices.shape)
            # print(masks[mask, 0, pixel[1], pixel[0]])
            if masks[mask, 0, pixel[1], pixel[0]]:
                pixel_lebel = mask
                break
        if pixel_lebel != -1:

            if pixel not in proj_dict.keys():
                proj_dict[point] = [(cam_num, pixel_lebel)]
            else:
                proj_dict[point].append((cam_num, pixel_lebel))
    # print(len(indices))
    # plt.figure(1)
    # plt.imshow(image)
    # plt.scatter(x_im, y_im, c=z_im, s=5, linewidths=0)
    # plt.xlim(0, 1616)
    # plt.ylim(0, 1232)
    # plt.savefig('res.png')
    # plt.show()

    return proj_dict

if __name__ == '__main__':
    hits_body = load_vel_hits(sys.argv[1])
    colors = np.zeros((hits_body.shape[1], 3))
    with open('labels_proj', 'rb') as f:
        label_proj = pickle.load(f)
    color_label = generate_unique_colors(max(max(sublist) for sublist in label_proj)+1)
    print(color_label)
    proj_dict = {}
    proj_dict = proj(hits_body, './data/lt_dataset/lb3/Cam0/1326036598034801.tiff', 0, proj_dict)
    proj_dict = proj(hits_body, './data/lt_dataset/lb3/Cam1/1326036598034801.tiff', 1, proj_dict)
    proj_dict = proj(hits_body, './data/lt_dataset/lb3/Cam2/1326036598034801.tiff', 2, proj_dict)
    proj_dict = proj(hits_body, './data/lt_dataset/lb3/Cam3/1326036598034801.tiff', 3, proj_dict)
    proj_dict = proj(hits_body, './data/lt_dataset/lb3/Cam4/1326036598034801.tiff', 4, proj_dict)
    proj_dict = proj(hits_body, './data/lt_dataset/lb3/Cam5/1326036598034801.tiff', 5, proj_dict)

    for point, obj in proj_dict.items():
        if len(obj) == 1:
            obj = obj[0]
            # print(obj[0], color_label[obj[0]])
            # print(obj[1], color_label[obj[0][obj[1]]])
            colors[point] = np.array(color_label[label_proj[obj[0]][obj[1]]])
        else:
            tmp_vote = []
            for c in obj:
                tmp_vote.append(color_label[label_proj[c[0]][c[1]]])
            colors[point] = np.array(most_frequent(tmp_vote))
            
    points_xyz = hits_body[:3, :].T
    write_ply_point_cloud('point_cloud_.ply', points_xyz, colors.astype(int))
