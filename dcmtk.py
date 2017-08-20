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


#run(["ls", "-la"])
#run(["ls", "-la"], vertical_tabs)

"""
for line in stdout.split("\n"):
  if line != '':
    #the real code does filtering here
    print "test:", line.rstrip()
  else:
    break
#out, err = p.communicate('foo\nfoofoo\n')
"""

class parameter:
	TYPE_NONE    = 0
	TYPE_BOOL    = 1
	TYPE_INTEGER = 2
	TYPE_FLOAT   = 3
	TYPE_STRING  = 4
	TYPE_ONEOF   = 5
	TYPE_MANY    = 6
	
	type = None
	name = None
	desc = None
	group = None
	
	def __init__(self, type, name=None, desc=None, options=None, group=None):
		self.type = type
		
		if name != None:
			self.name = name
			
		if desc != None:
			self.desc = desc
			
		if options != None:
			self.options = options
			
		if group:
			self.group = group

class param_group:
	items = None
	name  = None
	groups = []
	
	def __init__(self, name):
		self.items = []
		self.name = name
	
	def append(self, item):
		self.items.append(item)
		if item.group and item.group not in self.groups:
			self.groups.append(item.group)
	
	def __str__(self):
		buffer = "<" + self.name + ": "
		for e in self.items:
			buffer += str(e.name) + ", "
		buffer += "\b\b>"
		return buffer
			
	def __repr__(self):
		return self.__str__()	
	

