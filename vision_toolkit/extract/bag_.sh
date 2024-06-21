source ~/catkin_ws/devel/setup.bash


if [ $# -eq 0 ]; then
  echo "Error: Please provide an argument."
  exit 1
fi

index=0
for entry in $(ls -1v /data/$1/cam1/*.bag); do
    if [ "${entry: -4}" != ".bag" ]; then
        continue
    fi
    echo "${entry}"
    python3 ./read_bag_.py --bag "$entry" --cam 1 --save $1 --num $index
    ((index++))
  done

index=0
for entry in $(ls -1v /data/$1/cam2/*.bag); do
    if [ "${entry: -4}" != ".bag" ]; then
        continue
    fi
    echo "${entry}"
    python3 ./read_bag_.py --bag "$entry" --cam 2 --save $1 --num $index
    ((index++))
  done

index=0
for entry in $(ls -1v /data/$1/cam3/*.bag); do
    if [ "${entry: -4}" != ".bag" ]; then
        continue
    fi
    echo "${entry}"
    python3 ./read_bag_.py --bag "$entry" --cam 3 --save $1 --num $index
    ((index++))
  done

index=0
for entry in $(ls -1v /data/$1/cam4/*.bag); do
    if [ "${entry: -4}" != ".bag" ]; then
        continue
    fi
    echo "${entry}"
    python3 ./read_bag_.py --bag "$entry" --cam 4 --save $1 --num $index
    ((index++))
  done

index=0
for entry in $(ls -1v /data/$1/cam5/*.bag); do
    if [ "${entry: -4}" != ".bag" ]; then
        continue
    fi
    echo "${entry}"
    python3 ./read_bag_.py --bag "$entry" --cam 5 --save $1 --num $index
    ((index++))
  done

