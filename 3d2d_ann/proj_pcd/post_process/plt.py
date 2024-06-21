import matplotlib.pyplot as plt

# Example dictionaries
import yaml
with open('fre.yaml','r') as f:
    tmp = yaml.safe_load(f)
dict1 = tmp['pcd']
dict2 = tmp['point']

with open('semantic.yaml','r') as f:
    lb = yaml.safe_load(f)['labels']

total=0
for key,value in dict1.items():
    if key!=0:
        total+=value
for key,value in dict1.items():
    if key!=0:
        dict1[key]=value*1.0/total*100
dict1[0] = 0

total=0
for key,value in dict2.items():
    if key!=0:
        total+=value
for key,value in dict2.items():
    if key!=0:
        dict2[key]=value*1.0/total*100
dict2[0] = 0

# Step 1: Sort the keys of dict1 based on their values
sorted_keys = sorted(dict1, key=dict2.get, reverse=True)

# Step 2: Select the top 50 keys (or fewer if there are not enough keys)
top_keys = sorted_keys[:50]

# Step 3: Extract the values from both dictionaries corresponding to these top 50 keys
values_dict1 = [dict1[key] for key in top_keys]
values_dict2 = [dict2[key] for key in top_keys]

print(values_dict1)

# Step 4: Plot the histogram
x = range(len(top_keys))
width = 0.4  # the width of the bars
plt.figure(figsize=(16, 9))
plt.bar(x, values_dict1, width, label='Point Cloud frequency')
plt.bar([i + width for i in x], values_dict2, width, label='Point Frequency')

plt.xlabel('Label')
plt.ylabel('Frequency (%)')
plt.title('Point Cloud and Point Frequency of Semantic Labels')
plt.xticks([i + width / 2 for i in x], [lb[key] for key in top_keys], rotation=60, ha='right', fontsize=10)
plt.legend()

plt.tight_layout()
plt.savefig('top_objects.png')
