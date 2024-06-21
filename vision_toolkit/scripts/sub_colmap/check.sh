#!/bin/bash

# Check if a folder contains a subfolder named "sparse"
check_sparse() {
    local folder="$1"
    if [ -d "$folder/sparse" ]; then
        return 0 # "sparse" folder exists
    else
        return 1 # "sparse" folder does not exist
    fi
}

# Main function to check subfolders of a given directory
check_subfolders() {
    local parent_folder="$1"
    for folder in "$parent_folder"/*/*; do
        if [ -d "$folder" ]; then
            if ! check_sparse "$folder"; then
                echo "Folder $folder does not contain 'sparse' folder."
            fi
            # Recursive call to check subfolders
        fi
    done
}

# Check if argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <parent_folder>"
    exit 1
fi

# Check if provided folder exists
if [ ! -d "$1" ]; then
    echo "Error: '$1' is not a directory."
    exit 1
fi

# Call the main function with the provided folder path
check_subfolders "$1"
