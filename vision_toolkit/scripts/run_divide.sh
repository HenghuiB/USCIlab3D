
if [ $# -eq 0 ]; then
  echo "Error: Please provide an argument."
  exit 1
fi

for entry in "/lab/tmpig13b/kiran/bag_dump/$1/"*; do
    #python /lab/tmpig10c/kiran/nerf/GNerf/gaussian-splatting/render.py -m "$entry"
    session=$(basename "$entry")
    entry="$entry/all_imgs/"
    python ./divide_sectors.py --data "$entry" --target "/lab/tmpig10b/kiran/gs_train/$1/$session/"
  done



