## Requirements

The following commands need to be available:

* bash and other basic unix utilities, curl, wget
* python3
* git
* parallel
* dpkg (can be installed in non-debian distros)
* jq, sed, awk, gawk
* modus = 0.1.10 (`cargo install modus --version 0.1.10` or download from https://github.com/modus-continens/modus/releases/download/0.1.10/modus-0.1.10.x86_64-linux-musl)

The following python packages are needed for running the experiment:

* regex

And the following are needed for parsing the result:

* scipy (for confidence interval / sttatistical testing)

## Results

Time measurements **does not include** the time it takes to pull base images. These are always cached locally.

The following results are obtained running on a AWS EC2 VM with the following configuration:

* c5.2xlarge: 8 vCPUs, 16 GB RAM
* 8000 IOPS SSD disk

| app | Update version list (Modus) | Modus build | upstream ./update.sh | upstream Docker build | n |
| --- | --- | --- | --- | --- | --- |
| mysql | 1.54 (1.29 - 1.80) | 70.85 (70.25 - 71.44) | 2.87 (2.85 - 2.89) | 65.15 (64.99 - 65.32) | 31 |
| node | 4.57 (4.48 - 4.67) | 92.77 (92.26 - 93.28) | 1.02 (1.01 - 1.02) | 105.93 (105.62 - 106.25) | 30[^1] |
| redis | 1.23 (1.15 - 1.32) | 196.78 (196.58 - 196.98) | 1.05 (0.92 - 1.17) | 198.78 (198.61 - 198.96) | 32 |
| traefik | 0.00 | 11.17 (10.16 - 12.19) | 0.03 (0.03 - 0.03) | 8.76 (8.32 - 9.20) | 31 |
| ubuntu | 0.03 (0.03 - 0.03) | 15.35 (15.14 - 15.55) | 3.60 (3.12 - 4.08) | 7.57 (7.50 - 7.64) | 32 |

[^1]: Removed run #8, which spent 6093.47s in the upstream Docker build stage.
