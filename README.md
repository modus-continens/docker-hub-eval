## Requirements

The following commands need to be available:

* bash and other basic unix utilities, curl, wget
* python
* git
* parallel
* dpkg (can be installed in non-debian distros)
* jq, sed, awk, gawk
* modus = 0.1.8 (`cargo install modus --version 0.1.8` or download from https://github.com/modus-continens/modus/releases/download/0.1.8/modus-0.1.8.x86_64-linux-musl)

## Results

Time measurements **does not include** the time it takes to pull base images, as these are cached locally.

The following results are obtained running on a Google Cloud Compute VM with the following configuration:

* us-central1-a
* Intel Cascade Lake (Compute Optimized)
* c2-standard-4: 4 vCPUs, 16 GB RAM
* SSD disk

Numbers in parentheses are the 95% confidence interval of the population mean.

| app | Update version list (Modus) | Modus build | upstream ./update.sh | upstream Docker build | n |
| --- | --- | --- | --- | --- | --- |
| ubuntu | 0.03 (0.03 - 0.03) | 52.82 (44.24 - 61.41) | 21.07 (21.00 - 21.14) | 33.71 (28.35 - 39.07) | 16 |
| node | 4.63 (4.54 - 4.72) | 151.40 (150.52 - 152.29) | 1.22 (1.21 - 1.24) | 203.07 (202.50 - 203.64) | 15 |
| redis | 1.44 (1.33 - 1.54) | 394.13 (392.41 - 395.84) | 1.21 (1.15 - 1.28) | 365.82 (364.25 - 367.38) | 16 |
| traefik | 0.00 | 9.71 (9.26 - 10.16) | 0.03 (0.03 - 0.03) | 25.21 (21.26 - 29.16) | 15 |
| mysql | 2.24 (1.94 - 2.54) | 103.45 (98.29 - 108.61) | 1.34 (1.17 - 1.52) | 110.63 (101.41 - 119.86) | 15 |
