
for entry in "/lab/tmpig13b/kiran/bag_dump/$1/"*; do
    #python /lab/tmpig10c/kiran/nerf/GNerf/gaussian-splatting/render.py -m "$entry"
    python ./extract_and_gpt4.py "$entry"
  done
