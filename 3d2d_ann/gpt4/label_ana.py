import os
import shutil
from os.path import join,basename
import argparse
import json
parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str)
parser.add_argument('--output', type=str)
args = parser.parse_args()



dates=[]

for fn in os.listdir(args.input):
    if os.path.isdir(join(args.input, fn)):
        dates.append(join(args.input, fn))

# dates = ['/data/2023_12_18' ,'/data/2023_12_20', '/data/2023_12_24', '/data/2024_03_16']
res = {}


for date in dates:
    for session in os.listdir(date):
        txts_path = join(date, session, 'text_gpt4')
        for txt in os.listdir(txts_path):
            txt_path = join(txts_path,txt)
            with open(txt_path, 'r') as file:
                try:
                    data = json.load(file)
                    content = data['choices'][0]['message']['content']
                    content = content.replace('- ','')
                    items_list = [item.strip().lower() for part in content.split('\n') for item in part.split(',')]
                    
                    if len(items_list)<3:
                        continue
                    for item in items_list:
                        if len(item.split(' '))>8:
                            continue
                        res[item] = res.get(item, 0)+1
                except:
                    continue
 
res = dict(sorted(res.items(), key=lambda x: x[1], reverse=True))
with open(args.output, "w") as json_file:
    json.dump(res, json_file)



