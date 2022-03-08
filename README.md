## Requirements

The following commands need to be available:

* bash and other basic unix utilities, curl, wget
* python
* git
* parallel
* dpkg (can be installed in non-debian distros)
* jq, sed, awk, gawk
* modus = 0.1.9 (`cargo install modus --version 0.1.9` or download from https://github.com/modus-continens/modus/releases/download/0.1.9/modus-0.1.9.x86_64-linux-musl)

**Following data outdated**


<del>

## Results (EC2)

Time measurements **does not include** the time it takes to pull base images, as these are cached locally.

The following results are obtained running on a AWS EC2 VM with the following configuration:

* 4 vCPUs, 16 GB RAM

| app | Update version list (Modus) | Modus build | upstream ./update.sh | upstream Docker build | n |
| --- | --- | --- | --- | --- | --- |
| redis | 1.46 (1.27 - 1.65) | 959.56 (862.75 - 1056.37) | 1.15 (1.04 - 1.26) | 946.07 (859.80 - 1032.34) | 15 |
| traefik | 0.00 | 22.06 (17.02 - 27.09) | 0.06 (0.06 - 0.07) | 14.04 (9.80 - 18.27) | 15 |
| ubuntu | 0.03 (0.03 - 0.03) | 55.28 (39.42 - 71.14) | 6.05 (5.78 - 6.31) | 32.25 (24.29 - 40.20) | 16 |
| mysql | 2.10 (1.87 - 2.33) | 187.96 (165.24 - 210.68) | 4.93 (4.63 - 5.22) | 173.38 (151.13 - 195.63) | 15 |
| node | 5.61 (5.31 - 5.91) | 433.44 (374.59 - 492.29) | 4.00 (3.05 - 4.96) | 463.42 (414.29 - 512.55) | 15 |

## Results (GCP)

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

</del>
