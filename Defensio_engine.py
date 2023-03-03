#!/usr/bin/env python3
# Module Imports
import json
import os
import sys
import time
from datetime import datetime
from threading import Thread

import nmap
import whois

import DB_connect
import crealog

idprocess = "Defensio_engine"


def whois_public_ip(id_j):
    id_job = id_j

    job = list()
    job.append(id_job)

    job = list()
    job.append(id_job)

    connessione_whois = DB_connect.database_connect()
    conn_whois = connessione_whois.database_connection()

    cur_whois = conn_whois.cursor()
    sql_select = """SELECT ip,public_ip FROM job where id_job = %s; """
    cur_whois.execute(sql_select, job)
    result = cur_whois.fetchone()
    domain = result[0]
    public_ip = result[1]

    log = crealog.log_event()
    log.crealog(idprocess,
                "Esecuzione Whois IP Pubblico " + str(domain) + " del Job " + str(id_job))

    if public_ip == 'si':
        print(domain)
        result_whois = whois.whois(domain).text
        print(result_whois)

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Risultato Whois IP Pubblico " + str(public_ip) + " del Job " + str(id_job))

        sql_update_query = """INSERT INTO `whois_result` (`id_result_whois`, `id_job`, `ip_domain`, `result`) VALUES (NULL,%s,%s,%s);"""
        input_data = (id_job, domain, result_whois)

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Inserito risultato Whois IP Pubblico " + str(domain) + " del Job " + str(id_job) + " nel Database")

        cur_whois.execute(sql_update_query, input_data)
        conn_whois.commit()

    cur_whois.close()
    conn_whois.close()


def update_statistic_host(id_j):
    id_job = id_j
    # crea il record della statistica del job

    connessione_stat_host = DB_connect.database_connect()
    conn_stat_host = connessione_stat_host.database_connection()

    stat_host = conn_stat_host.cursor()
    sql_insert_query = """INSERT INTO statistic_job (id_statistic, id_job, Log, Medium, High, N_host, N_service) VALUES (NULL, %s, NULL, NULL, NULL, NULL, NULL); """

    job_data = list()
    job_data.append(id_job)

    stat_host.execute(sql_insert_query, job_data)
    conn_stat_host.commit()

    # estrae il numero di host trovati per lo specifico job
    sql_query_host_for_job = """ SELECT COUNT(ip) FROM host WHERE id_job= %s; """
    stat_host.execute(sql_query_host_for_job, job_data)
    result = stat_host.fetchone()
    n_host = result[0]

    # estrae i servizi(porte) trovate aperte in un job
    sql_query_service_for_job = """SELECT COUNT(port_n) FROM Port WHERE id_job = %s;"""
    stat_host.execute(sql_query_service_for_job, job_data)
    result = stat_host.fetchone()
    n_service = result[0]

    sql_update_query = """UPDATE statistic_job SET N_host = %s , N_service = %s WHERE statistic_job.id_job = %s; """
    update_data = (n_host, n_service, id_job)
    stat_host.execute(sql_update_query, update_data)
    conn_stat_host.commit()

    stat_host.close()
    conn_stat_host.close()


# setup di configurazione all avvio dell'engine

