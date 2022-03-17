#!/usr/bin/env python3
from itertools import chain
import os
import regex as re
import subprocess
from os import isatty, path
from time import time, sleep
from glob import glob
import sys
import json

root = path.abspath(path.dirname(__file__))

skip_actual_build = os.environ.get("SKIP_ACTUAL_BUILD") == "true"
push_to = os.environ.get("IMAGE_PUSH_TO")


def chdir(dir):
    dir = path.normpath(path.join(root, dir))
    if isatty(sys.stderr.fileno()):
        sys.stderr.write(f"\x1b[2K\r   Entering {dir}\n")
    else:
        sys.stderr.write(f"Entering {dir}\n")
    sys.stderr.flush()
    os.chdir(dir)


chdir(".")


class ExperimentFailedException(Exception):
    def __init__(self):
        super().__init__("Experiment failed")


def system(cmd, cwd=None, capture=True):
    cmd_nonewline = re.sub("\n.*$", " ...", cmd,
                           flags=re.MULTILINE | re.DOTALL)
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
                    stdout.append(stdout_read.decode(
                        "utf-8", errors="replace"))
                stderr_read = proc.stderr.read()
                if stderr_read:
                    stderr.append(stderr_read.decode(
                        "utf-8", errors="replace"))
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
        raise ExperimentFailedException
    else:
        sys.stderr.write("\n")
        sys.stderr.flush()

    return dur


system("modus --version", capture=False)
system(
    "echo true | parallel || { echo Please install the GNU parallel package; exit 1; }")