def wlmscpfs():
	"""
	wlmscpfs: DICOM Basic Worklist Management SCP (based on data files)
	usage: wlmscpfs [options] port

	parameters:
		port                           tcp/ip port number to listen on

	general options:
		-h      --help                 print this help text and exit
		        --version              print version information and exit
		        --arguments            print expanded command line arguments
		-q      --quiet                quiet mode, print no warnings and errors
		-v      --verbose              verbose mode, print processing details
		-d      --debug                debug mode, print debug information
		-ll     --log-level            [l]evel: string constant
		                               (fatal, error, warn, info, debug, trace)
		                               use level l for the logger
		-lc     --log-config           [f]ilename: string
		                               use config file f for the logger
	multi-process options:
		-s      --single-process       single process mode
		        --fork                 fork child process for each association (def.)
	input options:
		general:
		  -dfp  --data-files-path      [p]ath: string (default: /home/www/wlist)
		                               path to worklist data files
		handling of worklist files:
		  -efr  --enable-file-reject   enable rejection of incomplete worklist files
		                               (default)
		  -dfr  --disable-file-reject  disable rejection of incomplete worklist files
	processing options:
		returned character set:
		  -cs0  --return-no-char-set   return no specific character set (default)
		  -cs1  --return-iso-ir-100    return specific character set ISO IR 100
		  -csk  --keep-char-set        return character set provided in file
		other processing options:
		  -nse  --no-sq-expansion      disable expansion of empty sequences in C-FIND
		                               request messages
	network options:
		preferred network transfer syntaxes:
		  +x=   --prefer-uncompr       prefer explicit VR local byte order (default)
		  +xe   --prefer-little        prefer explicit VR little endian TS
		  +xb   --prefer-big           prefer explicit VR big endian TS
		  +xi   --implicit             accept implicit VR little endian TS only
		network host access control (tcp wrapper):
		  -ac   --access-full          accept connections from any host (default)
		  +ac   --access-control       enforce host access control rules
		post-1993 value representations:
		  +u    --enable-new-vr        enable support for new VRs (UN/UT) (default)
		  -u    --disable-new-vr       disable support for new VRs, convert to OB
		other network options:
		  -ta   --acse-timeout         [s]econds: integer (default: 30)
		                               timeout for ACSE messages
		  -td   --dimse-timeout        [s]econds: integer (default: unlimited)
		                               timeout for DIMSE messages
		        --max-associations     [a]ssocs: integer (default: 50)
		                               limit maximum number of parallel associations
		        --refuse               refuse association
		        --reject               reject association if no implement. class UID
		        --no-fail              don't fail on an invalid query
		        --sleep-after          [s]econds: integer
		                               sleep s seconds after find (default: 0)
		        --sleep-during         [s]econds: integer
		                               sleep s seconds during find (default: 0)
		  -pdu  --max-pdu              [n]umber of bytes: integer (4096..131072)
		                               set max receive pdu to n bytes (default: 16384)
		  -dhl  --disable-host-lookup  disable hostname lookup

	"""
	
	section = []
	parameters = param_group("parameters")
	parameters.append(parameter(parameter.TYPE_INTEGER, 
	                            "port", 
	                            "tcp/ip port number to listen on"))
	section.append(parameters)
	
	general_options = param_group("general_options")
	general_options.append(parameter(parameter.TYPE_BOOL, 
	                                 "--debug", "debug mode, print debug information"))
	general_options.append(parameter(parameter.TYPE_ONEOF, 
	                                 "--log-level", "[l]evel: string constant (fatal, error, warn, info, debug, trace) use level l for the logger", ["fatal", "error", "warn", "info", "debug", "trace"]))
	section.append(general_options)


	input_options = param_group("input_options")
	input_options.append(parameter(parameter.TYPE_STRING, 
	                     "--data-files-path", 
	                     "[p]ath: string (default: /home/www/wlist) path to worklist data files handling of worklist files:", 
	                     None, 
	                     "general"))
	input_options.append(parameter(parameter.TYPE_BOOL, 
	                     "--enable-file-reject", "enable rejection of incomplete worklist files (default)", 
	                     None, 
	                     "general"))
	input_options.append(parameter(parameter.TYPE_BOOL, 
	                     "--disable-file-reject", "disable rejection of incomplete worklist files", 
	                     None, 
	                     "general"))
	section.append(input_options)

	#print parameters
	
	"""
	parameters:
		port                           tcp/ip port number to listen on

	general options:
		--help                 print this help text and exit
		--version              print version information and exit
		--arguments            print expanded command line arguments
		--quiet                quiet mode, print no warnings and errors
		--verbose              verbose mode, print processing details
		--debug                debug mode, print debug information
		--log-level            [l]evel: string constant (fatal, error, warn, info, debug, trace) use level l for the logger
		--log-config           [f]ilename: string use config file f for the logger
	multi-process options:
		--single-process       single process mode
		--fork                 fork child process for each association (def.)
		
	input options:
		general:
		--data-files-path      [p]ath: string (default: /home/www/wlist) path to worklist data files handling of worklist files:
		--enable-file-reject   enable rejection of incomplete worklist files (default)
		--disable-file-reject  disable rejection of incomplete worklist files
		
	processing options:
		returned character set:
		--return-no-char-set   return no specific character set (default)
		--return-iso-ir-100    return specific character set ISO IR 100
		--keep-char-set        return character set provided in file
		other processing options:
		--no-sq-expansion      disable expansion of empty sequences in C-FIND
		                               request messages
	network options:
		preferred network transfer syntaxes:
		--prefer-uncompr       prefer explicit VR local byte order (default)
		--prefer-little        prefer explicit VR little endian TS
		--prefer-big           prefer explicit VR big endian TS
		--implicit             accept implicit VR little endian TS only
		network host access control (tcp wrapper):
		--access-full          accept connections from any host (default)
		--access-control       enforce host access control rules
		post-1993 value representations:
		--enable-new-vr        enable support for new VRs (UN/UT) (default)
		--disable-new-vr       disable support for new VRs, convert to OB
		other network options:
		--acse-timeout         [s]econds: integer (default: 30) timeout for ACSE messages
		--dimse-timeout        [s]econds: integer (default: unlimited) timeout for DIMSE messages
		--max-associations     [a]ssocs: integer (default: 50) limit maximum number of parallel associations
		--refuse               refuse association
		--reject               reject association if no implement. class UID
		--no-fail              don't fail on an invalid query
		--sleep-after          [s]econds: integer sleep s seconds after find (default: 0)
		--sleep-during         [s]econds: integer sleep s seconds during find (default: 0)
		--max-pdu              [n]umber of bytes: integer (4096..131072) set max receive pdu to n bytes (default: 16384)
		--disable-host-lookup  disable hostname lookup
	"""
	
	for s in section:
		print s.name + " " + str(s.groups)
		for g in s.groups:
			print "--> " + g
		for i in s.items:
			print i.name
	
wlmscpfs()
