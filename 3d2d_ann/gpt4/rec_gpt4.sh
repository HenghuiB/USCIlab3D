#!/bin/bash

# Initialize counters
total_calls=0
total_time=0

for entry in "/lab/tmpig13b/kiran/bag_dump/"*; do
    date=$(basename "$entry")
    if [[ "$date" != "2024_03_16" ]]; then
        continue  # Skip this date and proceed to the next iteration
    fi
    
    start_time=$(date +%s)  # Record start time
    
    # Call the script and record its output
    output=$(./extract_and_gpt4.sh "$date")
    
    end_time=$(date +%s)  # Record end time
    execution_time=$((end_time - start_time))  # Calculate execution time
    
    # Increment counters
    ((total_calls++))
    total_time=$((total_time + execution_time))

    # Log the execution details
    echo "[$date] Execution time: $execution_time seconds"
    echo "$output"
done

# Log total calls and total time
echo "Total calls to /extract_and_gpt4.sh: $total_calls"
echo "Total execution time: $total_time seconds"
