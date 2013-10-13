#!/usr/bin/env python

import subprocess, os, math


ps = subprocess.check_output(["ps -A | awk '{print $1}'"], shell=True)
ps = len(ps) - 1
print ps