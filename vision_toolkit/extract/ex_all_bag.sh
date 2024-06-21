#!/bin/bash

# Iterate over each folder in /data
for folder in /data/*; do
    # Check if it's a directory
    if [ -d "$folder" ]; then
        # Run bag.sh with the folder name as argument
        ./bag_.sh "$(basename "$folder")"
    fi
done
