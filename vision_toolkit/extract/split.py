import os
import shutil

import argparse
from cv_bridge import CvBridge

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
parser.add_argument('--intervalfile', type=str)
parser.add_argument('--num', type=int, default = -1)
args = parser.parse_args()

def copy_file(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        print(f"File copied successfully from '{source_path}' to '{destination_path}'.")
    except FileNotFoundError:
        print(f"Error: The file '{source_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied. Unable to copy the file.")

img_path = './'+args.data+'/imgs/'
target_path = './'+args.data+'/'

intervals=[]
with open(args.intervalfile, 'r') as file:
    lines = file.readlines()

    for line in lines:
        intervals.append(int(line.strip()))

count=0
tra=0
flag=0
while True:
    os.mkdir(target_path+str(tra))
    while True:
        for i in range(1,6):
            if not os.path.exists(f'{img_path}cam{i}_image_{count}.jpg'):
                flag=1
                break
            copy_file(f'{img_path}cam{i}_image_{count}.jpg', f'{target_path}{tra}/cam{i}_image_{count}.jpg')
        if flag==1:
            break
        count+=1
        if count in intervals:
            print(count)
            break
    if flag==1:
        break
    tra+=1
    if count>500:
        break
    if args.num==tra:
        break

