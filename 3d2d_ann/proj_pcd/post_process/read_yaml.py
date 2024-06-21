import yaml

with open('./semantic.yaml', 'r') as file:
    data_loaded = yaml.safe_load(file)
    label_idx = data_loaded['labels']
    color_idx = data_loaded['color_map']
# print(label_idx.values())


a = "1. Architectural Components:\n   - 'window', 'door', 'wall', 'roof', 'stairs', 'pole', 'lamp post', 'shrub', 'balustrade', 'ceiling', 'handrail', 'railing', 'staircase', 'door handle', 'pillar', 'balcony', 'archway', 'doorway'\n\n2. Outdoors & Open Spaces:\n   - 'sky', 'grass', 'park', 'tree', 'bench', 'outdoor lighting', 'pipe', 'curb', 'parking lot', 'sidewalk', 'plant', 'lawn', 'path', 'vegetation', 'flowers', 'street', 'pathway', 'garden', 'outdoor', 'golf course'\n\n3. Buildings & Structures:\n   - 'building', 'house', 'construction barrier', 'entrance', 'portable toilet', 'construction cone', 'public art', 'gate', 'construction site', 'building', 'parking structure', 'construction materials', 'garage', 'stadium', 'advertisement', 'locker', 'container', 'station', 'arch', 'lattice', 'architecture', 'structure'\n\n4. Street & Roadway Elements:\n   - 'sign', 'vehicle', 'space line', 'van', 'parking space line', 'post', 'parking meter', 'road', 'bicycle racks', 'red curb', 'street sign', 'crosswalk', 'ramp', 'road sign', 'parking bay marker', 'handicap parking sign', 'parking sign', 'handicap parking symbol', 'parking symbol', 'road marking', 'transportation sign', 'lane marker'\n\n5. Vegetation:\n   - 'potted plant', 'shrubbery', 'bush', 'planter', 'tree', 'plant', 'plants', 'leaf', 'shrub', 'bushes', 'foliage', 'ivy', 'greenery', 'palm', 'shrubs', 'grass', 'branch' \n\n6. Furniture:\n   - 'table', 'chair', 'outdoor furniture', 'patio umbrella', 'picnic table', 'furniture', 'public bench'\n\n7. Waste Management:\n   - 'trash can', 'trash', 'waste container', 'dumpster', 'garbage can'\n\n8. Lighting:\n   - 'outdoor lighting', 'light', 'lamp post', 'lamp', 'ceiling lights', 'lighting equipment', 'streelight'\n\n9. Miscellaneous Outdoor Objects:\n   - 'umbrella', 'bicycle', 'drain cover', 'gravel', 'cover', 'reflection', 'rock', 'signage', 'flag', 'yard'\n\n10. Miscellaneous Indoor Objects:\n   - 'air vent', 'vent', 'blinds', 'image', 'monument', 'signboard', 'camera', 'ladder'\n\n11. Vehicles:\n   - 'vehicle', 'van', 'truck', 'bicycle', 'golf cart', 'cart', 'motorcycle', 'trailer', 'bus'"
a = [i.split('\n   - ') for i in a.split('\n\n')]
res = {}
for i in a:
    words = i[1].split(', ')
    for word in words:
        word = word[1:-1]
        if word not in label_idx.values():
            print(word)
        res[word] = i[0]
print(len(res.keys()))
