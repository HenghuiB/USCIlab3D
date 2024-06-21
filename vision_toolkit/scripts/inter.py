import os
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from scipy import interpolate
import transforms3d as tf
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--img_path', type=str)
parser.add_argument('--output', type=str)
parser.add_argument('--odo', type=str)
args = parser.parse_args()
ODOM_FILE = args.odo
OUTFILE = args.output
file_names = []
name_dict = {}
for fn in os.listdir(args.img_path):
    if ".jpg" in fn:
        if int(fn[5:-4]) in name_dict.keys():
            name_dict[int(fn[5:-4])].append(fn)
        else:
            file_names.append(int(fn[5:-4]))
            name_dict[int(fn[5:-4])] = [fn]
# file_names.sort()


x = []
y = []
z = []
row = []
pitch = []
yaw = []
time = []

with open(ODOM_FILE, "r") as f:
    for line in f:
        poses = line.strip().split(", ")
        #bad fix here
        x.append(float(poses[2]))
        y.append(float(poses[1]))
        z.append(float(poses[0]))
        row.append(float(poses[3]))
        pitch.append(float(poses[4]))
        yaw.append(float(poses[5]))
        time.append(int(poses[6].replace('.', '')))



interpolator_x = interpolate.interp1d(time, x)
interpolator_y = interpolate.interp1d(time, y)
interpolator_z = interpolate.interp1d(time, z)
interpolator_row = interpolate.interp1d(time, row)
interpolator_pitch = interpolate.interp1d(time, pitch)
interpolator_yaw = interpolate.interp1d(time, yaw)



decimal_places = len(str(time[-1]))
rounded_file_names = []
time_dict={}
for i in file_names:
    rounded_file_names.append(int(str(i)[:decimal_places]))
    time_dict[rounded_file_names[-1]] = i
# rounded_file_names = [int(str(i)[:decimal_places]) for i in file_names]
rounded_file_names.sort()
interpolation_time = np.array(rounded_file_names)


closest_pose=[]
for i in range(len(time)):
    tmp = [2**50 for _ in range(6)]
    res= ['' for _ in range(6)]
    for i_t in range(len(interpolation_time)):
        for file_name in name_dict[time_dict[interpolation_time[i_t]]]:
            cam = int(file_name[3])
            if abs(interpolation_time[i_t]-time[i])<tmp[cam-1]:
                tmp[cam-1] = abs(interpolation_time[i_t]-time[i])
                res[cam-1] = file_name
    closest_pose+=res

interpolated_x = interpolator_x(interpolation_time)
interpolated_y = interpolator_y(interpolation_time)
interpolated_z = interpolator_z(interpolation_time)
interpolated_row = interpolator_row(interpolation_time)
interpolated_pitch = interpolator_pitch(interpolation_time)
interpolated_yaw = interpolator_yaw(interpolation_time)



# translation = [[0.13116, -0.01, -0.019], [0.05004123414516961, 0.121650402733524, -0.019], [-0.100232816459295, 0.0851840836344303, -0.019], [-0.11198852150514299, -0.0690037437469328, -0.019], [0.03102010381926821, -0.127830742621022, -0.019]]
# rotation = [[1.5707963267949, 1.5707963267949, 0], [1.5707963267949, 2.82743338823082, 0], [1.5707963267949, -2.19911485751285, 0], [1.5707963267949, -0.942477796076929, 0], [1.5707963267949, 0.314159265358991, 0]]


# translation = [[0.13116, -0.01, -0.019], [0.03102010381926821, -0.127830742621022, -0.019], [-0.100232816459295, 0.0851840836344303, -0.019], [-0.11198852150514299, -0.0690037437469328, -0.019], [0.05004123414516961, 0.121650402733524, -0.019]]
translation = [[0.05004123414516961, 0.121650402733524, -0.019], [-0.100232816459295, 0.0851840836344303, -0.019], [0.03102010381926821, -0.127830742621022, -0.019], [-0.11198852150514299, -0.0690037437469328, -0.019], [0.13116, -0.01, -0.019]]


# rotation = [[0, -1.5707963267949, 0], [0, 0.314159265358991-3.14159265358979, 0], [0, 3.14159265358979-2.19911485751285, 0], [0, 3.14159265358979-0.942477796076929, 0], [0, 2.82743338823082-3.14159265358979, 0]]
rotation = [[0, 2.82743338823082-3.14159265358979, 0], [0, 3.14159265358979-2.19911485751285, 0], [0, 0.314159265358991-3.14159265358979, 0],[0, 3.14159265358979-0.942477796076929, 0],  [0, -1.5707963267949, 0]]

# velodine = tf.euler.euler2mat(1.5707963267949, 3.14159265358979, 0, 'sxyz')
print('+554322333')
with open(os.path.join(OUTFILE,'odometry.txt'), "w") as f:
    for i in range(len(interpolation_time)):
        for file_name in name_dict[time_dict[interpolation_time[i]]]:
            if file_name not in closest_pose:
                continue
            cam = int(file_name[3])
            x = interpolated_x[i] + translation[cam-1][0]
            f.write(f"{float(x):.6f} ")
            y = interpolated_y[i] + translation[cam-1][2]
            # x = interpolated_x[i] + translation[cam-1][2]
            # f.write(f"{float(x):.6f} ")
            # y = interpolated_y[i] + translation[cam-1][0]

            f.write(f"{float(y):.6f} ")
            z = interpolated_z[i] + translation[cam-1][1]
            f.write(f"{float(z):.6f} ")
            row = interpolated_row[i] + rotation[cam-1][0]
            pitch = interpolated_pitch[i] + rotation[cam-1][1]
            # pitch = interpolated_pitch[i] + rotation[cam-1][1] + (0.3+0.03*5)
            yaw = interpolated_yaw[i] + rotation[cam-1][2]
            # rotation_matrix = tf.euler.euler2mat(rotation[cam-1][0], rotation[cam-1][1], rotation[cam-1][2], 'sxyz')
            # t = tf.euler.euler2mat(interpolated_row[i], interpolated_pitch[i], interpolated_yaw[i], 'sxyz')
            # row, pitch, yaw = tf.euler.mat2euler(np.dot(rotation_matrix, np.dot(velodine,t)), 'sxyz')
            # row, pitch, yaw = tf.euler.mat2euler(np.dot(rotation_matrix, t), 'sxyz')
            f.write(f"{float(row):.6f} ")
            f.write(f"{float(pitch):.6f} ")
            f.write(f"{float(yaw):.6f} ")
            f.write(file_name)
            f.write('\n')
