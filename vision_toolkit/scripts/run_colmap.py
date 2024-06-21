import subprocess
import os
import sys

def generate_colmap(parent_folder):
    for session in os.listdir(parent_folder):
        session_path = os.path.join(parent_folder, session)
        for sector in os.listdir(session_path):
            folder_path = os.path.join(session_path, sector)
            subprocess.call(f"python ./convert.py -s {folder_path}", shell=True)
            print(folder_path)

if __name__ == "__main__":
    parent_folder = sys.argv[1]
    generate_colmap(parent_folder)

#0:0 10:1 22:2
#CUDA_VISIBLE_DEVICES=1 python run_colmap.py /lab/tmpig10b/kiran/gs_train/2023_03_29/
#iGpu 2023_03_11 2023_03_27
#iGpu2 2023_03_28 2023_03_29
#iGpu3 2023_03_30 2023_06_18
#iGPu4 2023_06_19
#iGpu5 2023_06_20
#iGpu7 2023_06_21 2023_06_22
#iGPu8 2023_06_24 2023_06_25
#igpu10 2023_06_26 2023_06_27
#igpu13 2023_06_28
#igpu14 2023_12_24 2024_03_16
#igpu15 2023_07_01 2023_07_02 2023_07_03 2023_07_05
#igpu20 2023_07_06 2023_07_11
#igpu21 2023_07_13 2023_07_14 2023_07_15 2023_07_16
#igpu22 2023_07_17 2023_07_28
#igpu23 2023_08_20
#igpu24 2023_07_30 2023_07_31
#igpu25 2023_08_05 2023_08_07 2023_08_08 2023_08_09 2023_08_10