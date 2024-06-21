
import os
import sys
import openai
import pandas as pd
from IPython import embed
from ast import literal_eval
import numpy as np
pd.options.display.max_colwidth = 275
import json

import base64
import requests

# OpenAI API Key
api_key = ""

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

labels="'sky', 'building', 'tree', 'sidewalk', 'window', 'grass', 'fence', 'path', 'bench', 'bush', 'vehicle', 'streetlight', 'door', 'wall', 'trash can', 'brick wall', 'handrail', 'pavement', 'sign', 'curb', 'plant', 'lamp post', 'railing', 'shadow', 'stairs', 'shrub', 'person', 'fire hydrant', 'crosswalk', 'light', 'ceiling', 'planter', 'bicycle', 'reflection', 'table', 'umbrella', 'brick', 'parking lot', 'chair', 'stop sign', 'pillar', 'banner', 'dumpster', 'red curb', 'vegetation', 'roof', 'lamp', 'staircase', 'floor', 'trash bin', 'street sign', 'flower', 'pipe', 'balcony', 'palm tree', 'traffic cone', 'manhole cover', 'parking garage', 'road marking', 'glass', 'bollard', 'gate', 'lawn', 'concrete', 'sun', 'construction barrier', 'paving stone', 'recycling bin', 'fountain', 'electric box', 'truck', 'scaffolding', 'traffic sign', 'van', 'pedestrian', 'sunlight', 'handicap parking sign', 'traffic light', 'sculpture', 'security camera', 'plaque', 'rock', 'trailer', 'patio umbrella', 'parking sign', 'poster', 'golf cart', 'tent', 'picnic table', 'parking meter', 'construction site', 'text', 'flag', 'barrier', 'portable toilet', 'ramp', 'potted plant', 'pole', 'brickwork', 'air conditioning unit', 'bike rack', 'house', 'vent', 'bus stop', 'statue', 'bulletin board', 'awning', 'porch', 'motorcycle', 'tarp', 'outdoor lighting', 'construction fence', 'soil', 'air conditioner', 'parking space line', 'road sign', 'ceiling light', 'hydrant', 'patio', 'signpost', 'concrete wall', 'leaf', 'construction equipment', 'water', 'bus stop shelter', 'ceiling lights', 'gravel', 'chain-link fence', 'corridor', 'canopy', 'clock tower', 'concrete floor', 'backpack', 'doorway', 'ivy', 'bus', 'pallet', 'metal fence', 'gutter', 'trash receptacle', 'exit sign', 'mulch', 'metal', 'clouds', 'ladder', 'emergency phone', 'ventilation grille', 'mailbox', 'human', 'scooter', 'handicap parking space', 'tank', 'signboard', 'rubble', 'traffic lights', 'plant pot', 'flagpole', 'lamp posts', 'parking structure', 'chain', 'generator', 'emergency call station', 'flower bed', 'fencing', 'driveway', 'air conditioning units', 'pickup truck', 'outdoor light', 'door handle', 'advertisement', 'storage tank', 'pebbles', 'building exterior', 'drain cover', 'flooring', 'stone', 'interior lighting', 'cable', 'billboard', 'curtain', 'corner', 'construction materials', 'flowerbed', 'warning sign', 'park bench', 'balustrade', 'cart', 'crane', 'chain link', 'trash bag', 'metal gate', 'graffiti', 'reserved parking sign', 'concrete planter', 'bicycle racks', 'garbage can', 'monument', 'speed limit sign', 'paper', 'shrubbery', 'cardboard box', 'stones', 'bag', 'ventilation grill', 'manhole cover', 'glass reflection', 'drainage grate', 'blinds', 'solar panel', 'outdoor seating', 'pedestrian crosswalk', 'forklift', 'pergola', 'valve', 'barbed wire', 'waste container', 'surveillance camera', 'utility meter', 'signage', 'lettering', 'handicap parking symbol', 'lamp', 'birds', 'feeding station', 'debris', 'public seating', 'public art', 'entrance', 'public bathroom', 'fence', 'outdoor gear', 'outdoor clothing', 'picnic bench', 'golf course', 'sports field', 'recreational vehicle', 'transportation sign', 'pedestrian walkway', 'restaurant sign', 'construction cone', 'parking bay', 'outdoor furniture', 'stadium', 'lane marker', 'parking bay marker', 'air vent', 'archway', 'public phone', 'closed sign', 'emergency vehicle', 'drinking station', 'traffic bollard', 'rental bikes', 'gun', 'hat', 'girl', 'boy'"
# Path to your image
image_path = sys.argv[1]
output_path = sys.argv[2]
# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# payload = {
#     "model": "gpt-4-vision-preview",
#     "messages": [
#       {
#         "role": "user",
#         "content": [
#           {
#             "type": "text",
#             "text": "List every possible semantic class that exists in the scene. List only the names and nothing else, split by comma and make words consice."
#           },
#           {
#             "type": "image_url",
#             "image_url": {
#               "url": f"data:image/jpeg;base64,{base64_image}"
#             }
#           }
#         ]
#       }
#     ],
#     "max_tokens": 300
# }


payload = {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "I will give you a list of semantic class, list every possible semantic class that exists in the scene. List only the names and nothing else, split by comma.\n"+labels
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
}


if os.path.exists(image_path.split('/')[-1].split('.')[0]+'.txt'):
    sys.exit(0)
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

with open(os.path.join(output_path, image_path.split('/')[-1].split('.')[0]+'.txt'), 'w') as f:
    json.dump(response.json(), f)

