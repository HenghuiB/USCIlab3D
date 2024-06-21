#!/bin/bash


for entry in "/lab/tmpig13b/kiran/bag_dump/"*; do
    date=$(basename "$entry")
    # if [[ "$date" == "2023_06_20" || "$date" == "2023_06_19" || "$date" == "2023_03_30" || "$date" == "2023_03_29" || "$date" == "2023_03_28" || "$date" == "2023_03_11" ]]; then
    #     continue  # Skip this date and proceed to the next iteration
    # fi
    ./extract_and_gpt4.sh "$date"
  done


