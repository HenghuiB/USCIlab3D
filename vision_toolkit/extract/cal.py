import subprocess
import os
import sys

def generate_colmap(parent_folder):
    with open ('res.txt','a') as f:
        for session in os.listdir(parent_folder):
            if session=='All_sessions.txt':
                continue
            session_path = os.path.join(parent_folder, session)
            for sector in os.listdir(session_path):
                folder_path = os.path.join(session_path, sector)
                f.write(f'{session} {sector} {len(os.listdir(os.path.join(folder_path, "all_imgs")))} {len(os.listdir(os.path.join(folder_path, "all_pcl")))}\n')

if __name__ == "__main__":
    parent_folder = sys.argv[1]
    generate_colmap(parent_folder)