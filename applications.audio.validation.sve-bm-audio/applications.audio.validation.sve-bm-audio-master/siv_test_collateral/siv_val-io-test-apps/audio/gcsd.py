import sys
import os
import argparse
import subprocess
from daemon import Daemon

parser = argparse.ArgumentParser(description = 'Daemonize GenericCommandServer')
parser.add_argument('action', action="store", default='start', 
                    help="start, stop or restart")

parsed_args = parser.parse_args()

# initialize daemon
class GCSDaemon(Daemon):
    def run(self):
        execfile("/usr/local/gv/GenericCommand/GenericCommandServer.py")

pid_file = "/tmp/gcsd.pid"
daemon = GCSDaemon(pid_file, "/dev/null", "/usr/local/gv/var/log/gcsd.log", "/usr/local/gv/var/log/gcsd.log")
if 'start' == parsed_args.action:
    daemon.start()
elif 'stop' == parsed_args.action:
    daemon.stop()
elif 'restart' == parsed_args.action:
    daemon.restart()
else:
    print "Unknown command"
    sys.exit(2)
sys.exit(0)
