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
import collections
from IPython import embed
import os

from os.path import join

BaseImage = collections.namedtuple(
    "Image", ["id", "qvec", "tvec", "camera_id", "name", "xys", "point3D_ids"])
def qvec2rotmat(qvec):
    return np.array([
        [1 - 2 * qvec[2]**2 - 2 * qvec[3]**2,
         2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3],
         2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2]],
        [2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3],
         1 - 2 * qvec[1]**2 - 2 * qvec[3]**2,
         2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1]],
        [2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2],
         2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1],
         1 - 2 * qvec[1]**2 - 2 * qvec[2]**2]])

class Image(BaseImage):
    def qvec2rotmat(self):
        return qvec2rotmat(self.qvec)
    

def read_points3D_text(path):
    """
    see: src/base/reconstruction.cc
        void Reconstruction::ReadPoints3DText(const std::string& path)
        void Reconstruction::WritePoints3DText(const std::string& path)
    """
    xyzs = None
    rgbs = None
    errors = None
    num_points = 0
    with open(path, "r") as fid:
        while True:
            line = fid.readline()
            if not line:
                break
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                num_points += 1

    res={}
    xyzs = np.empty((num_points, 3))
    rgbs = np.empty((num_points, 3))
    errors = np.empty((num_points, 1))
    count = 0
    with open(path, "r") as fid:
        while True:
            line = fid.readline()
            if not line:
                break
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                elems = line.split()
                xyz = np.array(tuple(map(float, elems[1:4])))
                rgb = np.array(tuple(map(int, elems[4:7])))
                error = np.array(float(elems[7]))
                res[int(elems[0])] = list(map(float, elems[1:4])) +[0,0,0]
                xyzs[count] = xyz
                rgbs[count] = rgb
                errors[count] = error
                count += 1

    return xyzs, rgbs, errors, res


def write_ply_point_cloud(filename, points):
    header = '''ply
format ascii 1.0
element vertex {}
property float x
property float y
property float z
'''.format(len(points))

    header += '''property uchar red
property uchar green
property uchar blue
'''
    header += '''end_header
'''

    with open(filename, 'w') as f:
        f.write(header)
        for point in points:
            f.write('{} {} {} {} {} {}\n'.format(point[0], point[1], point[2], point[3], point[4], point[5]))


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


def read_extrinsics_text(path):
    images = {}
    with open(path, "r") as fid:
        while True:
            line = fid.readline()
            if not line:
                break
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                elems = line.split()
                image_id = int(elems[0])
                qvec = np.array(tuple(map(float, elems[1:5])))
                tvec = np.array(tuple(map(float, elems[5:8])))
                camera_id = int(elems[8])
                image_name = elems[9]
                elems = fid.readline().split()
                xys = np.column_stack([tuple(map(float, elems[0::3])),
                                       tuple(map(float, elems[1::3]))])
                point3D_ids = np.array(tuple(map(int, elems[2::3])))
                images[image_id] = Image(
                    id=image_id, qvec=qvec, tvec=tvec,
                    camera_id=camera_id, name=image_name,
                    xys=xys, point3D_ids=point3D_ids)
    return images




