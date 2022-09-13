#!/usr/bin/env python3
# Module Imports
import subprocess
import sys
import time
from datetime import datetime
import arachni
import DB_connect
import enum4linux_read_json
import mariadb
import nmap

while True:

    connessione = DB_connect.database_connect()
    conn=connessione.database_connection("operator","!d3f3n510!", '185.245.183.75', 3306, "defensio")

    id_j=''
    # estrazione parametri del job selezionato

    cur = conn.cursor()

    cur.execute('SELECT id_job,ip,netmask FROM job  WHERE abilitato="on" AND esecuzione="off"')
    if cur.rowcount != 0:
        result = cur.fetchone()
        print(result)

        id_j=result[0]
        ip=result[1]
        netmask=result[2]
        ip_net=ip+'/'+netmask
        print(ip_net)
        # genera la stringa di inizio del job
        start_job = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(start_job)
        # variabile None da utilizzare nelle interrogazioni SQL per i campi autoincrementali
        vuoto = None

        # oggetto portscanner
        nm = nmap.PortScanner()

        # scansione secondo parametri del job
        nm.scan(hosts=ip_net, arguments='-sV -p130-447')
        for host in nm.all_hosts():
            print(host)
            # inserimento SQL nella tabella HOST
            cur.execute("INSERT INTO host (id,id_job,start_job,ip,hostname) VALUES (%s,%s,%s,%s,%s)",
                        (vuoto, id_j, start_job, host, nm[host].hostname()))

            # ciclo for per i protocolli riscontrati
            for proto in nm[host].all_protocols():
                print(proto)
                # creazione di una lista di porte trovate nella scansione
                localport = nm[host][proto].keys()

                # ordine delle porte scoperte
                sorted(localport)

                # ciclo for sulle porte scoperte
                for port in localport:
                    print(port)
                    # inserimento SQL nella tabella Port
                    cur.execute(
                        "INSERT INTO Port (id_port,id_job,ip,port_n,name,state,reason,product,version,info) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (vuoto, id_j, host, port, nm[host][proto][port]['name'], nm[host][proto][port]['state'],
                         nm[host][proto][port]['reason'], nm[host][proto][port]['product'],
                         nm[host][proto][port]['version'], nm[host][proto][port]['extrainfo']))


        # scrive il tag esecuzione sul record del job
        sql_update_query = """UPDATE job SET esecuzione = %s WHERE id_job  = %s"""
        input_data = ('on', result[0])
        cur.execute(sql_update_query, input_data)
        conn.commit()
        cur.close()

        arac = conn.cursor()
        arac.execute("SELECT Port.id_job, Port.ip,port_n FROM `Port` INNER JOIN job ON job.id_job=Port.id_job WHERE Port.name='http' AND job.arachni='on';")



        if arac.rowcount != 0:
            result = arac.fetchone()
            print(result)
            id_j = result[0]
            ip_target = result[1]
            port_target = result[2]

            obj = arachni.arachni_class()
            obj.arachni_http(id_j,ip_target, port_target)
            arachni_sql_report = "INSERT INTO arachni_report (id_arac_report, id_job) VALUES (NULL, %s);"
            bho = list()
            bho.append(id_j)
            arac.execute(arachni_sql_report, bho)

        sql_update_query = """UPDATE job SET arachni = %s WHERE id_job  = %s"""
        input_data = ('off', result[0])
        arac.execute(sql_update_query, input_data)


        conn.commit()
        arac.close()

        #enumforlinux module

        enum4linuxqueryjob = conn.cursor()
        enum4linuxqueryjob.execute("SELECT Port.id_job, Port.ip, port_n FROM `Port` INNER JOIN job ON job.id_job = Port.id_job WHERE Port.name = 'netbios-ssn' AND job.enumforlinux = 'on';")

        if enum4linuxqueryjob.rowcount != 0:

            result_enum_job = enum4linuxqueryjob.fetchone()
            print(result_enum_job)
            id_j = result_enum_job[0]
            ip_target = result_enum_job[1]


            file_name = str(id_j)+'_'+ip_target
            print(file_name)
            cmd = subprocess.run(["./enumforlinux/enum4linux-ng.py", "-A", ip_target, "-oJ", file_name])


            obj_enum4linux_json = enum4linux_read_json.enum4linux_read_json_class()
            obj_enum4linux_json.enum4linux_read_json(id_j,start_job,file_name+'.json' )

            sql_update_query = """UPDATE job SET enumforlinux = %s WHERE id_job  = %s"""
            input_data = ('off', result[0])
            enum4linuxqueryjob.execute(sql_update_query, input_data)

        enum4linuxqueryjob.close()
        conn.close()

    time.sleep(5)