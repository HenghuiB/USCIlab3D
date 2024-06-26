#!/bin/bash


for entry in "/lab/tmpig13b/kiran/bag_dump/"*; do
    date=$(basename "$entry")
    ./extract_and_gpt4.sh "$date"
  done


