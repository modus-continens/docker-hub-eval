#!/usr/bin/env python3
import os
import re
from statistics import mean
import subprocess
from os import isatty, path
from time import time, sleep
from glob import glob
import sys
import json

root = path.abspath(path.dirname(__file__))


def chdir(dir):
    dir = path.normpath(path.join(root, dir))
    if isatty(sys.stderr.fileno()):
        sys.stderr.write(f"\x1b[2K\r   Entering {dir}\n")
    else:
        sys.stderr.write(f"Entering {dir}\n")
    sys.stderr.flush()
    os.chdir(dir)


chdir(".")


def system(cmd, cwd=None, capture=True):
    cmd_nonewline = re.sub("\n.*$", " ...", cmd, flags=re.MULTILINE | re.DOTALL)
    if isatty(sys.stderr.fileno()):
        sys.stderr.write("\x1b[2K\r\x1b[34m=> ")
        sys.stderr.write(cmd_nonewline)
        sys.stderr.write("\x1b[0m")
    else:
        sys.stderr.write(cmd)
    sys.stderr.flush()
    start_time = time()
    if capture:
        with subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            stdout = []
            stderr = []
            os.set_blocking(proc.stdout.fileno(), False)
            os.set_blocking(proc.stderr.fileno(), False)
            while True:
                ret = proc.poll()
                dur = time() - start_time
                stdout_read = proc.stdout.read()
                if stdout_read:
                    stdout.append(stdout_read.decode())
                stderr_read = proc.stderr.read()
                if stderr_read:
                    stderr.append(stderr_read.decode())
                if isatty(sys.stderr.fileno()):
                    sys.stderr.write("\x1b[2K\r\x1b[34m=> ")
                    sys.stderr.write(cmd_nonewline)
                    sys.stderr.write(f" [{round(dur, 1)}s] \x1b[0m")
                    sys.stderr.flush()
                if ret is not None:
                    stdout = "".join(stdout)
                    stderr = "".join(stderr)
                    break
                else:
                    sleep(0.03)
    else:
        sys.stderr.write("\n")
        sys.stderr.flush()
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=False)
        dur = time() - start_time
        ret = r.returncode
        stdout = ""
        stderr = ""
    if ret != 0:
        if isatty(sys.stderr.fileno()):
            sys.stderr.write("\x1b[2K\r")
        sys.stderr.write(stdout)
        if isatty(sys.stderr.fileno()):
            sys.stderr.write("\x1b[31m")
        sys.stderr.write(stderr)
        if isatty(sys.stderr.fileno()):
            sys.stderr.write("\x1b[2K\r\x1b[31m   ")
            sys.stderr.write(cmd)
            sys.stderr.write("\n\x1b[0m")
        sys.stderr.write(f"      The above command returned {ret}\n")
        sys.stderr.flush()
        exit(1)
    else:
        sys.stderr.write("\n")
        sys.stderr.flush()

    return dur


apps = ["ubuntu", "redis"]
if len(sys.argv) > 1:
    only_run = sys.argv[1:]
    for app in only_run:
        if app not in apps:
            sys.stderr.write(f"{app} is not a valid app\n")
            sys.stderr.flush()
            exit(1)
    apps = only_run

upstream_git = {
    "ubuntu": ("https://github.com/tianon/docker-brew-ubuntu-core.git", "a11c63cee4049ffbe8acb8ba43c2c58fceb60057"),
    "redis": ("https://github.com/docker-library/redis.git", "4c11f9ce09d45c8b8617d17be181069b637b145f"),
}
app_query = {
    "ubuntu": "ubuntu(version)",
    "redis": "redis(version, variant)"
}


def cleanup_images():
    system("docker container prune -f")
    system("docker image rm -f $(docker image ls -aq) || true")
    system("docker image prune -f")
    system("docker image prune -f")
    # system("docker buildx prune -f")
    # takes too long


app_target = {}
app_docker_targets = {}
app_modus_prepare_time = {}
app_docker_prepare_time = {}
app_modus_time = {}
app_docker_times = {}
# The Dockerfile for these apps does not work under buildkit.
app_docker_nobuildkit = []

