import matplotlib.pyplot as plt
import os
import collections
import numpy as np
import struct
import argparse
from IPython import embed
Point3D = collections.namedtuple(
    "Point3D", ["id", "xyz", "rgb", "error", "image_ids", "point2D_idxs"]
)

def read_points3D_text(path):
    """
    see: src/colmap/scene/reconstruction.cc
        void Reconstruction::ReadPoints3DText(const std::string& path)
        void Reconstruction::WritePoints3DText(const std::string& path)
    """
    points3D = {}
    with open(path, "r") as fid:
        while True:
            line = fid.readline()
            if not line:
                break
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                elems = line.split()
                point3D_id = int(elems[0])
                xyz = np.array(tuple(map(float, elems[1:4])))
                rgb = np.array(tuple(map(int, elems[4:7])))
                error = float(elems[7])
                image_ids = np.array(tuple(map(int, elems[8::2])))
                point2D_idxs = np.array(tuple(map(int, elems[9::2])))
                points3D[point3D_id] = Point3D(
                    id=point3D_id,
                    xyz=xyz,
                    rgb=rgb,
                    error=error,
                    image_ids=image_ids,
                    point2D_idxs=point2D_idxs,
                )
    return points3D


test = read_points3D_text('./points3D.txt')
res = {}
for key, value in test.items():
    res[key] = value.point2D_idxs.shape[0]

import pickle
with open('lf.pkl', 'rb') as f:
    a = pickle.load(f)


# plt.hist(res, bins=range(0, 101, 10), label='number of each 3D point corresponding to 2d pixels')

# # plt.hist(res, bins=500, label='number of each 3D point corresponding to 2d pixels')
# # plt.hist(oo, bins=20, color='orange', label='number of each 3D point corresponding unique labels')

# plt.title('Histogram of number of each 3D point corresponding to 2d pixels')
# plt.xlabel('Values')
# plt.ylabel('Frequency')
# plt.legend()
# plt.savefig('pt.png')
num_plots = 10

num_rows = num_plots // 5
num_cols = 5

fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 3*num_rows))

# Iterate over each subplot
for i in range(num_plots):
    row = i // num_cols
    col = i % num_cols
    
    start_range = i * 10
    end_range = (i + 1) * 10
    
    # Filter data within the current range
    filtered_data = []
    for key, value in res.items():
        if start_range <= value < end_range:
            filtered_data.append(len(set(a[key])))

    
    # Plot histogram for the current range
    axs[row][col].hist(filtered_data, bins=range(min(filtered_data), max(filtered_data)+1))
    axs[row][col].set_title(f'{start_range}-{end_range}')
    axs[row][col].set_xlabel('Values')
    axs[row][col].set_ylabel('Frequency')
    axs[row][col].set_xlim(min(filtered_data), max(filtered_data))
    axs[row][col].set_xticks(range(min(filtered_data), max(filtered_data)+1, 2))  # Adjust x-axis ticks

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('multiple_histogramsb.png')

