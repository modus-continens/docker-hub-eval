#!/usr/bin/env python

import os
import subprocess
import json
os.chdir("upstream.git")
subprocess.run("./versions.sh", check=True, stdout=subprocess.DEVNULL)
versions_json = json.load(open("versions.json", "rt"))
for major_version, vv in versions_json.items():
	shell_version = vv["mysql-shell"]["version"]
	if "debian" in vv:
		t = vv["debian"]
		variant = t["suite"]
		version = t["version"]
		for arch in t["architectures"]:
			print(f'mysql_version("{version}","{major_version}","debian","{variant}","{arch}","{shell_version}").')
	if "oracle" in vv:
		t = vv["oracle"]
		variant = t["variant"]
		version = t["version"]
		for arch in t["architectures"]:
			print(f'mysql_version("{version}","{major_version}","oracle","{variant}","{arch}","{shell_version}").')
