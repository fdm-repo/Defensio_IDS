#!/usr/bin/env python3
# Module Imports
import nmap
import xml
import time
import sys
import os
from datetime import datetime
from libnmap.process import NmapProcess
from time import sleep
import subprocess
ipnet = "localhost/32"
port_target = '20-1024'

argument = "-O -sV -p" + port_target


nm = nmap.PortScanner()
nm.scan(hosts=ipnet, arguments=argument)
print(nm.command_line())
print(nm.scaninfo())
print(nm.all_hosts())
print(nm.scanstats())


for host in nm.all_hosts():
    print('Host: '+host)
    lista=list(nm[host].values())
    print(lista)
    os = nm[host]['osmatch'][0]['name']
    print(os)
    os_accuracy = nm[host]['osmatch'][0]['accuracy']
    print(os_accuracy)
    type = nm[host]['osmatch'][0]['osclass'][0]['type']
    print(type)

