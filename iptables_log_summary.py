#! /usr/bin/env python


'''
Find the number of dropped connection messages from remote machines to local ports
'''
import sys
import glob
import gzip
import socket
import datetime
import time

print "\nBeginning analysis of /var/log/messages"
lfile = '/var/log/messages'

files = glob.glob("/var/log/messages*")

now = datetime.datetime.now()

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
      event["month"] = line[0]
      event["day"] = line[1]
      event["time"] = line[2]
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
      port = "MULTI"
      if 'DPT' in e:
        port = e['DPT']

      date = time.strptime(str(now.year) + " " + str(e["month"]) + " " + str(e["day"].zfill(2)) + " "+ str(e["time"]), "%Y %b %d %H:%M:%S")

      knownconn = False
      if port not in uniqueports:
        uniqueports.append(port)
      if ip in conns:
        if port in conns[ip]:
          conns[ip][port] += 1
          if (conns[ip]["date"] < date):
            conns[ip]["date"] = date
        else:
          conns[ip][port] = 1
      else:
        hostname = "NXDOMAIN"
        try:
          hostname = socket.gethostbyaddr(origip)[0]
        except:
          pass
        conns[ip] = {port: 1, "hostname": hostname, "date" : date}
    except Exception, myerr:
      #sys.stdout.write( str(myerr))
      pass

  # Print the machine and dest port and the number of times.

  print "\nDROP Log Messages\nLast Connection Date\t Source IP\tPort\tCount\tHostname"
  for ip in conns:
    for port in conns[ip]:
      if port != "hostname" and port != "date": #terrible exclusion
        print time.strftime("%x %X", conns[ip]["date"]) + "\t" + ip.replace('_','.') + "\t" + port + "\t" + str(conns[ip][port]) + "\t" + conns[ip]["hostname"]
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
    #sys.stdout.write(type + " ");
    start = 0
    if type == "IPTABLES":
      start = 6
    elif type == "IPTABLES-DROP:":
      start = 6
    event = parseline(l,start)
    registerevent(event)

summarizeevents()
