import os
import shutil
from os.path import join,basename
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str)
parser.add_argument('--output', type=str)
args = parser.parse_args()


def check_same_length(list_of_lists):
    if not list_of_lists:
        return True

    first_length = len(list_of_lists[0])

    for inner_list in list_of_lists[1:]:
        if len(inner_list) != first_length:
            return False

    return True
dates=[]

for fn in os.listdir(args.input):
    if os.path.isdir(join(args.input, fn)):
        dates.append(join(args.input, fn))

# print(dates)
# dates = ['/data/2023_12_18' ,'/data/2023_12_20', '/data/2023_12_24', '/data/2024_03_16']
with open(args.output,'w') as f:
    for date in dates:
        flag = 0
        bags = [[] for _ in range(5)]
        for i in range(5):
            if not os.path.exists(join(date,'cam'+str(i+1))):
                print(date,' dont have cam folder')
                flag = 1
                break
            bags[i] = sorted([bag for bag in os.listdir(join(date,'cam'+str(i+1))) if bag.endswith(".bag") or bag.endswith(".active") and os.path.isfile(join(join(date,'cam'+str(i+1)), bag))])
        if flag == 1:
            continue
        if check_same_length(bags):
            for session in range(len(bags[i])):
                f.write(basename(date) + '/' + str(session) + '\t')
                for i in range(5):
                    f.write(str(bags[i][session]) + '\t')
                f.write('\n')
                os.makedirs('/lab/tmpig10b/kiran/bag_dump/' + basename(date) + '/' +str(session) + '/all_lego', exist_ok=True)
                os.makedirs('/lab/tmpig10b/kiran/bag_dump/' + basename(date) + '/' +str(session) + '/all_odom', exist_ok=True)
        else:
            print(date, ' bags number wrong')


