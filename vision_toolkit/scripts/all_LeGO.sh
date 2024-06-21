#!/bin/bash

# Iterate over each folder in /data
for folder in /data/*; do
    # Check if it's a directory
    if [ -d "$folder" ]; then
        # Run bag.sh with the folder name as argument
        ./run_LeGO.sh "$(basename "$folder")"
    fi
done
