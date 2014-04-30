#! /usr/bin/env python


'''
Find the number of dropped connection messages from remote machines to local ports
  built to check /var/log/messages to assist in establishing iptables rules.
'''
import sys
import glob
import gzip
import socket

print "\nBeginning analysis of /var/log/messages"
lfile = '/var/log/messages'

files = glob.glob("/var/log/messages*") 

events = []

def parseline(line,start):
  event= {}
  try:
    for item in line[start:-1]:
      item = item.split("=")
      key = item[0]
      if len(item) > 1:
        val = item[1]  
      else: 
        val = '';
      event[key] = val
    return event
  except:
    pass

def registerevent(event):
  events.append(event)

def summarizeevents():
  conns = {}
  uniqueports = []
  for e in events:
    try:
      origip = e['SRC']
      ip = origip.replace(".","_")
      port = e['DPT']
      knownconn = False
      if port not in uniqueports:
        uniqueports.append(port)
      if ip in conns:
        if port in conns[ip]:
          conns[ip][port] += 1
        else:
          conns[ip][port] = 1
      else:
        hostname = " - "
        try:
          hostname = socket.gethostbyaddr(origip)[0]
        except:
          pass
        conns[ip] = {port: 1, "hostname": hostname}
    except:
      pass

  # Print the machine and dest port and the number of times.
  
  print "\nDROP Log Messages\nSource IP\tPort\tCount\tHostname"
  for ip in conns:
    for port in conns[ip]:
      if port != "hostname":
        print ip + "\t" + port + "\t" + str(conns[ip][port]) + "\t" + conns[ip]["hostname"] 
  print "\nUnique Destination Ports"
  for p in uniqueports:
    print p

# MAIN
for file in files:
  logs = None
  print "  Parsing " + file
  if "gz" in str(file):
    logs = gzip.open(file, "rb")
  else:
    logs = open(file, "r")
  for line in logs:
    l =  line.split()
    type = l[5]
    start = 0
    if type == "IPTABLES":
      start = 6
    elif type == "IPTABLES-DROP":
      start = 7
    event = parseline(l,start)
    registerevent(event)
  
summarizeevents()
