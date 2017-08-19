#!/usr/bin/env python
import sys
import os
import atexit
import socket

config = {
	"host":  "127.0.0.1",
	"port":  7000,
	"debug": True
}

glob = {
	"cwd": os.path.dirname(os.path.realpath(__file__)),
	"pidfile": os.path.splitext("httpd.py")[0] + ".pid"
}

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
	
	def __init__(self, type, name=None, desc=None, options=None):
		self.type = type
		
		if name != None:
			self.name = name
			
		if desc != None:
			self.desc = desc
			
		if options != None:
			self.options = options

class param_group:
	items = None
	name  = None
	
	def __init__(self, name):
		self.items = []
		self.name = name
	
	def append(self, item):
		self.items.append(item)
	
	def __str__(self):
		buffer = "<" + self.name + ": "
		for e in self.items:
			buffer += str(e.name) + ", "
		buffer += "\b\b>"
		return buffer
			
	def __repr__(self):
		return self.__str__()	
	
def check_pid(pid):
	""" Check For the existence of a unix pid. """
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	except:
		return False
	
	return True

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/mwl-server')
def mwl_server():
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
	parameters.append(parameter(parameter.TYPE_INTEGER, "port", "tcp/ip port number to listen on"))
	section.append(parameters)
	
	general_options = param_group("general_options")
	general_options.append(parameter(parameter.TYPE_BOOL, "--debug", "debug mode, print debug information"))
	general_options.append(parameter(parameter.TYPE_ONEOF, "--log-level", "[l]evel: string constant (fatal, error, warn, info, debug, trace) use level l for the logger", ["fatal", "error", "warn", "info", "debug", "trace"]))
	section.append(general_options)

	print parameters
	
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
		--data-files-path      [p]ath: string (default: /home/www/wlist)
		                               path to worklist data files
		handling of worklist files:
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
	
	
	return render_template('mwl-server.html')

# start server
def startup():
	# my paid
	pid = os.getpid()
	
	# open pid file, we have tested in main if it is readable
	pidfp = open(get_pid_file(), "wb+")
	pidfp.truncate()
	pidfp.write(str(pid))
	pidfp.close()
	
	app.run(host=config["host"], port=config["port"], debug=config["debug"])

# cleanup before shutdown
def shutdown():
	sys.stdout.write("Shutting down ... ")
	try:
		os.remove(get_pid_file())
	except:
		pass
	
	print "done."

atexit.register(shutdown)

def get_pid_file():
	return glob["cwd"] + "/" + glob["pidfile"]

if __name__ == "__main__":
	#print "pid: %d, lock file: %s" % (pid, glob["pidfile"])
	
	pidfile = get_pid_file()
	#print pidfile
	#print os.path.isfile(pidfile)
	
	pidfile_content = None
	pidfp = None
	
	# check if pid file exists
	# if exists
	if os.path.isfile(pidfile):
		# open and get contents
		try:
			pidfp = open(pidfile, "wb+")
			# read value
			pidfile_content = pidfp.read()
			pidfp.close()
		
		# deal with file handling errors
		except IOError as err:
			sys.stderr.write("Error opening the file {0}: {1}\n".format(filename, err))
			sys.exit(1)
		
		# deal with other errors
		except:
			sys.stderr.write("Unknwon error while reading file {0}: {1}\n".format(filename, 
				sys.exc_info()[0]))
			sys.exit(2)
		
		# abort sratrtup because pocess is already running
		if pidfile_content and check_pid(int(pidfile_content)) == True:
			# exit
			sys.stderr.write("Program already running, pid: %s. Aborting!" % pidfile_content)
			sys.exit(3)
	
	# if we got this far:
	# - we have no pid file
	# - pid file content does not contain a pid of a running process
	
	# try to launch http deamon
	try:
		startup()
	
	except SystemExit:
		pass
		
	except socket.error:
		sys.stderr.write("Unable to bind socket: {0}\n".format(sys.exc_info()[0]))
		sys.exit(10)
		
		
	# deal with startup errors
	except:
		sys.stderr.write("Error while starting httpd: {0}\n".format(sys.exc_info()[0]))
		sys.exit(20)