def proj(points, mask_f, res, label_proj, color_label, hist):



    masks = torch.load(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/res/', mask_f), 'masks.pt')).cpu().numpy()
    with open(join(join('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/res/', mask_f), 'labels'), 'rb') as f:
        label = pickle.load(f)
    if mask_f not in points.keys():
        return res
    tmp = {}
    for mask in range(masks.shape[0]):
        indices = np.argwhere(masks[mask] == 1)
        pixels_with_value_1 = [(x, y) for _, x, y in indices]
        for pixel in pixels_with_value_1:
            if (pixel[1],pixel[0]) in tmp.keys():
                tmp[(pixel[1],pixel[0])]+=[label[mask]]
            else:
                tmp[(pixel[1],pixel[0])]=[label[mask]]
    pixels = {}
    for o_key,o_value in tmp.items():
        obj = sorted(o_value, key=lambda x: float(x[-5:-1]))[-1]
        pixels[o_key[0], o_key[1]] = obj[:-6]

    for idx in range(points[mask_f][0].shape[0]):
        point = points[mask_f][0][idx]
        id_3d = points[mask_f][1][idx]
        pixel = (round(point[1]), round(point[0])) 
        if pixel in pixels.keys():
            if id_3d in hist.keys():
                hist[id_3d].append(pixels[pixel])
            else:
                hist[id_3d] = [pixels[pixel]]
    return hist
    
    # for idx in range(points[mask_f][0].shape[0]):
    #     point = points[mask_f][0][idx]
    #     id_3d = points[mask_f][1][idx]
    #     pixel = (round(point[0]), round(point[1]))
    #     pixel_lebel=-1
    #     if id_3d == -1:
    #         continue
    #     for mask in range(masks.shape[0]):
    #         if masks[mask, 0, pixel[1], pixel[0]]:
    #             pixel_lebel = mask
    #             break
    #     if pixel_lebel != -1:
    #         res[id_3d][3:] = color_label[label_proj[mask_f][pixel_lebel]]


    return res

if __name__ == '__main__':
    cam_extrinsics = read_extrinsics_text('./images.txt')
    xyzs, rgbs, errors, res = read_points3D_text('./points3D.txt')

    with open('labels_proj', 'rb') as f:
        label_proj = pickle.load(f)
    color_label = generate_unique_colors(max(max(sublist) for sublist in label_proj.values())+1)

    points2d=[0 for i in range(5)]
    points2d = {}
    for _,value in cam_extrinsics.items():
        points2d[value.name[:-4]] = [value.xys, value.point3D_ids]
    # for _,value in cam_extrinsics.items():
    #     if value.name=='cam1_1687658166985010525.jpg':
    #         points2d[0] = [value.xys, value.point3D_ids]
    #     elif value.name=='cam2_1687658166982492271.jpg':
    #         points2d[1] = [value.xys, value.point3D_ids]
    #     elif value.name=='cam3_1687658166983268403.jpg':
    #         points2d[2] = [value.xys, value.point3D_ids]
    #     elif value.name=='cam4_1687658166981114215.jpg':
    #         points2d[3] = [value.xys, value.point3D_ids]
    #     elif value.name=='cam5_1687658166993004507.jpg':
    #         points2d[4] = [value.xys, value.point3D_ids]

    # print(color_label)
    hist = {}
    for mask_f in os.listdir('/lab/tmpig10c/kiran/Grounded-Segment-Anything/outputs/res/'):
        print(mask_f)
        hist = proj(points2d, mask_f, res, label_proj, color_label, hist)
    print(hist)
    with open('lf.pkl', 'wb') as f:
        pickle.dump(hist, f)
    # res = proj(points2d, 0, res, label_proj, color_label)
    # res = proj(points2d, 1, res, label_proj, color_label)
    # res = proj(points2d, 2, res, label_proj, color_label)
    # res = proj(points2d, 3, res, label_proj, color_label)
    # res = proj(points2d, 4, res, label_proj, color_label)
    # write_ply_point_cloud('point_cloud__.ply', res.values())
    # print(res)
    # for point, obj in proj_dict.items():
    #     if len(obj) == 1:
    #         obj = obj[0]
    #         # print(obj[0], color_label[obj[0]])
    #         # print(obj[1], color_label[obj[0][obj[1]]])
    #         colors[point] = np.array(color_label[label_proj[obj[0]][obj[1]]])
    #     else:
    #         tmp_vote = []
    #         for c in obj:
    #             tmp_vote.append(color_label[label_proj[c[0]][c[1]]])
    #         colors[point] = np.array(most_frequent(tmp_vote))
            
    # points_xyz = hits_body[:3, :].T
    # write_ply_point_cloud('point_cloud_.ply', points_xyz, colors.astype(int))
