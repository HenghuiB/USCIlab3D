import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str)
parser.add_argument('--odo', type=str)
parser.add_argument('--target', type=str)
args = parser.parse_args()

img_path = args.data
odo_path = args.odo
target_path = args.target

imgs = sorted([f for f in os.listdir(img_path) if os.path.isfile(os.path.join(img_path, f))])

import numpy as np
# import transformations as tf
import transforms3d as tf


# Function to convert Euler angles to quaternion and translation vector
def euler_to_quaternion_translation(roll, pitch, yaw, translation):
    # quaternion = tf.quaternion_from_euler(roll, pitch, yaw, 'sxyz')  # Hamilton convention ('sxyz' for roll, pitch, yaw)
    rotation_matrix = tf.euler.euler2mat(roll, pitch, yaw, 'sxyz')
    translation = -np.dot(rotation_matrix, translation)
    quaternion_result = tf.quaternions.mat2quat(rotation_matrix)

    return quaternion_result, translation





curr=0
dict={}
with open(odo_path, 'r') as f:
    lines = f.readlines()
    for temp in lines:
        temp = temp.strip().split()
        dict[temp[6]] = temp

with open(target_path, 'w') as f:
    while True:
        if imgs[curr] not in dict.keys():
            curr+=1
            continue
        temp = dict[imgs[curr]]
        translation_vector = np.array([float(temp[0]), float(temp[1]), float(temp[2])])
        roll, pitch, yaw = float(temp[3]), float(temp[4]), float(temp[5])
        quaternion_result, translation_result = euler_to_quaternion_translation(roll, pitch, yaw, translation_vector)
        img_name = imgs[curr]
        f.write(str(curr+1)+' '+str('{:.6f}'.format(quaternion_result[0]))+' '+str('{:.6f}'.format(quaternion_result[1]))+' '+str('{:.6f}'.format(quaternion_result[2]))+' '+str('{:.6f}'.format(quaternion_result[3]))+' '+str('{:.6f}'.format(translation_result[0]))+' '+str('{:.6f}'.format(translation_result[1]))+' '+str('{:.6f}'.format(translation_result[2]))+' '+'1'+' '+str(img_name))
        f.write('\n\n')
        curr+=1
        if curr==len(imgs):
            break