def code_word_count(fname):
    # with open(fname, "rt") as f:
    #     fcontent = f.read()
    #     return (len(re.split("\W+", fcontent)), fcontent.count("\n"))
    try:
        res = subprocess.run([path.join(root, "fair-codesize.sh"), fname], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        e = e.stderr.decode("utf-8", errors="replace")
        if isatty(sys.stderr):
            sys.stderr.write(f"\x1b[31m{e}\n\x1b[1mError while running fair-codesize.sh\n\x1b[0m")
            sys.stderr.flush()
        else:
            sys.stderr.write(e)
        raise ExperimentFailedException
    res = res.stdout.decode("utf-8", errors="replace")
    res = [r for r in re.splititer("\s+", res) if r != ""]
    res = [int(r) for r in res]
    return (res[8], res[7], res[6])


# TODO: convert into submodules
upstream_git = {
    "ubuntu": ("https://github.com/tianon/docker-brew-ubuntu-core.git", "a11c63cee4049ffbe8acb8ba43c2c58fceb60057"),
    "redis": ("https://github.com/docker-library/redis.git", "4c11f9ce09d45c8b8617d17be181069b637b145f"),
    "node": ("https://github.com/nodejs/docker-node.git", "3b1657458c2deaac996554ccfa76256227dfaac8"),
    "mysql": ("https://github.com/docker-library/mysql.git", "37981f652a98b8fc26f487be9eda167de4689d84"),
    "traefik": ("https://github.com/traefik/traefik-library-image.git", "19b29d4858c12d74647d59214e0a9417646343ca"),
    "nginx": ("https://github.com/nginxinc/docker-nginx.git", "92973a30900b2ed881d208d10cadade34bbbab33"),
}
apps = list(sorted(upstream_git.keys()))
if len(sys.argv) > 1:
    only_run = sys.argv[1:]
    for app in only_run:
        if app not in apps:
            sys.stderr.write(f"{app} is not a valid app\n")
            sys.stderr.flush()
            exit(1)
    apps = only_run

codesize_ours_extra = {
    "mysql": ["upstream.git/versions.sh"]
}
codesize_theirs_extra_scripts = {
    "node": ["functions.sh"],
    "mysql": [
        "versions.sh",
        "apply-templates.sh",
    ],
    "traefik": [
        "updatev1.sh",
        # not counting updatev2: it is exactly the same as v1, wonder why they made another file...
    ]
}
codesize_theirs_extra_templates = {
    "mysql": [
        "template/Dockerfile.*"
    ],
    "traefik": [
        "alpine/tmpl*.Dockerfile",
        "scratch/tmpl*.Dockerfile"
    ]
}
app_query = {
    "ubuntu": "ubuntu(version)",
    "redis": "redis(version, variant)",
    "node": "node(version, variant, arch, yarn_version)",
    "mysql": "mysql(major_version, dist, variant, \"amd64\")",
    "traefik": "traefik(version, variant, \"amd64\")",
    "nginx": "nginx(branch, dist, include_perl)",
}


def cleanup_images():
    if skip_actual_build:
        return
    system("docker container prune -f")
    system("docker image prune -f")
    system("docker builder prune -f")


app_modus_target = {}
app_docker_targets = {}
app_modus_prepare_time = {}
app_docker_prepare_time = {}
app_modus_time = {}
app_docker_times = {}
app_profiling_info = {}
# The Dockerfile for these apps does not work under buildkit.
app_docker_nobuildkit = []

for app in apps:
    chdir(app)
    app_modus_prepare_time[app] = 0
    app_docker_prepare_time[app] = 0
    if app in upstream_git:
        repo_dir = path.join(root, app, "upstream.git")
        git_url, commit_sha = upstream_git[app]
        if not skip_actual_build:
            if not path.isdir(repo_dir):
                system(f"git clone --single-branch '{git_url}' '{repo_dir}'")
                chdir(repo_dir)
            else:
                chdir(repo_dir)
                system("git reset --hard && git clean -dffx")
            system(f"git checkout '{commit_sha}'")
            chdir(app)

    app_modus_target[app] = "generated.Modusfile"
    for our_prepare_script in ["generate-versions.sh", "generate-versions.py"]:
        if path.isfile(our_prepare_script):
            if our_prepare_script.endswith(".sh"):
                it = "bash"
            elif our_prepare_script.endswith(".py"):
                it = "python3"
            if not skip_actual_build:
                app_modus_prepare_time[app] += system(
                    f"{it} ./{our_prepare_script} > generated.Modusfile")
                system("cat build.Modusfile >> generated.Modusfile")
            break
    else:
        app_modus_target[app] = "Modusfile"

    if app in upstream_git:
        chdir(repo_dir)
        with open("arch", "wt") as arch:
            arch.write("amd64")
        if not skip_actual_build:
            if path.isfile("../update-upstream.sh"):
                app_docker_prepare_time[app] += system("../update-upstream.sh")
            else:
                app_docker_prepare_time[app] += system("./update.sh")
        if app == "mysql":
            dockerfiles = glob("*.*/Dockerfile.*", recursive=True)
        elif app == "traefik":
            dockerfiles = list(chain(
                glob("alpine-*.Dockerfile", recursive=True),
                glob("scratch-*.Dockerfile", recursive=True),
            ))
        else:
            dockerfiles = glob("**/*Dockerfile", recursive=True)
        targets = []
        for d in dockerfiles:
            if app == "nginx" and "modules" in d:
                # Modules are a separate repository - we don't build them here.
                continue
            dir = path.relpath(path.abspath(
                path.dirname(d)), path.join(root, app))
            targets.append((dir, path.basename(d)))
        app_docker_targets[app] = targets
        chdir(app)

    print(f"{app}:")
    print(f"  Modusfile: {app_modus_target[app]}")
    if app in app_docker_targets:
        print(f"  Dockerfiles:")
        for dir, dfile in app_docker_targets[app]:
            print(f"    {dir}/{dfile}")
        app_docker_times[app] = 0

def print_performance(app):
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

def sanitize_tag_name(tag):
    return re.sub("[^a-zA-Z0-9_.-]", "_", tag)

for app, target in app_modus_target.items():
    try:
        chdir(app)
        cleanup_images()
        json_out = path.join(root, "modus-build.json")
        profiling_out = path.join(root, "profiling.json")
        if path.isfile(json_out):
            os.remove(json_out)
        if path.isfile(profiling_out):
            os.remove(profiling_out)

        if not skip_actual_build:
            for (context, fname) in app_docker_targets[app]:
                p = path.join(context, fname)
                with open(p, "rt") as f:
                    s = f.read()
                    matches = re.search(r"(^|\n)FROM (\S+)",
                                        s, flags=re.IGNORECASE)
                    if matches:
                        for image in matches.captures(2):
                            if image == "scratch" or image.startswith("traefik"):
                                continue
                            if subprocess.run(["docker", "image", "inspect", image], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
                                system(f"docker pull {image}")

        if not skip_actual_build:
            app_modus_time[app] = system(
                f"modus build . -f '{target}' '{app_query[app]}' --no-cache --json={json_out} --output-profiling={profiling_out}", capture=False)
            with open(json_out, "rt") as f:
                modus_outputs = json.load(f)
            with open(profiling_out, "rt") as f:
                profiling_info = json.load(f)
            os.remove(json_out)
        else:
            app_modus_time[app] = system(
                f"modus proof . -f '{target}' '{app_query[app]}'")
            modus_outputs = []
            profiling_info = {}
        app_profiling_info[app] = profiling_info
        if len(modus_outputs) != len(app_docker_targets[app]):
            if isatty(sys.stderr.fileno()):
                sys.stderr.write("\x1b[31;1m")
            sys.stderr.write(
                f"Warning: modus reported {len(modus_outputs)} output images, but {app} has {len(app_docker_targets[app])} Dockerfiles\n")
            sys.stderr.flush()
        if push_to is not None and not skip_actual_build:
            for output in modus_outputs:
                push_tag = push_to + f":{app}-modus-{sanitize_tag_name('-'.join(output['args']))}"
                system(f"docker tag {output['digest']} {push_tag}")
                system(f"docker push {push_tag}")
        cleanup_images()
        push_tags = []
        if path.isfile("custom-build-upstream.sh"):
            parallel_cmd = "cd upstream.git && bash ../custom-build-upstream.sh"
        else:
            parallel_cmd = "parallel <<EOF\n"
            for i, (context, fname) in enumerate(app_docker_targets[app]):
                ctxdir = path.join(root, app, context)
                build_cmd = f"docker build '{ctxdir}' -f {path.join(ctxdir, fname)} --no-cache"
                if push_to is not None:
                    push_tag = push_to + f":{app}-dockerfile-{sanitize_tag_name(path.relpath(ctxdir, path.join(root, app, 'upstream.git')))}-{sanitize_tag_name(fname)}"
                    build_cmd = build_cmd + " -t " + push_tag
                    push_tags.append(push_tag)
                use_buildkit = app not in app_docker_nobuildkit
                if use_buildkit:
                    build_cmd = f"DOCKER_BUILDKIT=1 {build_cmd}"
                else:
                    build_cmd = f"DOCKER_BUILDKIT=0 {build_cmd}"
                parallel_cmd += build_cmd + "\n"
            parallel_cmd += "EOF"
        if skip_actual_build:
            parallel_cmd = "true # skipped by flag"
        app_docker_times[app] = system(parallel_cmd)
        for pt in push_tags:
            system(f"docker push {pt}")

        print_performance(app)
    except ExperimentFailedException:
        rest_index = apps.index(app)
        remaining = apps[rest_index:]
        sys.stderr.write("To retry this failed experiment and continue with the remaining, run:\n")
        sys.stderr.write(f"  ./run-all.py {' '.join(remaining)}\n")
        sys.stderr.flush()
        exit(1)

tex_sources = ["", ""]

def print_codesize(app):
    print(f"Code size report for {app}:")
    print("\x1b[1mOurs:\x1b[0m")
    ours_total_chars = 0
    ours_total_words = 0
    ours_total_lines = 0
    mf_to_count = "build.Modusfile"
    if app_modus_target[app] != "generated.Modusfile":
        mf_to_count = "Modusfile"
    m_chars, m_words, m_lines = code_word_count(mf_to_count)
    ours_total_chars += m_chars
    ours_total_words += m_words
    ours_total_lines += m_lines
    our_extra = []
    if app in codesize_ours_extra:
        our_extra = codesize_ours_extra[app]
    for our_prepare_script in chain(["generate-versions.sh", "generate-versions.py"], our_extra):
        if path.isfile(our_prepare_script):
            u_chars, u_words, u_lines = code_word_count(our_prepare_script)
            ours_total_chars += u_chars
            ours_total_words += u_words
            ours_total_lines += u_lines
            print(f"  {our_prepare_script}: {u_chars} chars, {u_words} words, {u_lines} lines")
    print(f"  build.Modusfile: {m_chars} chars, {m_words} words, {m_lines} lines")
    print(f"  Ours total: {ours_total_chars} chars, {ours_total_words} words, {ours_total_lines} lines")
    print(f"\x1b[1mTheirs:\x1b[0m")
    theirs_chars = 0
    theirs_words = 0
    theirs_lines = 0
    theirs_chars_templates = 0
    theirs_words_templates = 0
    theirs_lines_templates = 0
    if app in codesize_theirs_extra_scripts:
        extra_scripts = [pp
                 for p in codesize_theirs_extra_scripts[app]
                 for pp in glob(path.join("upstream.git", p), recursive=True)]
    else:
        extra_scripts = []
    if app in codesize_theirs_extra_templates:
        extra_templates = [pp
                 for p in codesize_theirs_extra_templates[app]
                 for pp in glob(path.join("upstream.git", p), recursive=True)]
    else:
        extra_templates = []
    for t in chain(glob("upstream.git/**/*.template", recursive=True), ["upstream.git/update.sh"], extra_scripts, extra_templates):
        if path.isfile(t):
            chars, words, lines = code_word_count(t)
            theirs_chars += chars
            theirs_words += words
            theirs_lines += lines
            print(f"  {t}: {chars} chars, {words} words, {lines} lines")
    print(f"  Theirs total: {theirs_chars} chars, {theirs_words} words, {theirs_lines} lines")
    for t in chain(glob("upstream.git/**/*.template", recursive=True), extra_templates):
        if path.isfile(t):
            chars, words, lines = code_word_count(t)
            theirs_chars_templates += chars
            theirs_words_templates += words
            theirs_lines_templates += lines
    print(f"  Theirs templates total: {theirs_chars_templates} chars, {theirs_words_templates} words, {theirs_lines_templates} lines")

    def chg(ours, theirs):
        if theirs == 0:
            return "n/a"
        p = (ours - theirs) / theirs
        p *= 100
        if p < 0:
            return f"{p:.1f}\\%"
        else:
            return f"+{p:.1f}\\%"

    tex_sources[0] += f"  \\textbf{{{app}}} & {theirs_lines} & {theirs_words} & {theirs_chars} & {ours_total_lines} ({chg(ours_total_lines, theirs_lines)}) & {ours_total_words} ({chg(ours_total_words, theirs_words)}) & {ours_total_chars} ({chg(ours_total_chars, theirs_chars)}) \\\\\n"
    tex_sources[1] += f"  \\textbf{{{app}}} & {theirs_lines_templates} & {theirs_words_templates} & {theirs_chars_templates} & {m_lines} ({chg(m_lines, theirs_lines_templates)}) & {m_words} ({chg(m_words, theirs_words_templates)}) & {m_chars} ({chg(m_chars, theirs_chars_templates)}) \\\\\n"


for app in apps:
    chdir(app)
    print_performance(app)
    print("")
    print_codesize(app)
    print("")
    print("====================")
    print("")

print(tex_sources[0])
print("")
print(tex_sources[1])

print(">>>>")
print(json.dumps({
    "app_modus_time": app_modus_time,
    "app_modus_prepare_time": app_modus_prepare_time,
    "app_docker_times": app_docker_times,
    "app_docker_prepare_time": app_docker_prepare_time,
    "app_profiling_info": app_profiling_info,
}, indent=None))
