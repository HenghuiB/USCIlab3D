import json

# File path to the JSON data
file_path = "labels.json"

# Reading JSON data from the file
with open(file_path, "r") as json_file:
    data = json.load(json_file)

with open('keys.txt','w') as f:
    f.write(str(list(data.keys())[:100]))
