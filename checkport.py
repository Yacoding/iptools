#!/usr/bin/python
# encoding: utf-8
"""
checkport.py
Created by Michael Haskell on 2010-10-15
"""
import sys
import getopt
import socket
import datetime

# Test a tcp or udp port for response

"""
TCP
	rdp	3389
	http 80
UDP
	
"""

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg
	
def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "h:p:t:", ["host=", "port=", "type="])
		except getopt.error, msg:
			raise Usage(msg)

		# check for valid arguments
		if len(opts) == 0:
			raise Usage("./checkport.py -h hostname -p port [-t (udp|tcp)]")

		# set global variables
		for option, value in opts:
			if option in ("-h", "--host"):
				host = value
			if option in ("-p", "--port"):
				port = value
			if option in ("-t", "--type"):
				ptype = value
			else: 
				ptype = 'tcp'

		# Execute primary function
		if ptype == "tcp":
			checkTCPPort(host,port)
		elif ptype =="udp":
			checkUDPPort(host,port)

		# Exit
		sys.exit(1)

	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "Available Options: ./checkport.py -h hostname -p port [-t (udp|tcp)]"
		return 2

def checkTCPPort(host, port):
	curtime = datetime.datetime.now()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host, int(port)))
		s.shutdown(2)
		printSuccess(host, port, "TCP", curtime)
	except Exception, e:
		printFailure(host, port, "TCP", curtime, e)
		
def checkUDPPort(host, port):
	curtime = datetime.datetime.now()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect((host, int(port)))
		s.shutdown(2)
		printSuccess(host, port, "UDP", curtime)
	except Exception, e:
		printFailure(host, port, "UDP", curtime, e)

def printSuccess(host, port, ptype, curtime):
	print str(curtime) + " INFO Success connecting to " + host + " on " + ptype + " port: " + str(port)
	
def printFailure(host, port, ptype, curtime, e):
	print str(curtime) + " ALERT Cannot connect to " + host + " on " + ptype + " port: " + str(port) + " " + str(e)

if __name__ == "__main__":
	sys.exit(main())

