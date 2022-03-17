#!/usr/bin/env python3
import subprocess
import csv
import json
import os
from os import path

def system(args):
  print(f"=> {' '.join(args)}")
  subprocess.run(args, check=True, capture_output=False)

SMOKE_TESTS = {
  "mysql": "mysqld --version",
  "node": "node -v",
  "redis": "redis-server --version",
  "traefik": "traefik version",
  "ubuntu": "cat /etc/os-release",
}

repo = "public.ecr.aws/n6d1y9u6/modus-experiment-artifacts"
def run():
  global tags
  with open("output.csv", "wt") as out:
    w = csv.writer(out)
    rm_last = None
    for tag in tags:
      system(["docker", "pull", f"{repo}:{tag}"])
      # if rm_last is not None:
      #   system(["docker", "rmi", rm_last])
      smoke_test_cmd = None
      if "scratch" not in tag:
        for sk, sc in SMOKE_TESTS.items():
          if sk in tag:
            smoke_test_cmd = sc
            break
      if smoke_test_cmd is not None:
        system(["docker", "run", "--rm", "--entrypoint", "sh", f"{repo}:{tag}", "-c", smoke_test_cmd])
      if path.isfile("dive.json"):
        os.remove("dive.json") # dive does not truncate file properly
      system(["dive", "--json", "dive.json", f"{repo}:{tag}"])
      with open("dive.json", "rt") as j:
        obj = json.load(j)
        eff = obj["image"]["efficiencyScore"]
        size = obj["image"]["sizeBytes"]
        w.writerow([tag, size, eff])
      rm_last = f"{repo}:{tag}"

