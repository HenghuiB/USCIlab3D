
# GPT4

To generate GPT-4 output for a specific date, use the following command:```
./extract_and_gpt4.sh 2023_06_30
```

To process all dates, you can run:
```
./all_got4.sh
```

# projection

To project 3D points to 2D pixels and label them, run the following script:
```
./proj_pcd/proj_final.py --date <date> --session <session> --data_path <data_path> --curr <current_part> --total <total_parts>
```
For parallel processing of data, specify total to indicate the total number of parts into which the data is divided, and curr to specify which part is currently being processed.
