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

if [ "$IMAGE_PUSH_TO" != "" ]; then
  docker tag traefik:v1.7.34-alpine $IMAGE_PUSH_TO:traefik-dockerfile-v1.7.34-alpine
  docker tag traefik:v2.6.1-alpine $IMAGE_PUSH_TO:traefik-dockerfile-v2.6.1-alpine
  docker tag traefik:v1.7.34-scratch $IMAGE_PUSH_TO:traefik-dockerfile-v1.7.34-scratch
  docker tag traefik:v2.6.1-scratch $IMAGE_PUSH_TO:traefik-dockerfile-v2.6.1-scratch
  docker push $IMAGE_PUSH_TO:traefik-dockerfile-v1.7.34-alpine
  docker push $IMAGE_PUSH_TO:traefik-dockerfile-v2.6.1-alpine
  docker push $IMAGE_PUSH_TO:traefik-dockerfile-v1.7.34-scratch
  docker push $IMAGE_PUSH_TO:traefik-dockerfile-v2.6.1-scratch
fi

docker image rm traefik:v1.7.34-alpine
docker image rm traefik:v2.6.1-alpine
docker image rm traefik:v1.7.34-scratch
docker image rm traefik:v2.6.1-scratch
