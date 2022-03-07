#!/usr/bin/env python3

# for i in (seq 1 100); for j in ubuntu redis node mysql traefik; ./run-all.py $j > ~/runlog/$i-$j.log; sleep 1; end; end

import json
import os
from os import path
from statistics import mean
from scipy.stats import norm, sem

dicts = {}
apps = set()

for file in os.listdir("runlog"):
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
                do_item(n)

colorder = ["app_modus_prepare_time", "app_modus_time", "app_docker_prepare_time", "app_docker_times"]
print("| app | Update version list (Modus) | Modus build | upstream ./update.sh | upstream Docker build | n |")
print("| --- | --- | --- | --- | --- | --- |")
for app in apps:
    cols = {}
    for name in dicts.keys():
        if app not in dicts[name] or len(dicts[name][app]) == 0:
            continue
        app_vals = dicts[name][app]
        m = mean(app_vals)
        s = sem(app_vals)
        if s > 1e-6:
            left, right = norm.interval(0.95, loc=m, scale=s)
            if left < 0:
                left = 0
            cols[name] = f"{m:.2f} ({left:.2f} - {right:.2f})"
        else:
            cols[name] = f"{m:.2f}"
    print(f"| {app} | {' | '.join((cols[n] if n in cols else '-') for n in colorder)} |")
