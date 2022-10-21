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

def update_statistic_host(id_j):

    id_job=id_j
    #crea il record della statistica del job

    stat_host = conn.cursor()
    sql_insert_query = """INSERT INTO statistic_job (id_statistic, id_job, Log, Medium, High, N_host, N_service) VALUES (NULL, %s, NULL, NULL, NULL, NULL, NULL); """

    job_data = list()
    job_data.append(id_job)

    stat_host.execute(sql_insert_query, job_data)
    conn.commit()


    #estrae il numero di host trovati per lo specifico job
    sql_query_host_for_job = """ SELECT COUNT(ip) FROM host WHERE id_job= %s; """
    stat_host.execute(sql_query_host_for_job, job_data)
    result = stat_host.fetchone()
    n_host = result[0]

    #estrae i servizi(porte) trovate aperte in un job
    sql_query_service_for_job = """SELECT COUNT(port_n) FROM Port WHERE id_job = %s;"""
    stat_host.execute(sql_query_service_for_job, job_data)
    result = stat_host.fetchone()
    n_service = result[0]

    sql_update_query = """UPDATE statistic_job SET N_host = %s , N_service = %s WHERE statistic_job.id_job = %s; """
    update_data = (n_host, n_service, id_job)
    stat_host.execute(sql_update_query, update_data)
    conn.commit()


id_ass = input("inserisci il numero di assetto:")
id_asset = list()
id_asset.append(id_ass)



while True:

    connessione = DB_connect.database_connect()
    conn=connessione.database_connection("operator","!d3f3n510!", '185.245.183.75', 3306, "defensio")

    id_j=''
    # estrazione parametri del job selezionato

    cur = conn.cursor()



    cur.execute('SELECT id_job,id_asset,ip,netmask, single_port, low_port, high_port FROM job  WHERE abilitato="on" AND net_discovery="off" AND id_asset = %s',(id_asset))
    if cur.rowcount != 0:
        result = cur.fetchone()
        print("*************************************************************************************************************************************")
        print("Scansione Defensio Engine in esecuzione: Job n° "+str(result[0])+" | Assetto n° "+str(result[1])+" ! Target "+str(result[2])+" | Netmask "+str(result[3]))

        id_j=result[0]
        ip=result[2]
        netmask=result[3]
        ip_net=ip+'/'+netmask
        single_port = str(result[4])
        low_port = result[5]
        high_port = result[6]
        if single_port != 'None':
            port_target = single_port
        else:
            port_target = str(low_port) + "-" + str(high_port)
        print("Scansione attiva sulle porte: "+port_target)

        argument="-sV -p"+port_target
        print(argument)
        # genera la stringa di inizio del job
        start_job = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Time avvio job: "+str(start_job))
        # variabile None da utilizzare nelle interrogazioni SQL per i campi autoincrementali
        vuoto = None

        # oggetto portscanner

        try:
            nm = nmap.PortScanner()

            # scansione secondo parametri del job
            nm.scan(hosts=ip_net, arguments= argument)
            for host in nm.all_hosts():
                print("** Host trovato: "+host)
                # inserimento SQL nella tabella HOST
                cur.execute("INSERT INTO host (id,id_job,start_job,ip,hostname) VALUES (%s,%s,%s,%s,%s)",
                            (vuoto, id_j, start_job, host, nm[host].hostname()))

                # ciclo for per i protocolli riscontrati
                for proto in nm[host].all_protocols():
                    print("  L____ Protocollo attivo: "+proto)
                    # creazione di una lista di porte trovate nella scansione
                    localport = nm[host][proto].keys()

                    # ordine delle porte scoperte
                    sorted(localport)

                    # ciclo for sulle porte scoperte
                    for port in localport:
                        print("      L____ Servizio attivo sulla porta: "+str(port)+" | Servizio: "+nm[host][proto][port]['name']+" | Stato:"+nm[host][proto][port]['state'])
                        # inserimento SQL nella tabella Port
                        try:
                            cur.execute(
                                "INSERT INTO Port (id_port,id_job,ip,port_n,name,state,reason,product,version,info) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (vuoto, id_j, host, port, nm[host][proto][port]['name'], nm[host][proto][port]['state'],
                             nm[host][proto][port]['reason'], nm[host][proto][port]['product'],
                             nm[host][proto][port]['version'], nm[host][proto][port]['extrainfo']))
                        except:
                            print("errore nell inserimento dei risultati nella tabella port")
        except:
            print('errore in nmap')

        #aggiorna la statistica del job della tabella statistic_job

        try:
            update_statistic_host(id_j)
        except:
            print('errore nell\'update della tabella statistica')

        #esegue la scansione con arachni

        try:
            arac = conn.cursor()
            arac.execute(
                "SELECT Port.id_job, Port.ip,port_n FROM `Port` INNER JOIN job ON job.id_job=Port.id_job WHERE (Port.name='http' OR Port.port_n = '80') AND job.arachni='on';")
            if arac.rowcount != 0:
                result = arac.fetchone()
                print(result)
                id_j = result[0]
                ip_target = result[1]
                port_target = result[2]

                obj = arachni.arachni_class()
                obj.arachni_http(id_j, ip_target, port_target)
                arachni_sql_report = "INSERT INTO arachni_report (id_arac_report, id_job) VALUES (NULL, %s);"
                bho = list()
                bho.append(id_j)
                arac.execute(arachni_sql_report, bho)

            sql_update_query = """UPDATE job SET arachni = %s WHERE id_job  = %s"""
            input_data = ('off', result[0])
            arac.execute(sql_update_query, input_data)

            conn.commit()
            arac.close()
        except:
            print('errore in arachni')


        #esegue la scansione con enum4linux

        try:
            enum4linuxqueryjob = conn.cursor()
            enum4linuxqueryjob.execute(
                "SELECT Port.id_job, Port.ip, port_n FROM `Port` INNER JOIN job ON job.id_job = Port.id_job WHERE Port.name = 'netbios-ssn' AND job.enumforlinux = 'on';")

            if enum4linuxqueryjob.rowcount != 0:
                result_enum_job = enum4linuxqueryjob.fetchone()
                print(result_enum_job)
                id_j = result_enum_job[0]
                ip_target = result_enum_job[1]

                file_name = str(id_j) + '_' + ip_target
                print(file_name)
                cmd = subprocess.run(["./enumforlinux/enum4linux-ng.py", "-A", ip_target, "-oJ", file_name])

                obj_enum4linux_json = enum4linux_read_json.enum4linux_read_json_class()
                obj_enum4linux_json.enum4linux_read_json(id_j, start_job, file_name + '.json')

            sql_update_query = """UPDATE job SET enumforlinux = %s WHERE id_job  = %s"""
            input_data = ('off', result[0])
            enum4linuxqueryjob.execute(sql_update_query, input_data)
            conn.commit()
            enum4linuxqueryjob.close()

        except:
            print('errore in enum4linux')



        # scrive il tag esecuzione sul record del job
        cur = conn.cursor()
        sql_update_query = """UPDATE job SET net_discovery = %s WHERE id_job  = %s"""
        input_data = ('on', result[0])
        cur.execute(sql_update_query, input_data)
        conn.commit()
        cur.close()
        conn.close()
    time.sleep(5)