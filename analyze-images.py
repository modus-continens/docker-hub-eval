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
      if rm_last is not None:
        system(["docker", "rmi", rm_last])
      smoke_test_cmd = None
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
        w.writerow([tag, eff])
      rm_last = f"{repo}:{tag}"

# aws ecr-public describe-image-tags --repository-name 'modus-experiment-artifacts' --region us-east-1 | jq -r '.imageTagDetails[].imageTag'
tags = [
  "node-dockerfile-12_buster-slim-Dockerfile",
  "redis-dockerfile-6.2-Dockerfile",
  "ubuntu-modus-jammy",
  "redis-modus-5.0.14-",
  "traefik-dockerfile-v1.7.34-alpine",
  "traefik-dockerfile-v2.6.1-alpine",
  "node-dockerfile-16_alpine3.14-Dockerfile",
  "redis-dockerfile-7.0-rc-Dockerfile",
  "mysql-modus-8.0-debian-buster-amd64",
  "node-modus-14.19.0-stretch-amd64-1.22.17",
  "redis-modus-7.0-rc2-alpine",
  "redis-modus-6.2.6-",
  "mysql-dockerfile-8.0-Dockerfile.oracle",
  "node-dockerfile-12_stretch-Dockerfile",
  "node-dockerfile-17_stretch-Dockerfile",
  "node-modus-16.14.0-stretch-amd64-1.22.17",
  "node-dockerfile-17_alpine3.15-Dockerfile",
  "redis-dockerfile-5_alpine-Dockerfile",
  "node-modus-12.22.10-stretch-amd64-1.22.17",
  "redis-modus-5.0.14-alpine",
  "node-dockerfile-17_buster-slim-Dockerfile",
  "node-modus-12.22.10-buster-amd64-1.22.17",
  "ubuntu-dockerfile-bionic-Dockerfile",
  "node-modus-17.7.0-bullseye-slim-amd64-1.22.17",
  "node-dockerfile-17_alpine3.14-Dockerfile",
  "node-modus-17.7.0-buster-slim-amd64-1.22.17",
  "node-dockerfile-17_bullseye-slim-Dockerfile",
  "traefik-dockerfile-v2.6.1-scratch",
  "node-modus-14.19.0-bullseye-slim-amd64-1.22.17",
  "ubuntu-dockerfile-jammy-Dockerfile",
  "node-dockerfile-16_bullseye-Dockerfile",
  "mysql-dockerfile-8.0-Dockerfile.debian",
  "node-dockerfile-14_buster-slim-Dockerfile",
  "node-modus-16.14.0-buster-slim-amd64-1.22.17",
  "redis-modus-5.0.14-32bit",
  "redis-dockerfile-5_32bit-Dockerfile",
  "node-dockerfile-16_bullseye-slim-Dockerfile",
  "node-modus-17.7.0-stretch-slim-amd64-1.22.17",
  "ubuntu-dockerfile-impish-Dockerfile",
  "node-modus-17.7.0-stretch-amd64-1.22.17",
  "node-dockerfile-17_stretch-slim-Dockerfile",
  "node-modus-16.14.0-buster-amd64-1.22.17",
  "node-modus-12.22.10-bullseye-amd64-1.22.17",
  "redis-dockerfile-6.0-Dockerfile",
  "node-dockerfile-16_alpine3.15-Dockerfile",
  "node-dockerfile-17_bullseye-Dockerfile",
  "node-dockerfile-12_alpine3.14-Dockerfile",
  "redis-dockerfile-6.0_alpine-Dockerfile",
  "node-modus-17.7.0-alpine3.15-amd64-1.22.17",
  "traefik-modus-2.6.1-alpine-amd64",
  "node-modus-17.7.0-alpine3.14-amd64-1.22.17",
  "traefik-dockerfile-v1.7.34-scratch",
  "node-dockerfile-14_stretch-slim-Dockerfile",
  "node-modus-12.22.10-buster-slim-amd64-1.22.17",
  "node-dockerfile-16_stretch-slim-Dockerfile",
  "node-modus-14.19.0-alpine3.15-amd64-1.22.17",
  "node-modus-16.14.0-bullseye-slim-amd64-1.22.17",
  "ubuntu-dockerfile-trusty-Dockerfile",
  "node-modus-14.19.0-bullseye-amd64-1.22.17",
  "node-modus-16.14.0-stretch-slim-amd64-1.22.17",
  "node-modus-12.22.10-alpine3.14-amd64-1.22.17",
  "node-dockerfile-12_bullseye-slim-Dockerfile",
  "ubuntu-modus-trusty",
  "redis-dockerfile-7.0-rc_alpine-Dockerfile",
  "node-dockerfile-17_buster-Dockerfile",
  "redis-modus-7.0-rc2-",
  "node-dockerfile-14_stretch-Dockerfile",
  "traefik-modus-1.7.34-scratch-amd64",
  "ubuntu-modus-bionic",
  "node-modus-14.19.0-stretch-slim-amd64-1.22.17",
  "node-modus-17.7.0-bullseye-amd64-1.22.17",
  "ubuntu-modus-focal",
  "node-modus-14.19.0-alpine3.14-amd64-1.22.17",
  "mysql-dockerfile-5.7-Dockerfile.oracle",
  "node-dockerfile-16_buster-slim-Dockerfile",
  "node-modus-14.19.0-buster-slim-amd64-1.22.17",
  "node-dockerfile-12_bullseye-Dockerfile",
  "traefik-modus-2.6.1-scratch-amd64",
  "mysql-modus-5.7-oracle-7-slim-amd64",
  "node-dockerfile-12_buster-Dockerfile",
  "redis-dockerfile-6.2_alpine-Dockerfile",
  "node-modus-16.14.0-alpine3.15-amd64-1.22.17",
  "node-modus-16.14.0-alpine3.14-amd64-1.22.17",
  "node-modus-12.22.10-alpine3.15-amd64-1.22.17",
  "node-dockerfile-16_stretch-Dockerfile",
  "redis-modus-6.0.16-",
  "node-modus-12.22.10-stretch-slim-amd64-1.22.17",
  "node-dockerfile-16_buster-Dockerfile",
  "node-modus-14.19.0-buster-amd64-1.22.17",
  "ubuntu-dockerfile-focal-Dockerfile",
  "mysql-dockerfile-5.7-Dockerfile.debian",
  "node-dockerfile-14_buster-Dockerfile",
  "node-dockerfile-12_stretch-slim-Dockerfile",
  "ubuntu-modus-impish",
  "redis-modus-6.2.6-alpine",
  "ubuntu-modus-xenial",
  "node-dockerfile-12_alpine3.15-Dockerfile",
  "mysql-modus-8.0-oracle-8-slim-amd64",
  "node-modus-17.7.0-buster-amd64-1.22.17",
  "ubuntu-dockerfile-xenial-Dockerfile",
  "redis-modus-6.0.16-alpine",
  "node-modus-12.22.10-bullseye-slim-amd64-1.22.17",
  "node-dockerfile-14_alpine3.15-Dockerfile",
  "node-dockerfile-14_bullseye-Dockerfile",
  "mysql-modus-5.7-debian-buster-amd64",
  "node-dockerfile-14_bullseye-slim-Dockerfile",
  "node-modus-16.14.0-bullseye-amd64-1.22.17",
  "redis-dockerfile-5-Dockerfile",
  "traefik-modus-1.7.34-alpine-amd64",
  "node-dockerfile-14_alpine3.14-Dockerfile",
]

run()
