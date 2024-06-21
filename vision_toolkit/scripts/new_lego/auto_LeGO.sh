#!/bin/bash

bag_file=$1

roslaunch lego_loam run.launch &

pid1=$!
sleep 10
rosbag play "$bag_file" --topic /velodyne_points /imu/data --clock &

pid2=$!

wait $pid2

if [ $? -eq 0 ]; then
    kill $pid1
    exit 0
else
    exit 1
fi
