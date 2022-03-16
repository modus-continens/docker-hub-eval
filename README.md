## Requirements

The following commands need to be available:

* bash and other basic unix utilities, curl, wget
* python3
* git
* parallel
* dpkg (can be installed in non-debian distros)
* jq, sed, awk, gawk
* modus = 0.1.11 (`cargo install modus --version 0.1.11` or download from https://github.com/modus-continens/modus/releases/download/0.1.11/modus-0.1.11.x86_64-linux-musl)

The following python packages are needed for running the experiment:

* regex

And the following are needed for parsing the result:

* scipy (for confidence interval / sttatistical testing)

## Running the experiment

To run every build one time:

```
./run-all.py
```

To run every build an indefinite number of times (round robin):

```
./run-all-and-log.sh
```

At any point during this you may print the result up to the current point with `parse_runlog.py`.

## Results

Time measurements **does not include** the time it takes to pull base images. These are always cached locally.

The following results are obtained running on a AWS EC2 VM with the following configuration. Numbers in parentheses are the 95% confidence interval of the population mean.

* c5.2xlarge: 8 vCPUs, 16 GB RAM
* 8000 IOPS SSD disk

| app | Update version list (Modus) | Modus build total time | Modus Exporting time | upstream ./update.sh | upstream Docker build | n |
| --- | --- | --- | --- | --- | --- | --- |
| mysql | 1.33 (1.27 - 1.40) | 71.52 (71.31 - 71.72) | 3.39 (3.35 - 3.42) | 2.94 (2.90 - 2.98) | 66.68 (65.83 - 67.53) | 64 |
| node | 4.80 (4.72 - 4.89) | 96.23 (93.80 - 98.66) | 12.72 (11.83 - 13.60) | 1.04 (1.03 - 1.04) | 108.71 (108.15 - 109.28) | 64 |
| redis | 1.22 (1.16 - 1.28) | 197.99 (197.83 - 198.15) | 4.87 (4.81 - 4.92) | 1.04 (0.97 - 1.11) | 199.86 (199.71 - 200.01) | 64 |
| traefik | 0.00 | 10.83 (10.34 - 11.31) | 2.10 (2.07 - 2.13) | 0.03 (0.03 - 0.03) | 8.88 (8.56 - 9.20) | 64 |
| ubuntu | 0.03 (0.03 - 0.03) | 15.66 (15.53 - 15.79) | 3.46 (3.40 - 3.52) | 3.34 (3.28 - 3.41) | 7.81 (7.75 - 7.87) | 64 |
