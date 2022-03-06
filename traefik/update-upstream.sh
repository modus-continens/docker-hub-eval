#!/usr/bin/env bash

# The upstream git repo has templates for both v1 and v2 releases of the traefik
# image, but the repository only stores one single Dockerfile for each variant.
# Whenever they need to release a new image, they overwrite that Dockerfile and
# update the link in docker hub to point to a specific commit. This means that
# in order to generate the Dockerfiles for both v1 and v2, we need to run their
# script with v1, copy the Dockerfile somewhere, then run the script with v2
# argument.

# This script is run with cwd = upstream.git.

./updatev1.sh v1.7.34
cp alpine/Dockerfile alpine-v1.Dockerfile
cp scratch/Dockerfile scratch-v1.Dockerfile
./updatev2.sh v2.6.1
cp alpine/Dockerfile alpine-v2.Dockerfile
cp scratch/Dockerfile scratch-v2.Dockerfile

cp alpine/entrypoint.sh .
