import json

# File path to the JSON data
file_path = "pixel_not.json"


# Reading JSON data from the file
with open(file_path, "r") as json_file:
    data = json.load(json_file)

with open ('px.txt', 'w') as f:
    f.write(str(sorted(data.keys(), reverse=True)[:300]))
