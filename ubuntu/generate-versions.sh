#!/bin/bash
set -e

versions_md="$PWD/versions.Modusfile"
echo -n > "$versions_md"
cd upstream.git
for v in */; do
  v=${v%/}
  for arch in $(< $v/arches); do
    echo "ubuntu_version(\"$v\", \"$arch\")." >> "$versions_md"
  done
done
