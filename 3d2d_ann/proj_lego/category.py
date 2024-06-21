Vehicle= ['vehicle', 'bicycle', 'van', 'truck', 'motorcycle', 'golf cart', 'bus', 'car', 'skateboard']
Nature= ['sky', 'grass', 'tree', 'shrub', 'shrubbery', 'hedge','trunk','tree trunk','green area', 'birds', 'bush', 'yard', 'plant', 'sun', 'palm', 'rock', 'soil', 'leaf', 'leaves', 'water', 'flower', 'branch', 'bushes', 'vegetation', 'bird', 'ivy']
Human= ['person', 'hand']
Ground= ['pavement', 'curb', 'gravel', 'rail', 'sidewalk', 'street', 'walkway', 'floor', 'road', 'pedestrian walkway', 'crosswalk', 'ramp', 'garden', 'ground', 'pathway', 'paving stone', 'golf course', 'parking lot', 'drainage grate', 'mulch']
Structure= ['pipe', 'roof', 'building', 'sports field', 'campus', 'toilet', 'baseball field', 'architecture', 'monument', 'structure', 'courtyard', 'fountain', 'public space', 'construction', 'emergency station', 'ceiling', 'fence', 'gate', 'wall', 'balcony', 'container', 'stadium', 'lattice', 'shed', 'house', 'construction site', 'parking structure', 'garage', 'scaffolding', 'archway', 'call station']
Street_Furniture= ['bench', 'pole', 'feeding station', 'patio', 'handicap', 'barrier', 'hydrant', 'construction cone', 'construction barrier', 'lamp post', 'lamp', 'trash can',  'recept', 'sign', 'parking meter', 'public art', 'statue', 'sculpture', 'bollard', 'bus stop', 'park bench']
Architectural_Elements= ['window', 'door', 'elevator', 'gutter', 'bleachers', 'tank', 'generator', 'utility meter', 'corridor', 'stair', 'ventilation grill', 'door handle', 'entrance', 'post','air unit',  'pillar', 'balustrade', 'handrail', 'drain cover', 'manhole cover', 'vent', 'air vent', 'arch', 'sill', 'doorway', 'baluster', 'security _ camera', 'electric box']
General_Objects= ['umbrella', 'table', 'chair', 'stroller', 'furniture', 'board','bottle', 'canopy', 'outdoor gear', 'pot', 'rack', 'flag', 'locker', 'ladder', 'garbage', 'bulletin board', 'pallet', 'planter',  'curtain', 'blinds', 'cardboard box', 'tire', 'wheels', 'bag', 'bed', 'frame', 'bucket', 'painting', 'poster', 'advertisement', 'station', 'machine', 'equipment', 'tent', 'base', 'hat']
Signs_and_Symbols= ['shadow', 'reflection', 'traffic cone', 'parking space line', 'space line', 'road marking', 'parking symbol', 'stop sign', 'street sign', 'road sign', 'symbol', 'plaque', 'banner', 'graffiti', 'waste container', 'signboard', 'security camera', 'camera', 'warning sign', 'fire safety sign', 'transportation sign', 'handicap sign', 'closed sign', 'exit sign', 'parking sign', 'reservation sign', 'rec sign']
Materials= ['concrete', 'brick', 'construction materials', 'stone', 'wood', 'plastic', 'metal', 'glass', 'iron', 'materials']
Lighting= ['outdoor lighting', 'light',  'street light', 'indoor light', 'lantern', 'sunlight', 'shade']
Miscellaneous=['cover', 'trash', 'outdoor', 'chain', 'unit', 'security', 'exterior', 'fire', 'electric', 'meter', 'lettering','text', 'potted', 'space', 'portable', 'cone','stlight', 'cross', 'marker', 'grate', 'blea', 'stoller', 'units', 'picnic', 'electrical', 'cable', 'basin', 'pavilion', '##ster', 'bal', 'field', 'curve', 'bod', 'bay', 'pal', 'firent', 'box', 'exit', 'baseball', 'image', 'rec', 'sports', 'public', 'piping', 'grill', 'guttering', 'utility', 'call', 'case', 'recacle', 'gut', 'hydra', 'air', 'line', 'tile', 'cardboard', 'patch', 'reservoir',  'valve', 'phone', 'debris',  'railway']
# Miscellaneous = list(set(Miscellaneous))

a = Vehicle + Nature + Human + Ground + Structure + Street_Furniture + Architectural_Elements + General_Objects + Signs_and_Symbols + Materials + Lighting

a += Miscellaneous
seen = set()
duplicates = set()
for item in Miscellaneous:
    if item in seen:
        duplicates.add(item)
    else:
        seen.add(item)
print(duplicates)
import yaml

with open('./semantic.yaml', 'r') as file:
    data_loaded = yaml.safe_load(file)
    label_idx = data_loaded['labels']

for i in label_idx.values():
    if i not in a:
        print(i)



      