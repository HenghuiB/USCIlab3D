

import numpy as np
import open3d as o3d
import pickle, os

from os.path import join
import argparse
import yaml, random
parser = argparse.ArgumentParser()
parser.add_argument('--pcd', type=str)
parser.add_argument('--output', type=str)
args = parser.parse_args()


def write_ply_point_cloud(filename, points, objs, color_idx):
    res_colors = []
    for obj in objs:
        color = color_idx[obj[0]]
        res_colors.append(color)
    # pcd = o3d.t.geometry.PointCloud()
    # pcd.point["positions"] = o3d.core.Tensor(points)
    # # pcd.point["colors"] = o3d.core.Tensor(res_colors)
    # o3d.t.io.write_point_cloud(filename, pcd)
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(np.array(res_colors).astype(np.float64) / 255.0)
    o3d.io.write_point_cloud(filename, point_cloud, write_ascii=True)

def run(folder_path,output_path):

    with open('semantic.yaml', 'r') as file:
        data_loaded = yaml.safe_load(file)
        color_idx = data_loaded['color_map']

    pcds = os.listdir(folder_path)
    for pcd_name in pcds:
        pcd_path = (join(folder_path, pcd_name, pcd_name+'.pcd'))
        pcd = o3d.t.io.read_point_cloud(pcd_path)
        objs = pcd.point.obj_id.numpy() 
        pcd = pcd.point.positions.numpy()
        write_ply_point_cloud(join(output_path, pcd_name+'.ply'), pcd, objs, color_idx)
        
        

if __name__ == '__main__':
    run('/lab/tmpig10c/CDATA/2023_07_13/0/', '/lab/tmpig13d/henghui/test2/')