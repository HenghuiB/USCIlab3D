import json
import pandas as pd
import matplotlib.pyplot as plt

label_mapping = {
    # 'buildings': 'building',
    # 'trees': 'tree',
    # 'windows': 'window',
    # 'bushes': 'bush',
    # 'streetlight': 'street lamp',
    # 'shrubs': 'shrub',
    # 'street light': 'street lamp',
    # 'lamp post': 'street lamp',
    # 'street lamps': 'street lamp',
    # 'lights': 'light',
    # 'leaves': 'leaf',
    # 'bicycles': 'bicycle',
    # 'benches': 'bench',
    # 'planters': 'planter',
    # 'streetlights': 'street lamp',
    # 'doors': 'door',
    # 'street sign': 'sign',
    # 'street lights': 'street lamp',
    # '1. building': 'building',  # This seems like a typo, but I'll include it for consistency
    # 'lamp': 'light',
    # 'trash bin': 'trash can',
    # 'parking garage': 'parking lot',  # Assuming similar enough
    # 'light pole': 'light pole',  # No change needed
    # 'cars': 'car',
    # 'chairs': 'chair',
    # 'handrails': 'handrail',
    # 'road markings': 'road marking',
    # 'lighting': 'light',
    # 'glass': 'window',  # Assumption: glass on buildings or windows
    # 'vehicles': 'vehicle',
  "streetlamp": "street light",
  "tree trees": "tree",
  "chairs chair": "chair",
  "umbrella umbrella": "umbrella",
  "newspaper dispenser": "newspaper dispensers",
  "sky": "sky",
  "building": "buildings",
  "table tables": "table",
  "bush": "bushes",
  "bush vegetation bushes": "vegetation",
  "grass": "grass",
  "streetlight street lamp streetlamp": "street light",
  "lamp": "lamp",
  "pedestrian": "pedestrians",
  "street lights": "street lamp",
  "sidewalk": "sidewalk",
  "wall": "wall",
  "palm tree tree trees": "palm tree",
  "the image": "image",
  "buildings building": "buildings",
  "street lamps": "street lamp",
  "lamps umbrella": "lamp",
  "umbrellas": "umbrella",
  "##ted plants": "plants",
  "benches": "bench",
  "plants": "plant",
  "cars car vehicles": "car",
  "street lamps street street lamp": "street lamp",
  "road markings": "road mark",
  "signage": "sign",
  "shrubbery": "shrub",
  "cars vehicles": "car",
  "portable toilet": "toilet",
  "motor scooter": "scooter",
  "door": "door",
  "sign text": "sign",
  "lot street": "street",
  "pathway sidewalk": "sidewalk",
  "pathway": "path",
  "planters planter": "planter",
  "trash cans trash": "trash can",
  "bench benches": "bench",
  "plant planter": "planter",
  "window windows": "window",
  "barrier": "barrier",
  "golf cart": "cart",
  "stairs": "stairs",
  "handrail": "handrail",
  "sign sign traffic sign": "sign",
  "fence": "fence",
  "dumpster": "dumpster",
  "trash can": "bin",
  "brick wall": "wall",
  "roof": "roof",
  "water fountain": "fountain",
  "column": "column",
  "street curb": "curb",
  "plant pot": "planter",
  "bicycle": "bicycle",
  "vehicle": "vehicle",
  "brick wall building": "building",
  "red curb": "curb",
  "lot": "lot",
  "van": "van",
  "car": "vehicle",
  "handicap parking sign": "sign",
  "parking lot pavement": "parking lot",
  "parking spaces": "parking space",
  "light post": "lamp post",
  "cars": "car",
  "path pathway": "path",
  "lamp posts": "lamp post",
  "building brick wall": "building",
  "automobile": "car",
  "##cle bin trash": "trash can",
  "lamps outdoor lamp": "lamp",
  "bins": "bin",
  "doors": "door",
  "portable toilet cone": "toilet",
  "signs": "sign",
  "trailer": "trailer",
  "palm trees tree": "palm tree",
  "lawn": "lawn",
  "light pole": "lamp post",
  "bin": "bin",
  "streetlight": "street light",
  "bench chair": "bench",
  "potted plants": "plant",
  "truck": "truck",
  "handicap sign": "sign",
  "light streetlamp": "street light",
  "office building": "building",
  "street sign": "sign",
  "pavement": "pavement",
  "lamps": "lamp",
  "bollard": "bollard",
  "dumpster bin": "dumpster",
  "patio umbrella": "umbrella",
  "scooter": "scooter",
  "brick pattern": "brick",
  "electric vehicle": "vehicle",
  "outdoor umbrella": "umbrella",
  "crosswalk": "crosswalk",
  "different types": "types",
  "chains": "chain",
  "utility pole": "pole",
  "##lights light fixture": "light",
  "shrubs": "shrub",
  "space": "space",
  "fountain": "fountain",
  "fire hydrant": "hydrant",
  "golf cart bicycle rack": "bicycle rack",
  "bicycle lane": "lane",
  "traffic cone": "cone",
  "people": "people",
  "plaza": "plaza",
  "manhole cover": "manhole cover",
  "portable toilet trailer": "toilet",
  "awning solar panel": "solar panel",
  "cone": "cone",
  "light": "light",
  "handicap sign no parking sign": "sign",
  "awning": "awning",
  "curb parking curb": "curb",
  "recycle bin trash": "recycle bin",
  "traffic signals lamp": "traffic signal",
  "bollard umbrella": "bollard",
  "outdoor lights": "light",
  "path": "path",
  "car car": "car",
  "vegetation": "vegetation",
  "fence dumpster": "dumpster",
  "parking meter": "parking meter",
  "shrubs hedge": "shrub",
  "parking lot street": "parking lot",
  "trash bin": "trash can",
  "barrier construction barrier": "barrier",
  "traffic light streetlight": "traffic light",
  "vehicle car truck": "vehicle",
  "motorcycle": "motorcycle",
  "door window": "window",
  "signs signage": "sign",
  "column street light": "column",
  "railings handrail": "handrail",
  "ramp": "ramp",
  "clock tower": "clock tower",
  "outdoor lamp": "lamp",
  "cars car car": "car",
  "sidewalk curb": "sidewalk",
  "tables": "table",
  "shrub bushes hedge": "shrub",
  "handicap parking symbol": "sign",
  "patio canopy umbrellas": "umbrella",
  "column brick wall": "column"
}

