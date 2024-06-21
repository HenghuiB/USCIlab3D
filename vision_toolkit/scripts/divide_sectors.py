import os
import shutil
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
parser.add_argument('--target', type=str)
parser.add_argument('--interval', type=int, default = 250)
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

img_path = args.data
target_path = args.target
if img_path[-1]!='/':
    img_path+='/'
if target_path[-1]!='/':
    target_path+='/'

file_names_all = [[] for i in range(5)]

for fn in os.listdir(img_path):
    if ".jpg" in fn:
        file_names_all[int(fn[3])-1].append(fn)

for i in range(5):
    file_names_all[i] = sorted(file_names_all[i])    


if not os.path.exists(target_path):
    os.makedirs(target_path)


counts = [0,0,0,0,0]
lens = [len(i) for i in file_names_all]
done = [0,0,0,0,0]
interval = args.interval
tra=0

for tmp_len in lens:
    if tmp_len == 0:
        with open('error_log_divide.txt', 'a') as error_file:
            error_file.write(f"{args.data}\n")
        sys.exit(1)
print(lens)
while True:
    os.makedirs(target_path + 'sector' + str(tra) + '/input', exist_ok=True)
    os.makedirs(target_path + 'sector' + str(tra) + '/gt_dense', exist_ok=True)
    os.makedirs(target_path + 'sector' + str(tra) + '/gt_annot', exist_ok=True)

    for i in range(5):
        while counts[i] < round(lens[i]/(lens[0]/float(interval))*(tra+1)):
            if counts[i] == lens[i]-1:
                done[i]=1
                break
            if not os.path.exists(f'{img_path}{file_names_all[i][counts[i]]}'):
                print(f'{img_path}{file_names_all[i][counts[i]]}')
                raise ValueError("No image")
            copy_file(f'{img_path}{file_names_all[i][counts[i]]}', f'{target_path}sector{tra}/input/{file_names_all[i][counts[i]]}')
            counts[i] += 1
            

    tra+=1
    if args.num==tra:
        break
    if sum(done) == 5:
        break

