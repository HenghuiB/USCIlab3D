import ray
import os
import glob
import torch
import random
import gc,shutil
import subprocess

#@ray.remote(num_gpus=1)
#def use_gpu(inp):
#    print("ray.get_gpu_ids(): {}".format(ray.get_gpu_ids()))
#    print("CUDA_VISIBLE_DEVICES: {}".format(os.environ["CUDA_VISIBLE_DEVICES"]))

@ray.remote(num_gpus=1,num_cpus=4)
def colmap_for_gstrain(input_folder):
    return subprocess.run(['python', 'convert.py', '-s', 'input_folder'])


#whisper_remote = ray.remote(convert_m4a_to_mp3)
#whisper_remote = ray.remote(diarizate)
#whisper_remote = ray.remote(use_gpu)



if __name__ == "__main__":
    #ray.init(address='auto')
    ray.init(address='192.168.0.90:6379')
    ray.cluster_resources()
    folder_path = '/lab/tmpig10b/kiran/gs_train/rayt/'
    list_folders = glob.glob(os.path.join(folder_path, '*/'))
    
    outputs = []

    for i in range(len(list_folders)):
        #convert_m4a_to_mp3(file_list[i])
        #outputs.append(whisper_remote.remote(file_list[i]))
        outputs.append(colmap_for_gstrain.remote(list_folders[i]))
        #break


    ray.get(outputs)
    #ray.get(use_gpu.remote(0))

