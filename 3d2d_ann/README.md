# 3d2d_ann

This repository contains the code to project 3D point cloud to 2D image, doing a correspondence.

# match.py

To run the match, simply use

```shell
python match.py 1326035199606919
```
It means it will read the 1326035199606919.bin in ./velodyne_sync, and automatically find the closest images of 5 cams.

# project_vel_to_cam.py
It can project 3D point cloud to 2d.


To run the project, simply use

```shell
python project_vel_to_cam.py vel img cam_num
```

vel:  The velodyne binary file (timestamp.bin)

img:  The undistorted image (timestamp.tiff)

cam_num:  The index (0 through 5) of the camera
