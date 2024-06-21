import sys
import requests
import json
# Define your API key here
api_key = ""

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
text_query = "I have some objects, could you help me do a classify according to category, similart to semantiKITTI. Please classify every label, if it can be classfied to different category choose the most possible category, and for some objects can't be classfied, put them as 'Unlabeled and Miscellaneous'\n"
text_query += "'window', 'handrail', 'bench', 'sky', 'grass', 'door', 'wall', 'outdoor lighting', 'pipe', 'curb', 'roof', 'tree', 'building', 'shrub', 'concrete', 'pavement', 'door handle', 'stairs', 'shadow', 'pole', 'fence', 'person', 'lamp post', 'railing', 'bicycle', 'potted plant', 'shrubbery', 'drain cover', 'light', 'gravel', 'cover', 'plant', 'lawn', 'umbrella', 'patio umbrella', 'table', 'chair', 'bush', 'planter', 'trash can', 'sidewalk', 'trash', 'parking lot', 'sign', 'vehicle', 'space line', 'portable toilet', 'van', 'parking space line', 'post', 'parking meter', 'path', 'ceiling', 'vegetation', 'banner', 'flower', 'lamp', 'bushes', 'reflection', 'outdoor furniture', 'stone', 'fountain', 'construction barrier', 'stop sign', 'truck', 'entrance', 'street sign', 'hydrant', 'road', 'construction cone', 'bicycle racks', 'branch', 'red curb', 'brick', 'street', 'foliage', 'floor', 'plaque', 'pillar', 'public art', 'gate', 'sun', 'plants', 'concrete wall', 'palm', 'shrubs', 'balcony', 'balustrade', 'fire hydrant', 'sunlight', 'chain', 'rock', 'glass', 'hedge', 'motorcycle', 'trailer', 'fencing', 'unit', 'soil', 'conditioning unit', 'bricks', 'driveway', 'pedestrian walkway', 'parking bay marker', 'crosswalk', 'ramp', 'garden', 'handicap parking sign', 'ground', 'outdoor', 'flower bed', 'parking structure', 'hand', 'pathway', 'pot', 'leaf', 'dumpster', 'manhole cover', 'paving stone', 'parking sign', 'construction site', 'road sign', 'golf cart', 'steps', 'potted', 'staircase', 'leaves', 'air unit', 'cart', 'vent', 'bin', 'road marking', 'planters', 'billboard', 'construction fence', 'handicap parking symbol', 'parking symbol', 'electric box', 'symbol', 'signage', 'stair', 'air', 'cone', 'statue', 'sculpture', 'patio', 'doorway', 'space', 'house', 'lettering', 'walkway', 'portable', 'bollard', 'graffiti', 'ventilation grill', 'scaffolding', 'cross', 'ceiling lights', 'air vent', 'cones', 'bus', 'hydra', 'public phone', 'bay marker', 'greenery', 'plant pot', 'construction', 'container', 'drainage grate', 'warning sign', 'canopy', 'garbage can', 'lot', 'rack', 'flag', 'brickwork', 'gutter', 'water', 'utility meter', 'curtain', 'ladder', 'station', 'metal', 'painting', 'trunk', 'tree trunk', 'blinds', 'stadium', 'pallet', 'yard', 'advertisement', 'locker', 'cardboard box', 'corridor', 'text', 'marker', 'ivy', 'outdoor gear', 'poster', '##ster', 'archway', 'receptacle', 'barrier', 'courtyard', 'mulch', 'generator', 'tank', 'bulletin board', 'garage', 'machine', 'lane marker', 'equipment', 'rail', 'construction materials', 'sports field', 'emergency phone', 'board', 'monument', 'security camera', 'signboard', 'lattice', 'camera', 'waste container', 'base', 'fire', 'architecture', 'structure', 'arch', 'line', 'bleachers', 'meter', 'red', 'hat', 'transportation sign', 'public bench', 'emergency', 'baseball field', 'call', 'tile', 'birds', 'case', 'bottle', 'electric', 'tent', 'green area', 'exterior', 'public space', 'campus', 'closed sign', 'bal', 'field', 'curve', 'bod', 'tire', 'wheels', 'iron', 'call station', 'shade', 'bay', 'bag', 'backpack', 'bed', 'picnic table', 'frame', 'firent', 'box', 'pal', 'exit', 'furniture', 'baseball', 'bucket', 'image', 'security', 'the image', 'security _ camera', 'reservation sign', 'rec', 'sports', 'public', 'piping', 'grill', 'recacle', 'cable', 'basin', 'pavilion', 'materials', 'lighting equipment', 'streelight', 'utility', 'stlight', 'gut', 'skateboard', 'wood', 'toilet', 'railway', 'golf course', 'reservoir', 'feeding station', 'elevator', 'valve', 'phone', 'lantern', 'plastic', 'debris', 'cardboard', 'patch', 'grate', 'blea', 'stroller', 'units', 'recept', 'emergency station', 'picnic', 'electrical'"
payload = {
    "model": "gpt-4",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text_query
                }
            ]
        }
    ],
}
print('??')
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# Handle the response here
print(response.json())


with open('./sam5.txt', 'w') as f:
    json.dump(response.json(), f)
