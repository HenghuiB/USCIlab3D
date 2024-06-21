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
    with open('./semantic_res.yaml', 'r') as file:
        data_loaded = yaml.safe_load(file)
        label_idx = data_loaded['labels']
        color_idx = data_loaded['color_map']
    new_label_idx = {}
    with open('./merge.yaml', 'r') as file:
        data_loaded = yaml.safe_load(file)
        merge = data_loaded

    label_inverse = {}
    for key,value in label_idx.items():
        label_inverse[value] = key
    lb_map = {}
    for key, value in label_idx.items():
        if value in merge.keys():
            if merge[value] in label_idx.values():
                lb_map[key] = label_inverse[merge[value]]
    
    for date_folder in os.listdir(base_path):
        date_path = os.path.join(base_path, date_folder)
        if os.path.isdir(date_path):
            for session_folder in os.listdir(date_path):
                session_path = os.path.join(date_path, session_folder)
                if os.path.isdir(session_path):
                    new_label_idx = process_label_file(base_path, date_folder, session_folder, output_base_path, label_idx, lb_map, new_label_idx)

    with open('semantic.yaml', 'w') as file:
        data = {'labels':new_label_idx, 'color_map':color_idx}
        yaml.dump(data, file, default_flow_style=False)
def process_label_file(base_path, date_folder, session_folder, output_base_path, label_idx, lb_map, new_label_idx):
    folder_path = os.path.join(base_path, date_folder, session_folder)
    for pcd_folder in os.listdir(folder_path):
        pcd = os.path.join(folder_path, pcd_folder, pcd_folder+'.pcd')
        if not os.path.exists(pcd):
            print(pcd)
            print('not exist')
            continue
        pcd = o3d.t.io.read_point_cloud(pcd)
        intensity = pcd.point.intensity.numpy()   
        objs = pcd.point.obj_id.numpy()
        instance_id = pcd.point.instance_id.numpy()
        pcd = pcd.point.positions.numpy()
        objs = objs.squeeze()
        for i in range(len(objs)):
            if objs[i] in lb_map.keys():
                objs[i] = lb_map[objs[i]]
                if objs[i] not in new_label_idx.keys():
                    new_label_idx[int(objs[i])] = label_idx[objs[i]]
            else:
                if objs[i] not in new_label_idx.keys():
                    new_label_idx[int(objs[i])] = label_idx[objs[i]]
        # os.mkdirs(os.path.join('lab/tmpig10c/POST', date_folder, session_folder, pcd_folder), exist)
        os.makedirs(os.path.join('/lab/tmpig10c/POST', date_folder, session_folder, pcd_folder), exist_ok=True)
        write_ply_point_cloud(os.path.join('/lab/tmpig10c/POST', date_folder, session_folder, pcd_folder, pcd_folder+'.pcd'), pcd, intensity, objs.reshape(-1,1), instance_id)
        image_src = os.path.join(folder_path, pcd_folder, 'imgs.txt')
        image_dst = os.path.join('/lab/tmpig10c/POST', date_folder, session_folder, pcd_folder, 'imgs.txt')
        shutil.copy(image_src, image_dst)
    return new_label_idx


if __name__ == "__main__":
    base_path = '/lab/tmpig10c/post_res/'
    output_base_path = '/lab/tmpig10c/RES'
    process_files(base_path, output_base_path)
