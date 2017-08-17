#!/usr/bin/env python
import sys, os
import atexit

config = {
	"host":  "127.0.0.1",
	"port":  7000,
	"debug": True
}

glob = {
	"cwd": os.path.dirname(os.path.realpath(__file__)),
	"pidfile": os.path.splitext("httpd.py")[0] + ".pid"
}

def check_pid(pid):
	""" Check For the existence of a unix pid. """
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	except:
		return False
	else:
		return True

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

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
	
	# check if pid file exists
	# if exists
	pidfile_content = None
	pidfp = None
	
	if os.path.isfile(pidfile):
		# open
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
			sys.stderr.write("Unknwon error while reading file {0}: {1}\n".format(filename, err))
			sys.exit(2)
		
		# check if process is running
		# is running 
		if pidfile_content and check_pid(int(pidfile_content)) == True:
			# exit
			sys.stderr.write("Program already running, pid: %s. Aborting!" % pidfile_content)
			sys.exit(3)
		
	# pid file does not exist, try to launch http deamon
	startup()
	
	
	



