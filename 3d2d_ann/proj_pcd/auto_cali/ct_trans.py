import os
import shutil
import random
import subprocess
import numpy as np
import pickle
def process_files(base_path, output_base_path):
    res = {}
    for date_folder in os.listdir(base_path):
        date_path = os.path.join(base_path, date_folder)
        if os.path.isdir(date_path):
            for session_folder in os.listdir(date_path):
                session_path = os.path.join(date_path, session_folder)
                if os.path.isdir(session_path):
                    for cam in range(0,5):
                        cam_folder = os.path.join(base_path, date_folder, session_folder, 'cam'+str(cam+1))
                        if not os.path.exists(os.path.join(cam_folder, 'extrinsic.txt')):
                            print(cam_folder)
                            continue
                        with open(os.path.join(cam_folder, 'extrinsic.txt')) as f:
                            lines = f.readlines()
                        matrix_data = []
                        for line in lines:
                            if line.startswith("["):
                                line = line.strip()
                                if line[-1] == ",":
                                    line = line[:-1]
                                row = [float(val.strip(',')) for val in line.strip().lstrip("[,").rstrip("]\n").split(",")]
                                matrix_data.append(row)
                        extrinsic_matrix = np.array(matrix_data)
                        if date_folder not in res.keys():
                            res[date_folder] = {session_folder : {'cam'+str(cam+1):extrinsic_matrix}}
                        else:
                            if session_folder not in res[date_folder].keys():
                                res[date_folder][session_folder] = {'cam'+str(cam+1):extrinsic_matrix}
                            else:
                                if cam+1 not in res[date_folder][session_folder].keys():
                                    res[date_folder][session_folder]['cam'+str(cam+1)] = extrinsic_matrix
                                else:
                                    print('error')
    with open(output_base_path, 'wb') as output_file:
        pickle.dump(res, output_file)


if __name__ == "__main__":
    base_path = '/home/tmp/kiran/SensorsCalibration-master/lidar2camera/auto_calib_v2.0/res/'
    output_base_path = './extrinsic'
    process_files(base_path, output_base_path)
