#!/usr/bin/env python3
import os
from statistics import mean
import subprocess
from os import isatty, path
from time import time, sleep
from glob import glob
import sys

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
    if isatty(sys.stderr.fileno()):
        sys.stderr.write("\x1b[2K\r\x1b[34m=> ")
        sys.stderr.write(cmd)
        sys.stderr.write("\x1b[0m")
    else:
        sys.stderr.write(cmd)
    sys.stderr.flush()
    start_time = time()
    if capture:
        with subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            while True:
                ret = proc.poll()
                dur = time() - start_time
                if isatty(sys.stderr.fileno()):
                    sys.stderr.write("\x1b[2K\r\x1b[34m=> ")
                    sys.stderr.write(cmd)
                    sys.stderr.write(f" [{round(dur, 1)}s] \x1b[0m")
                    sys.stderr.flush()
                if ret is not None:
                    stdout = proc.stdout.read().decode("utf-8")
                    stderr = proc.stderr.read().decode("utf-8")
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


apps = ["ubuntu"]
upstream_git = {
    "ubuntu": ("https://github.com/tianon/docker-brew-ubuntu-core.git", "a11c63cee4049ffbe8acb8ba43c2c58fceb60057"),
}
app_query = {
    "ubuntu": "ubuntu(version)",
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
        app_modus_prepare_time[app] += system("bash ./generate-versions.sh")

    if path.isfile("versions.Modusfile"):
        with open("generated.Modusfile", "wt") as mf:
            with open("build.Modusfile") as bf:
                mf.write(bf.read())
            mf.write("\n")
            with open("versions.Modusfile", "r") as vf:
                mf.write(vf.read())
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
        app_docker_times[app] = [0] * len(app_docker_targets[app])

for app, target in app_target.items():
    chdir(app)
    cleanup_images()
    app_modus_time[app] = system(
        f"modus build . -f '{target}' '{app_query[app]}' --no-cache", capture=False)
    cleanup_images()
    for i, (context, fname) in enumerate(app_docker_targets[app]):
        chdir(path.join(app, context))
        build_cmd = f"docker build . -f {fname} -t {app}-docker-{i+1} --no-cache"
        use_buildkit = app not in app_docker_nobuildkit
        if use_buildkit:
            build_cmd = f"DOCKER_BUILDKIT=1 {build_cmd}"
        else:
            build_cmd = f"DOCKER_BUILDKIT=0 {build_cmd}"
        app_docker_times[app][i] = system(
            build_cmd, capture=not use_buildkit)

for i, app in enumerate(apps):
    print(f"Performance report for {app}:")
    modus_time = app_modus_time[app]
    modus_prepare_time = app_modus_prepare_time[app]
    print(
        f"  Modus build time: {round(modus_prepare_time, 1)}s version parsing + {round(modus_time, 1)}s modus build = {round(modus_prepare_time + modus_time, 1)}s")
    docker_times = app_docker_times[app]
    docker_times_str = " + ".join(f"{round(t, 1)}s" for t in docker_times)
    docker_prepare_time = app_docker_prepare_time[app]
    print(
        f"  Docker build times: {round(docker_prepare_time, 1)}s in update.sh +")
    print(f"    {docker_times_str} (avg {round(mean(docker_times), 1)}s, max {round(max(docker_times), 1)}s) in docker build (for each Dockerfile)")
    print(f"    = {round(docker_prepare_time + sum(docker_times), 1)}s ({round(docker_prepare_time + max(docker_times), 1)}s if assuming docker build perfectly parallelizable)")