while True:

    connessione = DB_connect.database_connect()
    conn = connessione.database_connection()

    try:
        data = json.load(open("eng_conf.json"))
    except:
        print("!!! Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
        log = crealog.log_event()
        log.crealog(idprocess,
                    "ERRORRE Connessione Database, eseguire ./inizializzazione_engine.py")
        sys.exit(1)

    id_ass = data['id_ass']
    id_asset = list()
    id_asset.append(id_ass)

    id_j = ''
    # estrazione parametri del job selezionato

    cur = conn.cursor()

    cur.execute('SELECT id_job,id_asset,ip,netmask, single_port, low_port, high_port FROM job  WHERE ((abilitato="on" AND openvas = "off" AND net_discovery="off" ) OR (abilitato="on" AND openvas = "on" AND eseguito_openvas = "on" AND net_discovery="off" )) AND id_asset = %s; ', id_asset)
    if cur.rowcount != 0:
        result = cur.fetchone()
        print(
            "*************************************************************************************************************************************")
        print("Scansione Defensio Engine in esecuzione: Job n° " + str(result[0]) + " | Assetto n° " + str(
            result[1]) + " | Target " + str(result[2]) + " | Netmask " + str(result[3]))

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Scansione Defensio Engine in esecuzione: Job n° " + str(result[0]) + " | Assetto n° " + str(
                        result[1]) + " ! Target " + str(result[2]) + " | Netmask " + str(result[3]))

        # chiude la connessione per evitare timeout durante la scansione di nmap
        cur.close()
        conn.close()

        # estrae i dati dell interrogazione sul job
        id_j = result[0]
        ip = result[2]
        netmask = result[3]
        ip_net = ip + '/' + netmask
        single_port = str(result[4])
        print(single_port)
        if single_port == 'None':
            single_port = ''

        low_port = result[5]
        high_port = result[6]
        if single_port != '':
            port_target = single_port
        else:
            port_target = str(low_port) + "-" + str(high_port)

        print("Scansione attiva sulle porte: " + port_target)

        argument = "-O -sV -p" + port_target

        print(argument)
        # genera la stringa di inizio del job
        start_job = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Time avvio job: " + str(start_job))
        # variabile None da utilizzare nelle interrogazioni SQL per i campi autoincrementali
        vuoto = None

        # oggetto portscanner

        # try:
        nm = nmap.PortScanner()

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Creazione process nmap.PortScanner()")
        # scansione secondo parametri del job

        nm.scan(hosts=ip_net, arguments=argument)

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Scansione conclusa")

        # crea la connessione per caricare i dati sul DB
        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()

        cur = conn.cursor()

        # ciclo for di estrazione dei dati raccolti dalla scansione
        for host in nm.all_hosts():
            print("** Host trovato: " + host)
            try:
                os_name = nm[host]['osmatch'][0]['name']
                print("OS: " + os_name)
            except:
                os_name = ''

            try:
                os_accuracy = nm[host]['osmatch'][0]['accuracy']
                print(os_accuracy)
            except:
                os_accuracy = ''

            try:
                type = nm[host]['osmatch'][0]['osclass'][0]['type']
                print(type)
            except:
                type = ''

            try:
                vendor = nm[host]['osmatch'][0]['osclass'][0]['vendor']
                print(vendor)
            except:
                vendor = ''

            try:
                osfamily = nm[host]['osmatch'][0]['osclass'][0]['osfamily']
                print(osfamily)
            except:
                osfamily = ''

            try:
                osgen = nm[host]['osmatch'][0]['osclass'][0]['osgen']
                print(osgen)
            except:
                osgen = ''

            # inserimento SQL nella tabella HOST
            cur.execute(
                "INSERT INTO host (id, id_job, start_job, ip, hostname, os_name, os_accuracy, type, vendor, osfamily, osgen) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (id_j, start_job, host, nm[host].hostname(), os_name, os_accuracy, type, vendor, osfamily, osgen))
            conn.commit()
            log = crealog.log_event()
            log.crealog(idprocess,
                        "Caricamento risultati tabella HOST:" + str(host))
            # ciclo for per i protocolli riscontrati
            for proto in nm[host].all_protocols():
                print("  L____ Protocollo attivo: " + proto)
                # creazione di una lista di porte trovate nella scansione
                localport = nm[host][proto].keys()

                # ordine delle porte scoperte
                sorted(localport)

                # ciclo for sulle porte scoperte
                for port in localport:
                    print("      L____ Servizio sulla porta: " + str(port) + " | Tipo servizio: " +
                          nm[host][proto][port]['name'] + " | Stato:" + nm[host][proto][port]['state'])
                    # inserimento SQL nella tabella Port
                    try:
                        cur.execute(
                            "INSERT INTO Port (id_port,id_job,ip,port_n,name,state,reason,product,version,info,start_job) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (vuoto, id_j, host, port, nm[host][proto][port]['name'], nm[host][proto][port]['state'],
                             nm[host][proto][port]['reason'], nm[host][proto][port]['product'],
                             nm[host][proto][port]['version'], nm[host][proto][port]['extrainfo'],start_job))
                        conn.commit()
                        log = crealog.log_event()
                        log.crealog(idprocess,
                                    "Caricamento risultati tabella Port:" + str(host) + " port:" + str(port))
                    except:
                        print("errore nell inserimento dei risultati nella tabella port")
                        log = crealog.log_event()
                        log.crealog(idprocess,
                                    "ERRORE Caricamento risultati tabella Port:" + str(host) + " port:" + str(port))
        # except:
        # print('errore in nmap')

        # whois per ip_pubblici

        try:
            whois_public_ip(id_j)
        except:
            print("WHOIS not possible")
            log = crealog.log_event()
            log.crealog(idprocess,
                        "ERRORE WHOIS su job " + str(id_j) + " non disponibile")

        # aggiorna la statistica del job della tabella statistic_job

        try:
            update_statistic_host(id_j)
        except:
            print('errore nell\'update della tabella statistica')
            log = crealog.log_event()
            log.crealog(idprocess,
                        "ERRORE update tabella statistica su job" + str(id_j) + " non disponibile")

        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()

        # scrive il tag esecuzione sul record del job
        cur = conn.cursor()
        sql_update_query = """UPDATE job SET net_discovery = %s WHERE id_job  = %s"""
        input_data = ('on', id_j)

        cur.execute(sql_update_query, input_data)
        conn.commit()
        log = crealog.log_event()
        log.crealog(idprocess,
                    "Aggiornata tabella JOB " + str(id_j) + " net_discovery --> on")
        cur.close()
        conn.close()

    print(
        """
 +-++-++-+ +-++-++-++-++-++-++-+
 |N||e||t| |S||c||a||n||n||e||r|
 +-++-++-+ +-++-++-++-++-++-++-+
                                                                              
    .........Net_Discovery Active...Waiting for Jobs...  ZZZZZZ...ZZZZZ..ZZZ...\n""")
    time.sleep(20)
    os.system('clear')

    check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn_check = DB_connect.database_connect()
    conn2 = conn_check.database_connection()

    cur2 = conn2.cursor()

    sql_update_query = """UPDATE engines SET last_check_ND = %s WHERE engines.codeword = %s; """
    input_data = (check, id_ass)
    cur2.execute(sql_update_query, input_data)
    conn2.commit()
    cur2.close()
    conn2.close()
