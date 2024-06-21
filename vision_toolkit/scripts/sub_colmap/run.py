import subprocess
import os
import sys
import time
from filelock import Timeout, FileLock
import concurrent.futures

def run_conversions_in_parallel(parent_folder, max_threads=6):
    s = time.time()
    # Define a function to run the conversion for a folder
    folders=[]
    for session in os.listdir(parent_folder):
        session_path = os.path.join(parent_folder, session)
        for sector in os.listdir(session_path):
            folder_path = os.path.join(session_path, sector)
            folders.append(folder_path)
    def run_conversion(folder):
        lock_file_path = os.path.join(folder, '.lock')
        lock = FileLock(lock_file_path, timeout=2)
        with lock:
            subprocess.call(f"python /lab/tmpig10c/kiran/vision_toolkit/scripts/sub_colmap/convert.py -s {folder}", shell=True)
        # subprocess.run(['python', '/lab/kiran/vision_toolkit/scripts/sub_colmap/convert_2.py', '-s'], cwd=folder)
            os.remove(lock_file_path)
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:

        futures = [executor.submit(run_conversion, folder) for folder in folders]
        concurrent.futures.wait(futures)
    print(time.time() - s)


#49210
#CUDA_VISIBLE_DEVICES=1 python run.py /lab/tmpig10b/kiran/gs_train/2023_03_11/ 4
if __name__ == "__main__":
    parent_folder = sys.argv[1]
    # generate_colmap(parent_folder)
    run_conversions_in_parallel(parent_folder, int(sys.argv[2]))
#err 13b
#0620 10b
#0619 20g