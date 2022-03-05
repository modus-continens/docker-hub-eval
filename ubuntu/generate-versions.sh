#!/bin/bash
set -e

cd upstream.git
for v in */; do
  v=${v%/}
  for arch in $(< $v/arches); do
    echo "ubuntu_version(\"$v\", \"$arch\")."
  done
done
