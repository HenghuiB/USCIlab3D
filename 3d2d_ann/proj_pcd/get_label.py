import os
import pickle
import sys
from os.path import join, basename
input = sys.argv[1]

all = ['sky', 'building', 'tree', 'sidewalk', 'window', 'grass', 'fence', 'path', 'bench', 'bush', 'vehicle', 'streetlight', 'door', 'wall', 'trash can', 'brick wall', 'handrail', 'pavement', 'sign', 'curb', 'plant', 'lamp post', 'railing', 'shadow', 'stairs', 'shrub', 'person', 'fire hydrant', 'crosswalk', 'light', 'ceiling', 'planter', 'bicycle', 'reflection', 'table', 'umbrella', 'brick', 'parking lot', 'chair', 'stop sign', 'pillar', 'banner', 'dumpster', 'red curb', 'vegetation', 'roof', 'lamp', 'staircase', 'floor', 'trash bin', 'street sign', 'flower', 'pipe', 'balcony', 'palm tree', 'traffic cone', 'manhole cover', 'parking garage', 'road marking', 'glass', 'bollard', 'gate', 'lawn', 'concrete', 'sun', 'construction barrier', 'paving stone', 'recycling bin', 'fountain', 'electric box', 'truck', 'scaffolding', 'traffic sign', 'van', 'pedestrian', 'sunlight', 'handicap parking sign', 'traffic light', 'sculpture', 'security camera', 'plaque', 'rock', 'trailer', 'patio umbrella', 'parking sign', 'poster', 'golf cart', 'tent', 'picnic table', 'parking meter', 'construction site', 'text', 'flag', 'barrier', 'portable toilet', 'ramp', 'potted plant', 'pole', 'brickwork', 'air conditioning unit', 'bike rack', 'house', 'vent', 'bus stop', 'statue', 'bulletin board', 'awning', 'porch', 'motorcycle', 'tarp', 'outdoor lighting', 'construction fence', 'soil', 'air conditioner', 'parking space line', 'road sign', 'ceiling light', 'hydrant', 'patio', 'signpost', 'concrete wall', 'leaf', 'construction equipment', 'water', 'bus stop shelter', 'ceiling lights', 'gravel', 'chain-link fence', 'corridor', 'canopy', 'clock tower', 'concrete floor', 'backpack', 'doorway', 'ivy', 'bus', 'pallet', 'metal fence', 'gutter', 'trash receptacle', 'exit sign', 'mulch', 'metal', 'clouds', 'ladder', 'emergency phone', 'ventilation grille', 'mailbox', 'human', 'scooter', 'handicap parking space', 'tank', 'signboard', 'rubble', 'traffic lights', 'plant pot', 'flagpole', 'lamp posts', 'parking structure', 'chain', 'generator', 'emergency call station', 'flower bed', 'fencing', 'driveway', 'air conditioning units', 'pickup truck', 'outdoor light', 'door handle', 'advertisement', 'storage tank', 'pebbles', 'building exterior', 'drain cover', 'flooring', 'stone', 'interior lighting', 'cable', 'billboard', 'curtain', 'corner', 'construction materials', 'flowerbed', 'warning sign', 'park bench', 'balustrade', 'cart', 'crane', 'chain link', 'trash bag', 'metal gate', 'graffiti', 'reserved parking sign', 'concrete planter', 'bicycle racks', 'garbage can', 'monument', 'speed limit sign', 'paper', 'shrubbery', 'cardboard box', 'stones', 'bag', 'ventilation grill', 'manhole cover', 'glass reflection', 'drainage grate', 'blinds', 'solar panel', 'outdoor seating', 'pedestrian crosswalk', 'forklift', 'pergola', 'valve', 'barbed wire', 'waste container', 'surveillance camera', 'utility meter', 'signage', 'lettering', 'handicap parking symbol', 'lamp', 'birds', 'feeding station', 'debris', 'public seating', 'public art', 'entrance', 'public bathroom', 'fence', 'outdoor gear', 'outdoor clothing', 'picnic bench', 'golf course', 'sports field', 'recreational vehicle', 'transportation sign', 'pedestrian walkway', 'restaurant sign', 'construction cone', 'parking bay', 'outdoor furniture', 'stadium', 'lane marker', 'parking bay marker', 'air vent', 'archway', 'public phone', 'closed sign', 'emergency vehicle', 'drinking station', 'traffic bollard', 'rental bikes', 'gun', 'hat', 'girl', 'boy']

def extract_and_call_script(folder_path, script_path="./vision_gpt4.py"):
    # Check if the folder exists
    sam_path = join(folder_path, 'SAM/')

    if not os.path.exists(sam_path):
        print(f"Error: Folder '{folder_path}' error.")
        return

    all_labels = []
    files = os.listdir(sam_path)
    print(len(files))
    for idx, SAM in enumerate(files):
        print(idx)
        if os.path.exists(join(sam_path, SAM, 'labels')):
            with open(join(sam_path, SAM, 'labels'), 'rb') as f:
                label = pickle.load(f)
            all_labels += label
    return all_labels

c = extract_and_call_script(input)
for i in c:
    if i[:-6] and i[:-6] not in all:
        print(i)