label_mapping = {'window windows': 'windows', 'windows window': 'windows', 'window window': 'window', 'windows': 'windows', 'window': 'window', 'water fountain bin': 'water fountain', 'water fountain': 'water fountain', 'wall wall columns': 'wall building', 'wall wall': 'wall', 'wall building': 'wall building', 'wall': 'wall', 'walkway sidewalk pathway': 'walkway', 'walkway': 'walkway', 'vent grill window': 'vent grill', 'vent grill': 'vent grill', 'vehicles': 'vehicles', 'vehicle vehicles portable toilet': 'vehicles', 'vehicle vehicles portable': 'vehicles', 'vehicle vehicles': 'vehicles', 'vehicle vehicle car': 'vehicles', 'vehicle vehicle': 'vehicles', 'vehicle van': 'van', 'vehicle utility vehicle': 'utility vehicle', 'vehicle truck': 'truck', 'vehicle trailer': 'trailer', 'vehicle station vehicle': 'vehicles', 'vehicle portable': 'vehicles', 'vehicle outdoor': 'vehicles', 'vehicle chairs': 'vehicles', 'vehicle chair': 'vehicles', 'vehicle cars': 'vehicles', 'vehicle car van': 'vehicles', 'vehicle car truck': 'vehicles', 'vehicle car': 'vehicles', 'vehicle': 'vehicles', 'vegetation bushes shrubs': 'vegetation', 'vegetation bushes': 'vegetation', 'vegetation / bushes shrubs': 'vegetation', 'vegetation / bushes': 'vegetation', 'vegetation': 'vegetation', 'van vehicles': 'vehicles', 'van vehicle': 'vehicles', 'van portable toilet': 'vehicles', 'van car': 'vehicles', 'van': 'vehicles', 'utility vehicle car': 'utility vehicle', 'utility vehicle': 'utility vehicle', 'utility pole post pole': 'utility pole', 'utility pole lamp post light pole street': 'utility pole', 'utility pole lamp post light pole': 'utility pole', 'utility pole': 'utility pole', 'utility cart': 'utility cart', 'utility box generator': 'utility box', 'utility box fire': 'utility box', 'utility box': 'utility box', 'units dumpster': 'dumpster', 'units': 'units', 'umbrellas': 'umbrellas', 'umbrella umbrellas patio umbrellas': 'umbrellas', 'umbrella umbrellas awnings': 'umbrellas', 'umbrella umbrellas': 'umbrellas', 'umbrella umbrella umbrella': 'umbrellas', 'umbrella umbrella': 'umbrellas', 'umbrella street umbrella': 'umbrellas', 'umbrella patios': 'umbrellas', 'umbrella patio umbrellas': 'umbrellas', 'umbrella patio': 'umbrellas', 'umbrella outdoor umbrellas': 'umbrellas', 'umbrella bicycle': 'umbrellas', 'umbrella': 'umbrellas', 'trucks van': 'vehicles', 'trucks': 'trucks', 'truck trailer': 'trucks', 'truck': 'trucks', 'trees trees': 'trees', 'trees tree trees': 'trees', 'trees tree buildings building': 'buildings', 'trees tree buildings': 'buildings', 'trees tree building': 'buildings', 'trees tree': 'trees', 'trees shrubs': 'trees', 'trees plant tree': 'trees', 'trees bushes': 'trees', 'trees buildings': 'buildings', 'trees': 'trees', 'tree trees': 'trees', 'tree tree trees': 'trees', 'tree tree': 'trees', 'tree shrubbery': 'trees', 'tree palm trees trees': 'trees', 'tree palm trees': 'trees', 'tree palm tree': 'trees', 'tree palm': 'trees', 'tree lamp post': 'trees', 'tree buildings building': 'buildings', 'tree building trees': 'trees', 'tree building buildings': 'buildings', 'tree building': 'buildings', 'tree': 'trees', 'trashycle bin': 'trash bin', 'trashs': 'trash', 'trashcle bin': 'trash bin', 'trash utility box': 'trash', 'trash trash planter': 'trash', 'trash trash cans': 'trash', 'trash trash': 'trash', 'trash street light': 'trash', 'trash scooter': 'trash', 'trash recycle bin': 'trash', 'trash receptacle trash': 'trash', 'trash reccle bin': 'trash', 'trash portable toilet': 'trash', 'trash portable': 'trash', 'trash meter': 'trash', 'trash handicap': 'trash', 'trash electric station': 'trash', 'trash cansers': 'trash', 'trash cans trash can': 'trash', 'trash cans trash': 'trash', 'trash cans planters': 'trash', 'trash cans': 'trash', 'trash can van': 'trash', 'trash can utility box': 'trash', 'trash can toilet': 'trash', 'trash can portable toilet': 'trash', 'trash can portable': 'trash', 'trash can machine': 'trash', 'trash can electric': 'trash', 'trash can box': 'trash', 'trash can bin': 'trash', 'trash can': 'trash', 'trash bins bin': 'trash bin', 'trash bins': 'trash bin', 'trash bin station': 'trash bin', 'trash bin parking meter': 'trash', 'trash bin meter': 'trash', 'trash bin': 'trash bin', 'trash bench': 'trash', 'trash': 'trash', 'trailer van': 'trailer', 'trailer portable': 'trailer', 'trailer generator': 'trailer', 'trailer': 'trailer', 'traffic signs road sign signage': 'traffic signs', 'traffic signals lamp': 'traffic signals', 'traffic signal streetlight': 'traffic signal', 'traffic sign sign sign': 'traffic sign', 'traffic sign': 'traffic sign', 'traffic light streetlight': 'traffic light', 'traffic light': 'traffic light', 'traffic cone': 'traffic cone','yellow zone': 'yellow zone', 'yellow paint markings': 'markings', 'yellow paint': 'paint', 'yellow lines on ground': 'lines', 'yellow line (marking)': 'line', 'yellow curb': 'curb', 'yellow bollards': 'bollards', 'yellow barrier': 'barrier', 'wooden plank': 'wood', 'wooden pallets': 'wood', 'wooden pallet': 'wood', 'wooden frame': 'frame', 'wooden fence': 'fence', 'wooden crate': 'crate', 'wood planks': 'wood', 'wood chips': 'wood chips', 'windowsill': 'window', 'windows.': 'window', 'windows': 'window', 'windowpanes': 'window', 'windowpane': 'window', 'window.': 'window', 'window-mounted air conditioner': 'air conditioner', 'window trim': 'trim', 'window sill': 'window', 'window reflections': 'window', 'window panes': 'window', 'window ledge': 'window', 'window grate': 'window', 'window frames': 'window', 'window frame': 'window', 'window display': 'window', 'window blinds': 'blinds', 'window blind': 'blind', 'window bars': 'bars', 'window arch': 'arch', 'window air conditioning unit': 'air conditioning unit', 'window (possibly)': 'window', 'window (partially visible)': 'window', 'window (blocked)': 'window', 'window': 'window', 'wood': 'wood', 'water': 'water', 'wall': 'wall', 'wind': 'wind', 'walk': 'walk path', 'vehicles': 'vehicles', 'vent grill': 'vent grill', 'utilities': 'utilities', 'umbrellas': 'umbrellas', 'trucks': 'trucks', 'trailer': 'trailer', 'traffic signs': 'traffic signs', 'traffic signals': 'traffic signals', 'traffic signal': 'traffic signal', 'traffic sign': 'traffic sign', 'traffic light': 'traffic light', 'traffic cone': 'traffic cone', 'yellow zone': 'yellow zone'}

