#!/usr/bin/env bash

set -x
mkdir runlog || true
for i in $(seq 1 100); do
  for j in ubuntu redis node mysql traefik nginx; do
    ./run-all.py $j > runlog/$i-$j.log
    sleep 1
  done
done
