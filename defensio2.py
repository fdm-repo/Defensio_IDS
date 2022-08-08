#!/usr/bin/env python
# Module Imports
import mariadb
import nmap
import os
import sys
from datetime import datetime

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="operator",
        password="!d3f3n510!",
        host='192.168.1.246',
        port=3306,
        database="defensio"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor


cur = conn.cursor()
### set NULL variabili globali job
id_j = name_j = ip_j = netmask_j = ip_net = ''
### estrazione parametri job
cur.execute(
    'SELECT * FROM job  WHERE 1')
print('Elenco Job\n')
for (id_job, name, ip, netmask) in cur:
    id_j = id_job
    name_j = name
    ip_j = ip
    netmask_j = netmask
    # costruzione stringa ip/netmask
    ip_net = ip + '/' + netmask
    print('Job n°:%s\tName:%s\tIp Target:%s' % (id_j, name_j, ip_net))
# selezione da cli del job da eseguire
n_job = input("select Job:")
# estrazione parametri del job selezionato
cur.execute(
    'SELECT ip,netmask FROM job  WHERE id_job=%s' % (n_job))
for (ip, netmask) in cur:
    # costruzione stringa ip/netmask
    ip_net = ip + '/' + netmask

# genera la stringa di inizio del job
start_job = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# variabile None da utilizzare nelle interrogazioni SQL per i campi autoincrementali
vuoto = None

# oggetto portscanner
nm = nmap.PortScanner()

# scansione secondo parametri del job
nm.scan(hosts=ip_net, arguments='-sV -p20-1024')
for host in nm.all_hosts():

    # inserimento SQL nella tabella HOST
    cur.execute("INSERT INTO host (id,id_job,start_job,ip,hostname) VALUES (%s,%s,%s,%s,%s)",
                (vuoto, id_j, start_job, host, nm[host].hostname()))
    # se richiesto os fingerprinting
    if 'osmatch' in nm[host]:
        for osmatch in nm[host]['osmatch']:
            print('OsMatch.name : {0}'.format(osmatch['name']))
            print('OsMatch.accuracy : {0}'.format(osmatch['accuracy']))
            print('OsMatch.line : {0}'.format(osmatch['line']))
            print('')

    if 'fingerprint' in nm[host]:
        print('Fingerprint : {0}'.format(nm[host]['fingerprint']))

    # ciclo for per i protocolli riscontrati
    for proto in nm[host].all_protocols():
        # creazione di una lista di porte trovate nella scansione
        localport = nm[host][proto].keys()
        # ordine delle porte scoperte
        sorted(localport)
        # ciclo for sulle porte scoperte
        for port in localport:
            # inserimento SQL nella tabella Port
            cur.execute(
                "INSERT INTO Port (id_port,id_job,ip,port_n,name,state,reason,product,version,info) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (vuoto, id_j, host, port, nm[host][proto][port]['name'], nm[host][proto][port]['state'],
                 nm[host][proto][port]['reason'], nm[host][proto][port]['product'], nm[host][proto][port]['version'],
                 nm[host][proto][port]['extrainfo']))

cur.execute(
    'SELECT id,ip FROM host where id_job=%s' % (id_j))

for (id, ip) in cur:
    print(f"Indice: {id}, Indirizzo IP: {ip}")
conn.commit()
print(f"Last Inserted ID: {cur.lastrowid}")

conn.close()