# new_l = {
#     'streetlamp': 'street lamp',
#     'trees': 'tree',
#     'chairs': 'chair',
#     'umbrella': 'umbrella',
#     'newspaper dispenser': 'newspaper dispensers',
#     'sky': 'sky',
#     'table': 'table',
#     'tables': 'table',
#     'bush vegetation': 'bush',
#     'bushes': 'bush',
#     'grass': 'grass',
#     'streetlight': 'street lamp',
#     'lamp': 'light',
#     'pedestrian': 'pedestrian',
#     'street lights': 'street lamp',
#     'sidewalk': 'sidewalk',
#     'wall': 'wall',
#     'palm tree': 'palm tree',
#     'the image': 'the image',
#     'umbrellas': 'umbrella',
#     '##ted plants': '##ted plants',
#     'benches': 'bench',
#     'plants': 'plant',
#     'cars': 'car',
#     'bench': 'bench',
#     'street lamps': 'street lamp',
#     'road markings': 'road marking',
#     'signage': 'sign',
#     'shrubbery': 'shrubbery',
#     'trash': 'trash',
#     'portable toilet': 'portable toilet',
#     'motor scooter': 'motor scooter',
#     'door': 'door',
#     'sign text': 'sign',
#     'lot street': 'parking lot',
#     'pathway': 'pathway',
#     'planters': 'planter',
#     'trash cans': 'trash can',
#     'planter': 'planter',
#     'plant': 'plant',
#     'window': 'window',
#     'person': 'person',
#     'barrier': 'barrier',
#     'golf cart': 'golf cart',
#     'stairs': 'stairs',
#     'street': 'street',
#     'handrail': 'handrail',
#     'fence': 'fence',
#     'dumpster': 'dumpster',
#     'trash can': 'trash can',
#     'brick wall': 'brick wall',
#     'roof': 'roof',
#     'water fountain': 'water fountain',
#     'column': 'column',
#     'street curb': 'street curb',
#     'plant pot': 'plant pot',
#     'bicycle': 'bicycle',
#     'vehicle': 'vehicle',
# }



