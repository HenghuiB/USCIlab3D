import os
import shutil
from os.path import join,basename
import argparse
import json
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str)
args = parser.parse_args()



dates=[]

for fn in os.listdir(args.input):
    if os.path.isdir(join(args.input, fn)):
        dates.append(join(args.input, fn))

res = {}


for date in dates:
    for session in os.listdir(date):
        img_path = join(date, session, 'all_imgs')
        first_100_images = {}

        for file_name in os.listdir(img_path):
            # Split the file name to get camera number and time
            parts = file_name.split('_')
            cam_number = parts[0][-1]  # Extracting the camera number from the filename

            # If this is the first time encountering this camera, initialize the list
            if cam_number not in first_100_images:
                first_100_images[cam_number] = []

            # Add the file name to the list of images for this camera
            first_100_images[cam_number].append(file_name)
        for key,value in first_100_images.items():
            first_100_images[key] = sorted(value)

        # Iterate through the images for each camera and copy the first 100
        for cam_number, images in first_100_images.items():
            # Create a directory for this camera if it doesn't exist
            cam_dir = os.path.join(date, session, 'check', f"cam{cam_number}")
            os.makedirs(cam_dir, exist_ok=True)

            # Copy the first 100 images to the new directory
            for i, image_name in enumerate(images[:300]):
                source_path = os.path.join(img_path, image_name)
                dest_path = os.path.join(cam_dir, image_name)
                shutil.copyfile(source_path, dest_path)
                print(f"Copying {image_name} to {dest_path}")




