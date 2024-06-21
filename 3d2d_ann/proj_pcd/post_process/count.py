import os
import shutil
import random
import subprocess
import open3d as o3d
import yaml


def write_ply_point_cloud(filename, points, intensities, objs, instance):

    pcd = o3d.t.geometry.PointCloud()
    pcd.point["positions"] = o3d.core.Tensor(points)
    pcd.point["intensity"] = o3d.core.Tensor(intensities)
    pcd.point["obj_id"] = o3d.core.Tensor(objs)
    pcd.point["instance_id"] = o3d.core.Tensor(instance)
    o3d.t.io.write_point_cloud(filename, pcd, write_ascii=True)

def process_files(base_path, output_base_path):
    pcd_fre = {}
    pt_fre = {}
    for date_folder in os.listdir(base_path):
        date_path = os.path.join(base_path, date_folder)
        if os.path.isdir(date_path):
            for session_folder in os.listdir(date_path):
                session_path = os.path.join(date_path, session_folder)
                if os.path.isdir(session_path):
                    print(date_folder)
                    pcd_fre, pt_fre = process_label_file(base_path, date_folder, session_folder, pcd_fre, pt_fre)

    with open('fre.yaml', 'w') as file:
        data = {'pcd':pcd_fre, 'point':pt_fre}
        yaml.dump(data, file, default_flow_style=False)
def process_label_file(base_path, date_folder, session_folder, pcd_fre, pt_fre):
    folder_path = os.path.join(base_path, date_folder, session_folder)
    for pcd_folder in os.listdir(folder_path):
        pcd = os.path.join(folder_path, pcd_folder, pcd_folder+'.pcd')
        pcd = o3d.t.io.read_point_cloud(pcd)
        objs = pcd.point.obj_id.numpy()
        objs = objs.squeeze()
        tmp = {}
        for i in objs:
            if int(i) not in tmp.keys():
                tmp[int(i)] = 1
            if int(i) not in pt_fre.keys():
                pt_fre[int(i)] = 1
            else:
                pt_fre[int(i)] +=1
        for i in tmp.keys():
            if int(i) not in pcd_fre.keys():
                pcd_fre[int(i)] = 1
            else:
                pcd_fre[int(i)] += 1
            
    return pcd_fre, pt_fre


if __name__ == "__main__":
    base_path = '/lab/tmpig10c/CDATA/'
    output_base_path = '/lab/tmpig10c/RES'
    process_files(base_path, output_base_path)