# for key,value in new_l.items():
#     if key not in label_mapping.keys():
#         label_mapping[key] = value




# Load data from JSON file
with open('labels.json') as f:
    data = json.load(f)

label_sum = 0
for ll in data.values():
    label_sum+=ll


new_dict = {}

for key,value in data.items():
    if key in label_mapping.keys():
        if key=='Sky':
            print('wtf')
            print(label_mapping[key])
            print(value)
        if label_mapping[key] in new_dict.keys():
            new_dict[label_mapping[key]] += value
        else:
            new_dict[label_mapping[key]] = value
    else:
        if key in new_dict.keys():
            new_dict[key] += value
        else:
            new_dict[key] = value

new_dict = dict(sorted(new_dict.items(), key=lambda x: x[1]))

with open('pixel.json') as f:
    pixel = json.load(f)


pixel_sum = 0
for ll in pixel.values():
    pixel_sum+=ll


for key,value in new_dict.items():
    new_dict[key] = {'Image Frequency' : value, 'Pixel Frequency' : 0}

new_dict['sky']['Image Frequency'] = 0
for key,value in pixel.items():
    if key not in new_dict.keys():
        continue
    if key in label_mapping.keys():
        new_dict[label_mapping[key]]['Pixel Frequency'] = value
    else:
        if key in new_dict.keys():
            new_dict[key]['Pixel Frequency'] = value
