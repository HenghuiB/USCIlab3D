#!/bin/bash
source /opt/ros/noetic/setup.bash


# roscore &

pid1=$!
sleep 10


input_file="/lab/tmpig13b/kiran/bag_dump/All_sessions.txt"


# Read input file line by line
while IFS=$'\t' read -r date_and_session bag_file bag_files; do
    # Extract date and session
    date=$(echo "$date_and_session" | cut -d'/' -f1)
    session=$(echo "$date_and_session" | cut -d'/' -f2)
    bag_path="/data/$date/cam1/$(basename "$bag_file")"
    echo $bag_path

    mkdir -p "/lab/tmpig13b/kiran/bag_dump/$date/$session/all_pcl/"
    rosrun pcl_ros bag_to_pcd "$bag_path" /velodyne_points "/lab/tmpig13b/kiran/bag_dump/$date/$session/all_pcl"

    sleep 10

    if [ -z "$(ls -A "/lab/tmpig13b/kiran/bag_dump/$date/$session/all_pcl/")" ]; then
    echo "$bag_path" >> error_pcl.txt
fi
done < "$input_file"
exit 0

