## Requirements

The following commands need to be available:

* bash and other basic unix utilities, curl, wget
* python3
* git
* parallel
* dpkg (can be installed in non-debian distros)
* jq, sed, awk, gawk
* envsubst (included with the "gettext" package on most distros)
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

## Note on NodeJS

Occasionally the upstream update script for NodeJS can stop working, causing the experiment to fail. This is because their build server advertises a new version before actually finish building it and having the artifacts available. This is not something under our control, but if this happens the NodeJS run can always be skipped by lefting it out of the retry command line printed by `run-all.py`.

## Results

Time measurements **does not include** the time it takes to pull base images. These are always cached locally.

The following results are obtained running on a AWS EC2 VM with the following configuration. Numbers in parentheses are the 95% confidence interval of the population mean.

* c5.2xlarge: 8 vCPUs, 16 GB RAM
* 8000 IOPS SSD disk

| app | Update version list (Modus) | Modus build total time | Modus Resolving time | Modus Exporting time | upstream ./update.sh | upstream Docker build | n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mysql | 1.34 (1.26 - 1.42) | 71.60 (71.43 - 71.77) | 1.33 (1.31 - 1.36) | 3.38 (3.35 - 3.40) | 2.95 (2.90 - 2.99) | 66.21 (66.00 - 66.42) | 64 |
| nginx | 0.00 | 29.92 (29.84 - 30.00) | 1.34 (1.32 - 1.36) | 3.44 (3.39 - 3.49) | 0.07 (0.06 - 0.07) | 23.08 (23.03 - 23.12) | 64 |
| node | 4.87 (4.75 - 4.99) | 96.27 (93.85 - 98.70) | 3.63 (2.89 - 4.36) | 12.74 (11.85 - 13.62) | 1.04 (1.03 - 1.05) | 108.65 (108.09 - 109.21) | 64 |
| redis | 1.15 (1.08 - 1.22) | 206.22 (203.08 - 209.36) | 1.03 (1.01 - 1.04) | 3.69 (3.65 - 3.72) | 0.97 (0.90 - 1.03) | 199.82 (199.72 - 199.92) | 64 |
| traefik | 0.00 | 11.34 (10.65 - 12.04) | 0.90 (0.89 - 0.91) | 2.12 (2.09 - 2.15) | 0.03 (0.03 - 0.03) | 9.20 (8.82 - 9.58) | 64 |
| ubuntu | 0.03 (0.03 - 0.03) | 15.79 (15.65 - 15.93) | 1.60 (1.58 - 1.61) | 3.49 (3.42 - 3.55) | 3.33 (3.30 - 3.35) | 7.87 (7.81 - 7.93) | 64 |
