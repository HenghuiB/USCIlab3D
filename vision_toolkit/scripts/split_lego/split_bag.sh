#!/bin/bash

# Ensure the user provides the necessary arguments
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <base_directory> <input_bag> <output_path>"
  exit 1
fi

BASE_DIR=$1
INPUT_BAG=$2
OUTPUT_PATH=$3
ERROR_LOG="error_log.txt"
# Ensure the output path exists
mkdir -p "$OUTPUT_PATH"

# Iterate through each 'sector' folder
for sector in "$BASE_DIR"/sector*; do
  if [ -d "$sector/input" ]; then
    input_dir="$sector/input"
    
    # Initialize variables to hold the min and max timestamps
    min_time=""
    max_time=""
    
    # Iterate through 'cam1' images and extract timestamps
    for img in "$input_dir"/cam1_*.jpg; do
      if [[ "$img" =~ cam1_([0-9]+)\.jpg ]]; then
        timestamp="${BASH_REMATCH[1]}"
        
        # Convert timestamp to required format
        formatted_time=$(echo "$timestamp" | sed 's/^\([0-9]\{10\}\)\([0-9]*\)$/\1.\2/')
        
        # Update min and max times
        if [ -z "$min_time" ] || [ "$formatted_time" \< "$min_time" ]; then
          min_time="$formatted_time"
        fi
        
        if [ -z "$max_time" ] || [ "$formatted_time" \> "$max_time" ]; then
          max_time="$formatted_time"
        fi
      fi
    done
    
    # Check if we found any valid timestamps
    if [ -n "$min_time" ] && [ -n "$max_time" ]; then
      echo "Sector: $(basename "$sector")"
      echo "Min cam1 time: $min_time"
      echo "Max cam1 time: $max_time"
      
      # Define output bag file path
      output_bag="$OUTPUT_PATH/$(basename "$sector")_output.bag"
      
      # Run the rosbag filter command
      echo "Running rosbag filter for sector $(basename "$sector")"
      rosbag filter "$INPUT_BAG" "$output_bag" "t.to_sec() >= $min_time and t.to_sec() <= $max_time"
      
      # Write min and max times to a text file in the output path
      echo "Min time: $min_time" > "$OUTPUT_PATH/$(basename "$sector")_times.txt"
      echo "Max time: $max_time" >> "$OUTPUT_PATH/$(basename "$sector")_times.txt"
    else
      echo "No valid cam1 images found in $OUTPUT_PATH $(basename "$sector")" | tee -a "$ERROR_LOG"
    fi
  else
    echo "Input directory not found in sector $OUTPUT_PATH $(basename "$sector")" | tee -a "$ERROR_LOG"
  fi
done
