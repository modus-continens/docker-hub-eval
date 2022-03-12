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

| app | Update version list (Modus) | Modus build total time | Modus Exporting time | upstream ./update.sh | upstream Docker build | n |
| --- | --- | --- | --- | --- | --- | --- |
| mysql | 1.52 (1.14 - 1.91) | 71.24 (71.01 - 71.48) | 3.45 (3.42 - 3.47) | 2.97 (2.91 - 3.03) | 65.52 (65.40 - 65.64) | 64 |
| node | 4.66 (4.58 - 4.73) | 96.78 (96.50 - 97.05) | 12.64 (12.55 - 12.72) | 1.04 (1.03 - 1.05) | 110.87 (110.50 - 111.24) | 64 |
| redis | 1.31 (1.22 - 1.40) | 198.39 (198.13 - 198.64) | 5.10 (4.91 - 5.29) | 1.02 (0.97 - 1.06) | 199.84 (199.73 - 199.96) | 64 |
| traefik | 0.00 | 10.71 (10.38 - 11.04) | 2.15 (2.13 - 2.18) | 0.03 (0.03 - 0.03) | 9.00 (8.54 - 9.47) | 64 |
| ubuntu | 0.03 (0.03 - 0.03) | 16.13 (16.02 - 16.24) | 3.56 (3.50 - 3.63) | 3.33 (3.30 - 3.37) | 8.00 (7.95 - 8.05) | 64 |
