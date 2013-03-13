#!/usr/bin/env python
import os, sys, subprocess

try:
    os.makedirs('hpdbs')
except:
    pass
for arg in sys.argv[1:]:
    cmd = ["../../reduce", arg]
    f = open('hpdbs/'+arg, 'w')
    f.write(subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout)
    f.close()

