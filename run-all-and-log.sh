#!/usr/bin/env bash

# Usage: ./run-all-and-log.sh [N]
# where N is the number of times to repeat the experiment
# default is 100

set -x
mkdir runlog || true
N=${1:-100}
for i in $(seq 1 $N); do
  for j in ubuntu redis node mysql traefik nginx; do
    ./run-all.py $j > runlog/$i-$j.log
    sleep 1
  done
done