# docker image ls --no-trunc --format '{{.Repository}}:{{.Tag}}' | grep ecr.aws
tags = """\
mysql-dockerfile-5.7-Dockerfile.debian
mysql-dockerfile-5.7-Dockerfile.oracle
mysql-dockerfile-8.0-Dockerfile.debian
mysql-dockerfile-8.0-Dockerfile.oracle
mysql-modus-5.7-debian-buster-amd64
mysql-modus-5.7-oracle-7-slim-amd64
mysql-modus-8.0-debian-buster-amd64
mysql-modus-8.0-oracle-8-slim-amd64
nginx-dockerfile-mainline_alpine-Dockerfile
nginx-dockerfile-mainline_alpine-perl-Dockerfile
nginx-dockerfile-mainline_debian-Dockerfile
nginx-dockerfile-mainline_debian-perl-Dockerfile
nginx-dockerfile-stable_alpine-Dockerfile
nginx-dockerfile-stable_alpine-perl-Dockerfile
nginx-dockerfile-stable_debian-Dockerfile
nginx-dockerfile-stable_debian-perl-Dockerfile
nginx-modus-mainline-alpine-false
nginx-modus-mainline-alpine-true
nginx-modus-mainline-debian-false
nginx-modus-mainline-debian-true
nginx-modus-stable-alpine-false
nginx-modus-stable-alpine-true
nginx-modus-stable-debian-false
nginx-modus-stable-debian-true
node-dockerfile-12_alpine3.14-Dockerfile
node-dockerfile-12_alpine3.15-Dockerfile
node-dockerfile-12_bullseye-Dockerfile
node-dockerfile-12_bullseye-slim-Dockerfile
node-dockerfile-12_buster-Dockerfile
node-dockerfile-12_buster-slim-Dockerfile
node-dockerfile-12_stretch-Dockerfile
node-dockerfile-12_stretch-slim-Dockerfile
node-dockerfile-14_alpine3.14-Dockerfile
node-dockerfile-14_alpine3.15-Dockerfile
node-dockerfile-14_bullseye-Dockerfile
node-dockerfile-14_bullseye-slim-Dockerfile
node-dockerfile-14_buster-Dockerfile
node-dockerfile-14_buster-slim-Dockerfile
node-dockerfile-14_stretch-Dockerfile
node-dockerfile-14_stretch-slim-Dockerfile
node-dockerfile-16_alpine3.14-Dockerfile
node-dockerfile-16_alpine3.15-Dockerfile
node-dockerfile-16_bullseye-Dockerfile
node-dockerfile-16_bullseye-slim-Dockerfile
node-dockerfile-16_buster-Dockerfile
node-dockerfile-16_buster-slim-Dockerfile
node-dockerfile-16_stretch-Dockerfile
node-dockerfile-16_stretch-slim-Dockerfile
node-dockerfile-17_alpine3.14-Dockerfile
node-dockerfile-17_alpine3.15-Dockerfile
node-dockerfile-17_bullseye-Dockerfile
node-dockerfile-17_bullseye-slim-Dockerfile
node-dockerfile-17_buster-Dockerfile
node-dockerfile-17_buster-slim-Dockerfile
node-dockerfile-17_stretch-Dockerfile
node-dockerfile-17_stretch-slim-Dockerfile
node-modus-12.22.10-alpine3.14-amd64-1.22.17
node-modus-12.22.10-alpine3.15-amd64-1.22.17
node-modus-12.22.10-bullseye-amd64-1.22.17
node-modus-12.22.10-bullseye-slim-amd64-1.22.17
node-modus-12.22.10-buster-amd64-1.22.17
node-modus-12.22.10-buster-slim-amd64-1.22.17
node-modus-12.22.10-stretch-amd64-1.22.17
node-modus-12.22.10-stretch-slim-amd64-1.22.17
node-modus-14.19.0-alpine3.14-amd64-1.22.17
node-modus-14.19.0-alpine3.15-amd64-1.22.17
node-modus-14.19.0-bullseye-amd64-1.22.17
node-modus-14.19.0-bullseye-slim-amd64-1.22.17
node-modus-14.19.0-buster-amd64-1.22.17
node-modus-14.19.0-buster-slim-amd64-1.22.17
node-modus-14.19.0-stretch-amd64-1.22.17
node-modus-14.19.0-stretch-slim-amd64-1.22.17
node-modus-16.14.0-alpine3.14-amd64-1.22.17
node-modus-16.14.0-alpine3.15-amd64-1.22.17
node-modus-16.14.0-bullseye-amd64-1.22.17
node-modus-16.14.0-bullseye-slim-amd64-1.22.17
node-modus-16.14.0-buster-amd64-1.22.17
node-modus-16.14.0-buster-slim-amd64-1.22.17
node-modus-16.14.0-stretch-amd64-1.22.17
node-modus-16.14.0-stretch-slim-amd64-1.22.17
node-modus-17.7.1-alpine3.14-amd64-1.22.17
node-modus-17.7.1-alpine3.15-amd64-1.22.17
node-modus-17.7.1-bullseye-amd64-1.22.17
node-modus-17.7.1-bullseye-slim-amd64-1.22.17
node-modus-17.7.1-buster-amd64-1.22.17
node-modus-17.7.1-buster-slim-amd64-1.22.17
node-modus-17.7.1-stretch-amd64-1.22.17
node-modus-17.7.1-stretch-slim-amd64-1.22.17
redis-dockerfile-5_32bit-Dockerfile
redis-dockerfile-5_alpine-Dockerfile
redis-dockerfile-5-Dockerfile
redis-dockerfile-6.0_alpine-Dockerfile
redis-dockerfile-6.0-Dockerfile
redis-dockerfile-6.2_alpine-Dockerfile
redis-dockerfile-6.2-Dockerfile
redis-dockerfile-7.0-rc_alpine-Dockerfile
redis-dockerfile-7.0-rc-Dockerfile
redis-modus-5.0.14-
redis-modus-5.0.14-32bit
redis-modus-5.0.14-alpine
redis-modus-6.0.16-
redis-modus-6.0.16-alpine
redis-modus-6.2.6-
redis-modus-6.2.6-alpine
redis-modus-7.0-rc2-
redis-modus-7.0-rc2-alpine
traefik-dockerfile-v1.7.34-alpine
traefik-dockerfile-v1.7.34-scratch
traefik-dockerfile-v2.6.1-alpine
traefik-dockerfile-v2.6.1-scratch
traefik-modus-1.7.34-alpine-amd64
traefik-modus-1.7.34-scratch-amd64
traefik-modus-2.6.1-alpine-amd64
traefik-modus-2.6.1-scratch-amd64
ubuntu-dockerfile-bionic-Dockerfile
ubuntu-dockerfile-focal-Dockerfile
ubuntu-dockerfile-impish-Dockerfile
ubuntu-dockerfile-jammy-Dockerfile
ubuntu-dockerfile-trusty-Dockerfile
ubuntu-dockerfile-xenial-Dockerfile
ubuntu-modus-bionic
ubuntu-modus-focal
ubuntu-modus-impish
ubuntu-modus-jammy
ubuntu-modus-trusty
ubuntu-modus-xenial""".splitlines()

run()
