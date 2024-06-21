import os
import sys
import re

def find_closest_file(input_filename):
    match = re.search(r'(\d+)', input_filename)
    if not match:
        raise ValueError("Input filename does not contain a numeric part.")

    numeric_part = int(match.group(1))

    lb3_folders = ['./lb3/Cam0', './lb3/Cam1', './lb3/Cam2', './lb3/Cam4', './lb3/Cam5']

    closest_filename = None
    closest_difference = float('inf')

    files_in_folder = os.listdir(lb3_folders[0])


    for file_in_folder in files_in_folder:
        match_folder = re.search(r'(\d+)', file_in_folder)
        if not match_folder:
            continue

        numeric_folder = int(match_folder.group(1))
        difference = abs(numeric_folder - numeric_part)

        if difference < closest_difference:
            closest_difference = difference
            closest_filename = os.path.join(lb3_folders[0], file_in_folder)

    if closest_filename is None:
        raise FileNotFoundError("No matching file found in the lb3 folders.")

    return [os.path.join(folder, closest_filename.split('/')[-1]) for folder in lb3_folders]

# Example usage
input_filename = './velodyne_sync/'+sys.argv[1]+'.bin'
result = find_closest_file(input_filename)
print(result)

