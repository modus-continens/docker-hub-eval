#!/usr/bin/env bash

set -xe

parallel <<EOF
docker build --no-cache . -f alpine-v1.Dockerfile -t traefik:v1.7.34-alpine
docker build --no-cache . -f alpine-v2.Dockerfile -t traefik:v2.6.1-alpine
EOF
parallel <<EOF
docker build --no-cache . -f scratch-v1.Dockerfile -t traefik:v1.7.34-scratch
docker build --no-cache . -f scratch-v2.Dockerfile -t traefik:v2.6.1-scratch
EOF
