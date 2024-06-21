
for entry in "/lab/tmpig13b/kiran/bag_dump/$1/"*; do
    #python /lab/tmpig10c/kiran/nerf/GNerf/gaussian-splatting/render.py -m "$entry"
    session=$(basename "$entry")
    entry="$entry/all_imgs/"
    python ./sync_cam2.py --data "$entry" --target "/lab/tmpig13b/kiran/bag_dump/$1/$session/"
  done
