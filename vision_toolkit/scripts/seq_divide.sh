#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <date1> <date2> ..."
    exit 1
fi

# Loop through each date argument and run run_divide.sh with it
for date_arg in "$@"; do
    ./run_divide.sh "$date_arg"
done
