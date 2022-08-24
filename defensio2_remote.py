#!/usr/bin/env python
# Module Imports
import mariadb
import nmap
import time
import sys
from datetime import datetime


while True:
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

    cur = conn.cursor()
    # estrazione parametri del job selezionato
    cur.execute('SELECT id_job,ip,netmask FROM job  WHERE abilitato="on" AND esecuzione="off"')

    for (id_job, ip, netmask ) in cur:
        print(id_job,ip,netmask)


        # costruzione stringa ip/netmask
        id_j = id_job
        ip_net = ip + '/' + netmask
        print(ip_net)

        sql_update_query = """UPDATE job SET esecuzione = %s WHERE id_job  = %s"""
        input_data = ('on', id_job)

        print("Esecuzione del job "+str(id_job))
        #scrive il tag esecuzione sul record del job
        #cur.execute(sql_update_query, input_data)

        
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
            cur.execute("INSERT INTO host (id,id_job,start_job,ip,hostname) VALUES (%s,%s,%s,%s,%s)", (vuoto, id_j, start_job, host, nm[host].hostname()))

             # ciclo for per i protocolli riscontrati
            for proto in nm[host].all_protocols():

                # creazione di una lista di porte trovate nella scansione
                localport = nm[host][proto].keys()

                # ordine delle porte scoperte
                sorted(localport)

                # ciclo for sulle porte scoperte
                for port in localport:

                    # inserimento SQL nella tabella Port
                    cur.execute("INSERT INTO Port (id_port,id_job,ip,port_n,name,state,reason,product,version,info) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(vuoto, id_j, host, port, nm[host][proto][port]['name'], nm[host][proto][port]['state'],nm[host][proto][port]['reason'], nm[host][proto][port]['product'], nm[host][proto][port]['version'],nm[host][proto][port]['extrainfo']))

    conn.commit()
    time.sleep(5)
    print("attesa ciclo")
    cur.close()
    conn.close()
