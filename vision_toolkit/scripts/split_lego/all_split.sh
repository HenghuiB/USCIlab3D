#!/bin/bash

# Input file
input_file="/lab/tmpig10c/kiran/vision_toolkit/scripts/split_lego/All_sessions.txt"


# Read input file line by line
while IFS=$'\t' read -r date_and_session bag_file bag_files; do
    # Extract date and session
    date=$(echo "$date_and_session" | cut -d'/' -f1)
    session=$(echo "$date_and_session" | cut -d'/' -f2)

    bag_path="/data/$date/cam1/$(basename "$bag_file")"
    echo $bag_path
    ./split_bag.sh "/lab/tmpig10b/kiran/gs_train/$date/$session/" "$bag_path" "/home/tmp/kiran/split_bags/$date/$session"
done < "$input_file"
