
# extract python code

The program takes something as input and saves it into something. You can run it through this command

```
./bag_.sh 2023_06_30
```
It will extract images from bag file,you just have to pass the bag folder, assuming it has cam1, cam2, cam3, cam4, cam5. And it will generate a folder having same name eg 2023_06_30/imgs.

```
python split.py --data 2023_06_30 --intervalfile ./interval.txt
```
It will split the images folder according to the interval file.

# 3dobject_tracking

Build instructions:
(From root directory of the repo, ie. /path/to/3dobject_tracking/)

```
mkdir build
cd build
```
Then:
(CMake):
```
cmake ../
make
```

or
(Ninja):
```
cmake -G Ninja ../
ninja
```

ROS version: http://wiki.ros.org/melodic/Installation (Recommended for Ubuntu 18.04 which is what I have)

# removeNoise
Removes noise with a value of 0 from a depth image.

With the noisy image named "depthimage.png" in the same directory as the program, run the following command:
```
python removeNoise.py
```

# autostitcher
Stitches together 5 images into a panorama.

The images are located in a directory named "hello" and are named "cam1.png", "cam2.png", "cam3.png", "cam4.png", "cam5.png". Run the following command in the terminal:
```
python autostitcher
```
The resulting panorama is outputted with the default file name "testpanorama.png".

# bag_reader
Reads images from cam[1-5] bag files in the same directory, offsets the image stream of each so that they are of equal length, and merges them into a "merge.bag" file.

When the executable is built, run the following command in the terminal:
```
./bag_reader
```

# bagstitch
Reads "merged.bag" from the directory and stitches together every set of five images from the image streams (color and depth) using autostitcher.py. The panoramas are stored in the "hello" directory.

Run the following command in the terminal:
```
python bagstitch.py
```
