#!/bin/bash


for entry in "/lab/tmpig13b/kiran/bag_dump/"*; do
    date=$(basename "$entry")
    ./sync_cam.sh "$date"
  done


