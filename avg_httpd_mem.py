#! /usr/bin/python

import sys
import time
import datetime
import os
import subprocess
from subprocess import call

if len(sys.argv) > 1:
  freq = sys.argv[1]
else:
  freq = 5

while True:
  command = "ps aux"
  process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  os.waitpid(process.pid, 0)
  output = process.stdout.read().strip().split('\n')
  count = 0
  total = 0
  for line in output:
    if "bin/httpd" in line and "root" not in line:
      line = line.split()
      total += int(line[5])
      count += 1

  if count > 0:
    print str(time.time()) + " Avg Resident Mem: " + str(total/count) + " (" + str((total/count)/1000) + " MB) for " + str(count) + " processes."

  time.sleep(int(freq))
