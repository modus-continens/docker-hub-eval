#!/usr/bin/env python3

# for i in (seq 1 100); for j in ubuntu redis node mysql traefik; ./run-all.py $j > ~/runlog/$i-$j.log; sleep 1; end; end

import json
import os
from os import path
from statistics import mean
from scipy.stats import norm, sem

dicts = {}
apps = set()

for file in sorted(os.listdir("runlog")):
    with open(path.join("runlog", file), "rt") as f:
        data = f.read()
        marker = ">>>>\n"
        index = data.find(marker)
        if index != -1:
            j = data[index+len(marker):]
            j = json.loads(j)

            def do_item(name):
                if name not in j:
                    return
                if name not in dicts:
                    dicts[name] = {}
                for app, val in j[name].items():
                    if app not in dicts[name]:
                        dicts[name][app] = []
                    dicts[name][app].append(val)
                    apps.add(app)
            for n in j.keys():
                if n == "app_profiling_info":
                    app_profiling_info = j[n]
                    for app, pinfo in app_profiling_info.items():
                        for key, val in pinfo.items():
                            dkey = f"app_profiling_{key}"
                            if dkey not in dicts:
                                dicts[dkey] = {}
                            if app not in dicts[dkey]:
                                dicts[dkey][app] = []
                            dicts[dkey][app].append(val)
                            apps.add(app)
                else:
                    do_item(n)

def derived(name, fn):
    dicts[name] = {}
    for app in apps:
        nvalues = {n: dicts[n][app] for n in ["app_modus_prepare_time", "app_modus_time", "app_docker_prepare_time", "app_docker_times"]}
        arr = [0] * len(nvalues["app_modus_time"])
        for i in range(0, len(arr)):
            arr[i] = fn({n: nvalues[n][i] for n in nvalues})
        dicts[name][app] = arr

derived("app_modus_total_time", lambda d: d["app_modus_prepare_time"] + d["app_modus_time"])
derived("app_docker_total_time", lambda d: d["app_docker_prepare_time"] + d["app_docker_times"])

# colorder = ["app_modus_prepare_time", "app_modus_time", "app_profiling_resolving_total", "app_profiling_exporting_total", "app_docker_prepare_time", "app_docker_times"]
# print("| app | Update version list (Modus) | Modus build total time | Modus Resolving time | Modus Exporting time | upstream ./update.sh | upstream Docker build | n |")
# print("| --- | --- | --- | --- | --- | --- | --- | --- |")
# for app in sorted(apps):
#     cols = {}
#     n = -1
#     for name in dicts.keys():
#         if app not in dicts[name] or len(dicts[name][app]) == 0:
#             continue
#         app_vals = dicts[name][app][:64]
#         if n == -1:
#             n = len(app_vals)
#         elif n != len(app_vals):
#             print(f"ERROR: {app}: len mismatch")
#         m = mean(app_vals)
#         s = sem(app_vals)
#         if s > 1e-6:
#             left, right = norm.interval(0.95, loc=m, scale=s)
#             if left < 0:
#                 left = 0
#             cols[name] = f"{m:.2f} ({left:.2f} - {right:.2f})"
#         else:
#             cols[name] = f"{m:.2f}"
#     print(f"| {app} | {' | '.join((cols[n] if n in cols else '-') for n in colorder)} | {n} |")

colorder = ["app_docker_times", "app_modus_time"]
for app in sorted(apps):
    cols = {}
    n = -1
    for name in dicts.keys():
        if app not in dicts[name] or len(dicts[name][app]) == 0:
            continue
        app_vals = dicts[name][app]
        if n == -1:
            n = len(app_vals)
        elif n != len(app_vals):
            print(f"ERROR: {app}: len mismatch")
        m = mean(app_vals)
        s = sem(app_vals)
        if s > 1e-6:
            left, right = norm.interval(0.95, loc=m, scale=s)
            if left < 0:
                left = 0
            cols[name] = f"{m:.2f} & {left:.2f}--{right:.2f}"
        else:
            cols[name] = f"{m:.2f} & {m:.2f}--{m:.2f}"
    print(f"\\textbf{{{app}}} & {' & '.join((cols[n] if n in cols else '- & -') for n in colorder)} \\\\")
