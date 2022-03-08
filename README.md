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
| mysql | 2.52 (1.88 - 3.16) | 105.99 (101.53 - 110.45) | 1.35 (1.22 - 1.49) | 112.75 (105.67 - 119.82) | 20 |
| ubuntu | 0.03 (0.03 - 0.03) | 55.16 (48.41 - 61.90) | 21.08 (21.03 - 21.14) | 35.16 (30.96 - 39.37) | 21 |
| node | 4.78 (4.38 - 5.19) | 151.11 (150.28 - 151.95) | 1.22 (1.21 - 1.23) | 203.10 (202.59 - 203.62) | 21 |
| traefik | 0.00 | 9.76 (9.34 - 10.17) | 0.03 (0.03 - 0.03) | 26.15 (23.11 - 29.19) | 20 |
| redis | 1.39 (1.31 - 1.48) | 394.52 (393.01 - 396.03) | 1.20 (1.14 - 1.25) | 366.08 (364.84 - 367.32) | 21 |

