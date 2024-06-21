
import yaml

with open('./semantic_res.yaml', 'r') as file:
    data_loaded = yaml.safe_load(file)
    label_idx = data_loaded['labels']

label_inverse = {}
for key,value in label_idx.items():
    label_inverse[value] = key


with open('./merge.yaml', 'r') as file:
    data_loaded = yaml.safe_load(file)
    a = data_loaded
print(label_idx[282] in a.keys())
print(a[label_idx[282]])


lb_map = {}
for key, value in label_idx.items():
    if value in a.keys():
        if a[value] in label_idx.values():
            lb_map[key] = label_inverse[a[value]]
    # else:
        # print(value)
# print(lb_map)