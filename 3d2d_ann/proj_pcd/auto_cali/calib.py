import os
import shutil
import random
import subprocess

def process_files(base_path, output_base_path):
    for date_folder in os.listdir(base_path):
        date_path = os.path.join(base_path, date_folder)
        if os.path.isdir(date_path):
            for session_folder in os.listdir(date_path):
                session_path = os.path.join(date_path, session_folder)
                if os.path.isdir(session_path):
                    process_label_file(base_path, date_folder, session_folder, output_base_path)

def process_label_file(base_path, date_folder, session_folder, output_base_path):

    for cam in range(0,5):
        cam_folder = os.path.join(base_path, date_folder, session_folder, 'cam'+str(cam+1))
        max_folder=''
        max_file=-1
        for bag_folder in os.listdir(cam_folder):
            if not os.path.exists(os.path.join(cam_folder, bag_folder, 'masks', 'calib')):
                print(os.path.join(cam_folder, bag_folder, 'masks', 'calib'))
                return 0
            if len(os.listdir(os.path.join(cam_folder, bag_folder, 'masks', 'calib')))>max_file:
                max_file = len(os.listdir(os.path.join(cam_folder, bag_folder, 'masks', 'calib')))
                max_folder = bag_folder
        
        session_output_path = os.path.join(output_base_path, date_folder, session_folder, 'cam'+str(cam+1))
        os.makedirs(session_output_path, exist_ok=True)
        pcd_src = os.path.join(base_path, date_folder, session_folder, 'cam'+str(cam+1), max_folder, 'calib.pcd')
        pcd_dst = os.path.join(session_output_path, 'calib.pcd')
        shutil.copy(pcd_src, pcd_dst)
        
        image_src = os.path.join(base_path, date_folder, session_folder, 'cam'+str(cam+1), max_folder, 'calib.jpg')
        image_dst = os.path.join(session_output_path, 'calib.jpg')
        shutil.copy(image_src, image_dst)

        txt_src = os.path.join('/lab/kiran/3d2d_ann/proj_pcd/cus_data/cam/', str(cam+1),  'calib.txt')
        txt_dst = os.path.join(session_output_path, 'calib.txt')
        shutil.copy(txt_src, txt_dst)

        mask_src = os.path.join(base_path, date_folder, session_folder, 'cam'+str(cam+1), max_folder, 'masks', 'calib')

        mask_dst = os.path.join(session_output_path, 'masks')
        shutil.copytree(mask_src, mask_dst)


if __name__ == "__main__":
    base_path = '/lab/tmpig10c/auto_res/'
    output_base_path = '/lab/tmpig10c/RES'
    process_files(base_path, output_base_path)
