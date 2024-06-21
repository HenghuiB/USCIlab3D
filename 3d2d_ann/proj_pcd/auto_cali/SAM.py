import os
import shutil
import random
import subprocess
#/lab/kiran/3d2d_ann/proj_pcd/auto_cali/
def process_files(base_path, output_base_path):
    # tmp_path = ['2023_08_20', '2024_03_16', '2023_07_14', '2023_08_08', '2023_03_30', '2023_07_31', '2023_08_05', '2023_08_07', '2023_03_29', '2023_07_15', '2023_06_20', '2023_12_24']
    # tmp_path = [, , , ]
    tmp_path = ['2023_12_24']
    for date_folder in tmp_path:
        date_path = os.path.join(base_path, date_folder)
        print(os.listdir(base_path))
        print(tmp_path)
        if os.path.isdir(date_path):
            for session_folder in os.listdir(date_path):
                session_path = os.path.join(date_path, session_folder)
                if os.path.isdir(session_path):
                    label_file_path = os.path.join(session_path, 'label_dict.txt')
                    if os.path.isfile(label_file_path):
                        process_label_file(label_file_path, date_folder, session_folder, output_base_path)

def process_label_file(label_file_path, date_folder, session_folder, output_base_path):
    with open(label_file_path, 'r') as file:
        lines = file.readlines()
    
    # Randomly sample 10 lines
    # sampled_lines = random.sample(lines, min(10, len(lines)))
    num_lines = len(lines)
    step = max(num_lines // 10, 1)
    indices = [i for i in range(0, num_lines, step)][:10]
    sampled_lines = [lines[i] for i in indices]
    
    for cam in range(0,5):
        for idx, line in enumerate(sampled_lines):
            line_parts = line.strip().split()
            pcd_file = line_parts[0]
            image_files = line_parts[1:6]  # cam1 to cam5 images
            
            session_output_path = os.path.join(output_base_path, date_folder, session_folder, 'cam'+str(cam+1),str(idx))
            os.makedirs(session_output_path, exist_ok=True)
            
            # Copy pcd file
            pcd_src = os.path.join(os.path.dirname(label_file_path), 'all_pcl',pcd_file)
            pcd_dst = os.path.join(session_output_path, 'calib.pcd')
            shutil.copy(pcd_src, pcd_dst)
            
            # Copy image file (assuming using cam1 image)
            image_src = os.path.join(os.path.dirname(label_file_path), 'all_imgs', image_files[cam])
            image_dst = os.path.join(session_output_path, 'calib.jpg')
            shutil.copy(image_src, image_dst)
            
            # Run the external script on the image
            run_external_script(image_dst, session_output_path)

def run_external_script(image_path, output_path):
    script_path = '/lab/tmpig10c/kiran/henghui/Grounded-Segment-Anything/segment_anything/scripts/amg.py'
    checkpoint_path = '/lab/tmpig10c/kiran/henghui/Grounded-Segment-Anything/sam_vit_h_4b8939.pth'
    model_type = 'vit_h'
    output_masks_path = os.path.join(output_path, 'masks')
    os.makedirs(output_masks_path, exist_ok=True)
    command = [
        'python', script_path,
        '--checkpoint', checkpoint_path,
        '--model-type', model_type,
        '--input', image_path,
        '--output', output_masks_path,
        '--stability-score-thresh', '0.9',
        '--box-nms-thresh', '0.4',
        '--stability-score-offset', '0.9'
    ]
    subprocess.run(command)

if __name__ == "__main__":
    base_path = '/lab/tmpig13b/kiran/bag_dump/'
    output_base_path = '/lab/tmpig10c/auto_res/'
    process_files(base_path, output_base_path)