for app in apps:
    chdir(app)
    app_modus_prepare_time[app] = 0
    app_docker_prepare_time[app] = 0
    if app in upstream_git:
        repo_dir = path.join(root, app, "upstream.git")
        git_url, commit_sha = upstream_git[app]
        if not path.isdir(repo_dir):
            system(f"git clone --single-branch '{git_url}' '{repo_dir}'")
            chdir(repo_dir)
        else:
            chdir(repo_dir)
            system("git reset --hard && git clean -dffx")
        system(f"git checkout '{commit_sha}'")
        chdir(app)

    if path.isfile("generate-versions.sh"):
        app_modus_prepare_time[app] += system("bash ./generate-versions.sh > generated.Modusfile")
        system("cat build.Modusfile >> generated.Modusfile")
        app_target[app] = "generated.Modusfile"
    else:
        app_target[app] = "Modusfile"

    if app in upstream_git:
        chdir(repo_dir)
        with open("arch", "wt") as arch:
            arch.write("amd64")
        app_docker_prepare_time[app] += system("./update.sh")
        dockerfiles = glob("**/*Dockerfile", recursive=True)
        targets = []
        for d in dockerfiles:
            dir = path.relpath(path.abspath(
                path.dirname(d)), path.join(root, app))
            targets.append((dir, path.basename(d)))
        app_docker_targets[app] = targets
        chdir(app)

    print(f"{app}:")
    print(f"  Modusfile: {app_target[app]}")
    if app in app_docker_targets:
        print(f"  Dockerfiles:")
        for dir, dfile in app_docker_targets[app]:
            print(f"    {dir}/{dfile}")
        app_docker_times[app] = 0

for app, target in app_target.items():
    chdir(app)
    cleanup_images()
    json_out = path.join(root, "modus-build.json")
    if path.isfile(json_out):
        os.remove(json_out)
    app_modus_time[app] = system(
        f"modus build . -f '{target}' '{app_query[app]}' --no-cache --json={json_out}", capture=False)
    with open(json_out, "rt") as f:
        modus_outputs = json.load(f)
    os.remove(json_out)
    if len(modus_outputs) != len(app_docker_targets[app]):
        if isatty(sys.stderr.fileno()):
            sys.stderr.write("\x1b[31;1m")
        sys.stderr.write(f"Warning: modus reported {len(modus_outputs)} output images, but {app} has {len(app_docker_targets[app])} Dockerfiles\n")
        sys.stderr.flush()
    cleanup_images()
    parallel_cmd = "parallel <<EOF\n"
    for i, (context, fname) in enumerate(app_docker_targets[app]):
        ctxdir = path.join(root, app, context)
        build_cmd = f"docker build '{ctxdir}' -f {path.join(ctxdir, fname)} -t {app}-docker-{i+1} --no-cache"
        use_buildkit = app not in app_docker_nobuildkit
        if use_buildkit:
            build_cmd = f"DOCKER_BUILDKIT=1 {build_cmd}"
        else:
            build_cmd = f"DOCKER_BUILDKIT=0 {build_cmd}"
        parallel_cmd += build_cmd + "\n"
    parallel_cmd += "EOF"
    app_docker_times[app] = system(parallel_cmd)

for i, app in enumerate(apps):
    print(f"Performance report for {app}:")
    modus_time = app_modus_time[app]
    modus_prepare_time = app_modus_prepare_time[app]
    print(
        f"  Modus build time: {round(modus_prepare_time, 1)}s version parsing + {round(modus_time, 1)}s modus build = {round(modus_prepare_time + modus_time, 1)}s")
    docker_time = app_docker_times[app]
    docker_prepare_time = app_docker_prepare_time[app]
    print(
        f"  Docker build times: {round(docker_prepare_time, 1)}s in update.sh")
    print(f"    + {round(docker_time, 1)}s in docker build (parallel)")
    print(f"    = {round(docker_prepare_time + docker_time, 1)}s")
