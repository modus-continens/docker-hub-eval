## Requirements

The following commands need to be available:

* bash and other basic unix utilities, curl, wget
* python
* git
* parallel
* dpkg (can be installed in non-debian distros)
* jq, sed, awk
* modus = 0.1.7 (`cargo install modus --version 0.1.7` or download from https://github.com/modus-continens/modus/releases/download/0.1.7/modus-0.1.7.x86_64-linux-musl)

## Results

```
Performance report for ubuntu:
  Modus build time: 0.0s version parsing + 25.3s modus build = 25.3s
  Docker build times: 5.3s in update.sh
    + 16.0s in docker build (parallel)
    = 21.4s

Code size report for ubuntu:
Ours:
  generate-versions.sh: 27 words, 10 lines
  build.Modusfile: 525 words, 82 lines
  Ours total: 552 words, 92 lines
Theirs:
  upstream.git/update.sh: 561 words, 118 lines
  Theirs total: 561 words, 118 lines
   Entering /home/tingmao/docker-hub-eval/redis
```

```
Performance report for redis:
  Modus build time: 1.5s version parsing + 349.1s modus build = 350.6s
  Docker build times: 1.4s in update.sh
    + 332.8s in docker build (parallel)
    = 334.3s

Code size report for redis:
Ours:
  generate-versions.sh: 185 words, 54 lines
  build.Modusfile: 1151 words, 199 lines
  Ours total: 1336 words, 253 lines
Theirs:
  upstream.git/old-protected-mode-sed.template: 63 words, 4 lines
  upstream.git/Dockerfile.template: 709 words, 122 lines
  upstream.git/Dockerfile-alpine.template: 609 words, 104 lines
  upstream.git/update.sh: 362 words, 97 lines
  Theirs total: 1743 words, 327 lines
   Entering /home/tingmao/docker-hub-eval/node
```

```
Performance report for node:
  Modus build time: 4.8s version parsing + 184.1s modus build = 188.9s
  Docker build times: 1.4s in update.sh
    + 214.2s in docker build (parallel)
    = 215.6s

Code size report for node:
Ours:
  generate-versions.sh: 1354 words, 532 lines
  build.Modusfile: 872 words, 186 lines
  Ours total: 2226 words, 718 lines
Theirs:
  upstream.git/Dockerfile-slim.template: 473 words, 84 lines
  upstream.git/Dockerfile-debian.template: 332 words, 60 lines
  upstream.git/Dockerfile-alpine.template: 440 words, 88 lines
  upstream.git/update.sh: 835 words, 248 lines
  upstream.git/functions.sh: 843 words, 361 lines
  Theirs total: 2923 words, 841 lines
   Entering /home/tingmao/docker-hub-eval/mysql
```

```
Performance report for mysql:
  Modus build time: 1.8s version parsing + 161.1s modus build = 162.8s
  Docker build times: 4.1s in update.sh
    + 86.2s in docker build (parallel)
    = 90.3s

Code size report for mysql:
Ours:
  generate-versions.py: 97 words, 22 lines
  upstream.git/versions.sh: 412 words, 141 lines
  build.Modusfile: 1261 words, 211 lines
  Ours total: 1770 words, 374 lines
Theirs:
  upstream.git/update.sh: 19 words, 7 lines
  upstream.git/versions.sh: 412 words, 141 lines
  upstream.git/apply-templates.sh: 142 words, 48 lines
  Theirs total: 573 words, 196 lines
   Entering /home/tingmao/docker-hub-eval/traefik
```

```
Performance report for traefik:
  Modus build time: 0s version parsing + 11.1s modus build = 11.1s
  Docker build times: 0.1s in update.sh
    + 6.8s in docker build (parallel)
    = 6.8s

Code size report for traefik:
Ours:
  build.Modusfile: 287 words, 56 lines
  Ours total: 287 words, 56 lines
Theirs:
  upstream.git/update.sh: 135 words, 37 lines
  upstream.git/updatev1.sh: 44 words, 15 lines
  upstream.git/alpine/tmplv1.Dockerfile: 113 words, 24 lines
  upstream.git/alpine/tmplv2.Dockerfile: 135 words, 26 lines
  upstream.git/scratch/tmplv1.Dockerfile: 83 words, 16 lines
  upstream.git/scratch/tmplv2.Dockerfile: 83 words, 16 lines
  Theirs total: 593 words, 134 lines
```
