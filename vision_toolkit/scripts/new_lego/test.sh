
roslaunch lego_loam run.launch &

./run_LeGO_parameter.sh /home/tmp/kiran/split_bags/2023_03_11/0/sector0_output.bag 2023_03_11 0 0

sleep 8

if [ ! -s /tmp/odometry.txt ]; then
    echo "$1" >> LeGO_error.txt
else

    mkdir -p "/lab/tmpig13b/kiran/bag_dump/$3/$2/all_odom/sector$4/"
    mkdir -p "/lab/tmpig13b/kiran/bag_dump/$3/$2/all_lego/sector$4/"
    mv /tmp/odometry.txt "/lab/tmpig13b/kiran/bag_dump/$3/$2/all_odom/sector$4/"
    mv /tmp/cornerMap.pcd "/lab/tmpig13b/kiran/bag_dump/$3/$2/all_lego/sector$4/"
    mv /tmp/trajectory.pcd "/lab/tmpig13b/kiran/bag_dump/$3/$2/all_lego/sector$4/"
    mv /tmp/surfaceMap.pcd "/lab/tmpig13b/kiran/bag_dump/$3/$2/all_lego/sector$4/"
fi