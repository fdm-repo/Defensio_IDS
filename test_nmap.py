#!/usr/bin/env python
# Module Imports
import nmap
import xml
import time
import sys
import os
from datetime import datetime

#ip=input("Insert IP Target: ")
#netmask=input("Insert Netmask: ")
ip = 'localhost'
netmask = '32'

ip_net=ip+'/'+netmask

nm = nmap.PortScanner()

# scansione secondo parametri del job
nm.scan(hosts=ip_net, arguments='-sV --script vulners -p80')




for host in nm.all_hosts():
    print('Host: '+host)
    lista=list(nm[host].values())
    print(lista)
    for i in range(len(lista)):
        print('i '+str(i))
        print(lista[i])
        if len(lista[i])==1:
            continue
        for a in range(len(lista[i])):
            print('a '+str(a)+' su '+str(len(lista[i])))
            print(lista[i][a])



    # ciclo for per i protocolli riscontrati
    '''for proto in nm[host].all_protocols():
        print('Protocollo: '+proto)
        # creazione di una lista di porte trovate nella scansione
        localport = nm[host][proto].keys()

        # ordine delle porte scoperte
        sorted(localport)
        print('+++++++++++++++++++++++++++')
        # ciclo for sulle porte scoperte
        for port in localport:
           
            print(nm[host][proto][port])
            print('Port: '+str(port))
            print('Name: '+nm[host][proto][port]['name'])
            print('State: '+nm[host][proto][port]['state'])
            print('Reason: '+nm[host][proto][port]['reason'])
            print('Service: '+nm[host][proto][port]['product'])
            print('Version: '+nm[host][proto][port]['version'])
            print('Info: '+nm[host][proto][port]['extrainfo'])
            print('----------------------------------')'''