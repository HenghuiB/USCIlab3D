#!/bin/bash

# Start time
start_time=$(date +%s)

# Function to process each folder
process_folder() {
    folder="$1"
    echo $folder
    python ./convert_2.py -s "$folder"
}

# Export the function to make it available to GNU Parallel
export -f process_folder

# Run GNU Parallel to execute the loop with 12 threads
parallel -j 4 process_folder ::: /lab/tmpig10b/kiran/gs_train/partest/0/*

# End time
end_time=$(date +%s)

# Calculate runtime
runtime=$((end_time - start_time))

# Print runtime
echo "Total runtime: $runtime seconds"
