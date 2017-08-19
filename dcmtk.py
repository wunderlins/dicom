#!/usr/bin/env python

import subprocess
import re

def run(cmd, handler=None):
	proc = subprocess.Popen(cmd, 
	                         stdout=subprocess.PIPE, 
	                         stderr=subprocess.PIPE,
	                         stdin=subprocess.PIPE)
	
	if handler == None:
		for line in iter(proc.stdout.readline, ""):
			#line = proc.stdout.readline().rstrip()
			line = line.rstrip()
			if not line:
				break
			print line
	else:
		handler(proc, cmd)


def vertical_tabs(proc, cmd):
	for line in iter(proc.stdout.readline, ""):
		#line = proc.stdout.readline().rstrip()
		line = line.rstrip()
		if not line:
			break
		print re.sub('([^ ]) ', '\\1 | ', line)


run(["ls", "-la"])
run(["ls", "-la"], vertical_tabs)

"""
for line in stdout.split("\n"):
  if line != '':
    #the real code does filtering here
    print "test:", line.rstrip()
  else:
    break
#out, err = p.communicate('foo\nfoofoo\n')
"""
