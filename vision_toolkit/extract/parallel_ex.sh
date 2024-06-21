#!/bin/bash

# Function to process each folder
process_folder() {
    folder="$1"
    # if [ "$folder" = "2023_03_11" ]; then
    #         echo "Skipping folder $folder"
    #         continue
    # fi
    ./bag_.sh "$(basename "$folder")"
}

# Export the function to make it available to GNU Parallel
export -f process_folder

# Run GNU Parallel to execute the loop with 8 threads
parallel -j 12 process_folder ::: /data/*
