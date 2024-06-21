#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 parameter_path"
    exit 1
fi

date=$(basename "$1")


bag_count=0

# Loop through each bag file and execute the script
for bag_file in $(ls -v "/data/$1/cam1"/*.bag); do



    ./auto_LeGO.sh "$bag_file"
    if [ ! -s /tmp/odometry.txt ]; then
        echo "$1 $bag_file" >> LeGO_error.txt
    else
        mv /tmp/odometry.txt "/lab/tmpig10b/kiran/bag_dump/$date/$bag_count/all_odom/"
        mv /tmp/cornerMap.pcd "/lab/tmpig10b/kiran/bag_dump/$date/$bag_count/all_lego/"
        mv /tmp/trajectory.pcd "/lab/tmpig10b/kiran/bag_dump/$date/$bag_count/all_lego/"
        mv /tmp/surfaceMap.pcd "/lab/tmpig10b/kiran/bag_dump/$date/$bag_count/all_lego/"
    fi

    sleep 20
    ((bag_count+=1))
done

