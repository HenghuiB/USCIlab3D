#!/bin/bash

# Function to delete .lock files
delete_lock_files() {
    # Use find command to locate .lock files and delete them
    find "$1" -maxdepth 3 -type f -name ".lock" -delete
}

# Check if folder path is provided as parameter
if [ $# -eq 0 ]; then
    echo "Usage: $0 <folder_path>"
    exit 1
fi

folder_path="$1"

# Check if folder exists
if [ -d "$folder_path" ]; then
    # Call function to delete .lock files
    delete_lock_files "$folder_path"
    echo "Deleted .lock files in $folder_path and its subfolders up to depth 3."
else
    echo "Folder not found."
fi