# Convert data to DataFrame
            
for key,value in new_dict.items():
    new_dict[key]['Image Frequency'] /= label_sum
    new_dict[key]['Pixel Frequency'] /= pixel_sum


df = pd.DataFrame(new_dict.items())


df[['Image Frequency', 'Pixel Frequency']] = pd.DataFrame(df[1].tolist(), index=df.index)

# Sort DataFrame by Image Frequency in descending order
# df = df.sort_values(by='Image Frequency', ascending=False)

df['Total Frequency'] = df['Image Frequency'] + df['Pixel Frequency']

# Sort DataFrame by Total Frequency in descending order
df = df.sort_values(by='Total Frequency', ascending=False)


df = df[df['Pixel Frequency'] != 0]
df = df.head(50)
# Plotting
plt.figure(figsize=(12, 6))
bar_width = 0.35
objects = df[0]
index = range(len(objects))

plt.bar(index, df['Image Frequency'], bar_width, label='Image Frequency', color='skyblue')
plt.bar([i + bar_width for i in index], df['Pixel Frequency'], bar_width, label='Pixel Frequency', color='orange')

plt.xlabel('Semantic labels')
plt.ylabel('Frequency')
plt.title('Image and Pixel Frequency of Semantic labels')
plt.xticks([i + bar_width/2 for i in index], objects, rotation=45, ha='right')
plt.legend()
plt.tight_layout()

# Save the plot as an image
plt.savefig('image_and_pixel_frequency_1.png')


# Sort DataFrame by count in descending order
# df = df.sort_values(by='Count', ascending=False)

# # Plotting
# plt.figure(figsize=(12, 6))
# plt.bar(df['Object'][:50], df['Count'][:50], color='skyblue')
# plt.xlabel('Semantic labels')
# plt.ylabel('Percentage')
# plt.title('Top 50 Semantic labels in the dataset')
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()

# # Save the plot as an image
# plt.savefig('top_objects.png')

# # Show plot
# plt.show()
