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
    os.makedirs(input_folder + "/distorted/sparse", exist_ok=True)
    colmap_command = 'colmap'

    ## Feature extraction
    feat_extracton_cmd = colmap_command + " feature_extractor "\
        "--database_path " + input_folder + "/distorted/database.db \
        --image_path " + input_folder + "/input \
        --ImageReader.single_camera 1 \
        --ImageReader.camera_model " + "PINHOLE" + " \
        --SiftExtraction.use_gpu " + str(1)
    exit_code = os.system(feat_extracton_cmd)
    if exit_code != 0:
        print(f"Feature extraction failed with code {exit_code}. Exiting.")
        return 0

    ## Feature matching
    feat_matching_cmd = colmap_command + " exhaustive_matcher \
        --database_path " + input_folder + "/distorted/database.db \
        --SiftMatching.use_gpu " + str(1)
    exit_code = os.system(feat_matching_cmd)
    if exit_code != 0:
        print(f"Feature matching failed with code {exit_code}. Exiting.")
        return 0

    ### Bundle adjustment
    # The default Mapper tolerance is unnecessarily large,
    # decreasing it speeds up bundle adjustment steps.
    mapper_cmd = (colmap_command + " mapper \
        --database_path " + input_folder + "/distorted/database.db \
        --image_path "  + input_folder + "/input \
        --output_path "  + input_folder + "/distorted/sparse \
        --Mapper.ba_global_function_tolerance=0.000001")
    exit_code = os.system(mapper_cmd)
    if exit_code != 0:
        print(f"Mapper failed with code {exit_code}. Exiting.")
        return 0

    ### Image undistortion
    ## We need to undistort our images into ideal pinhole intrinsics.
    img_undist_cmd = (colmap_command + " image_undistorter \
        --image_path " + input_folder+ "/input \
        --input_path " + input_folder + "/distorted/sparse/0 \
        --output_path " + input_folder + "\
        --output_type COLMAP")
    exit_code = os.system(img_undist_cmd)
    if exit_code != 0:
        print(f"Mapper failed with code {exit_code}. Exiting.")
        return 0

    files = os.listdir(input_folder + "/sparse")
    os.makedirs(input_folder + "/sparse/0", exist_ok=True)
    # Copy each file from the source directory to the destination directory
    for file in files:
        if file == '0':
            continue
        source_file = os.path.join(input_folder, "sparse", file)
        destination_file = os.path.join(input_folder, "sparse", "0", file)
        shutil.move(source_file, destination_file)

    return 1


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

