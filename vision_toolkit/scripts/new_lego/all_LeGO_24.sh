#!/bin/bash

# Input file
input_file="All_sessions.txt"


# Read input file line by line
while IFS=$'\t' read -r date_and_session bag_file bag_files; do
    # Extract date and session
    date=$(echo "$date_and_session" | cut -d'/' -f1)
    session=$(echo "$date_and_session" | cut -d'/' -f2)

    bag_directory="/home/tmp/kiran/split_bags/$date/$session/"
    for bag_file in "$bag_directory"*.bag; 
    do
        # Extract the sector identifier (e.g., sector0, sectorN) from the filename
        # bag_path="/data/$date/cam1/$(basename "$bag_file")"
        echo "$bag_file" "$session" "$date" "$sector"
        sector=$(basename "$bag_file" _output.bag)
        ./run_LeGO_parameter.sh "$bag_file" "$session" "$date" "$sector"
        sleep 8
    done
done < "$input_file"


