import os
import subprocess
from os.path import join
import json
import sys
import time

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


def extract_and_call_script(folder_path, interval=50, script_path="./vision_gpt4.py"):
    # Check if the folder exists
    img_path = join(folder_path, 'all_imgs/')
    pcl_path = join(folder_path, 'all_pcl/')
    json_path = join(folder_path, 'sync_data.json')
    res_path = join(folder_path, 'label_dict.txt')
    if not os.path.exists(img_path) or not os.path.exists(json_path) or not os.path.exists(pcl_path):
        print(f"Error: Folder '{folder_path}' error.")
        return
    
    with open(json_path, "r") as json_file:
        sync_data = json.load(json_file)
    reverse_sync = []
    for tmp in sync_data:
        reverse_sync.append({value: key for key, value in tmp.items()})
    f = open(res_path,'w')

    files = os.listdir(pcl_path)
    files.sort()
    os.makedirs(join(folder_path, 'text_gpt4/'), exist_ok=True)
    start = time.time()
    for i, file_name in enumerate(files):
        if i % interval == 0:
            five_imgs = find_closest_file(file_name, reverse_sync)
            for v_img in five_imgs:
                image_path = os.path.join(img_path, v_img)
                print(f"Processing image: {image_path}")
                print('pcl', file_name)
            # Call the other script with the image as a parameter
                if os.path.exists(join(folder_path, 'text_gpt4/', image_path.split('/')[-1].split('.')[0]+'.txt')):
                    continue
                subprocess.run(["python" , script_path , image_path , join(folder_path, 'text_gpt4/')])
            f.write(f"{file_name} {' '.join(five_imgs)}\n")
    f.close()
    print(time.time()-start)
    # Specify the folder containing images and the path to the other script
    # folder_path = "/lab/tmpig13b/kiran/bag_dump/2023_03_30/3/"
folder_path = sys.argv[1]
other_script_path = "./vision_gpt4.py"

# Call the function with the specified parameters
extract_and_call_script(folder_path, interval=150, script_path=other_script_path)

