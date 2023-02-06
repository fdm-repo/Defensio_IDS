#!/usr/bin/env python3
# Module Imports
import json
import os
import sys
import time
from datetime import datetime
from threading import Thread
import crealog
import DB_connect
import arachni

# setup di configurazione all avvio dell'engine

idprocess = "WebScanner_engine"


while True:

    connessione = DB_connect.database_connect()
    conn = connessione.database_connection()

    try:
        data = json.load(open("eng_conf.json"))
    except:
        print("Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
        sys.exit(1)

    id_ass = data['id_ass']
    id_asset = list()
    id_asset.append(id_ass)

    # esegue la scansione con arachni

    eseguito_arachni = ''

    try:
        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()
        arac = conn.cursor()
        arac.execute(
            "SELECT Port.id_job, Port.ip,port_n FROM `Port` INNER JOIN job ON job.id_job=Port.id_job WHERE (Port.name='http' OR Port.port_n = '80') AND job.arachni='on'AND job.net_discovery='on';")
        if arac.rowcount != 0:
            result = arac.fetchone()
            print(result)
            id_j = result[0]
            ip_target = result[1]
            port_target = result[2]
            arac.close()
            conn.close()

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Esecuzione del job " + str(id_j) + " sull'host " + str(ip_target)+" e sulla porta "+str(port_target))

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Chiamata alla classe e alle funzioni del file ARACHNI")

            obj = arachni.arachni_class()

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Esecuzione della funzione arachni_http(id_j, ip_target, port_target ")

            obj.arachni_http(id_j, ip_target, port_target)

            connessione = DB_connect.database_connect()
            conn = connessione.database_connection()
            arac = conn.cursor()
            arachni_sql_report = "INSERT INTO arachni_report (id_arac_report, id_job) VALUES (NULL, %s);"


            bho = list()
            bho.append(id_j)
            arac.execute(arachni_sql_report, bho)

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Inserimento ID_Report nella tabella arachni_report del DB relativo al job " + str(
                            id_j) + " sull'host " + str(ip_target) + " e sulla porta " + str(port_target))

            arac.close()
            conn.close()
            eseguito_arachni = 'on'





    except:
        print('errore in arachni su servizio http')

        log = crealog.log_event()
        log.crealog(idprocess,
                    "ERRORE nella scansione con arachni del servizio HTTP ")

    try:
        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()
        arac = conn.cursor()
        arac.execute(
            "SELECT Port.id_job, Port.ip,port_n FROM `Port` INNER JOIN job ON job.id_job=Port.id_job WHERE (Port.name='https' OR Port.port_n = '443') AND job.arachni='on' AND job.net_discovery='on';")
        if arac.rowcount != 0:
            result = arac.fetchone()
            print(result)
            id_j = result[0]
            ip_target = result[1]
            port_target = result[2]
            arac.close()
            conn.close()

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Esecuzione del job " + str(id_j) + " sull'host " + str(ip_target)+" e sulla porta "+str(port_target))

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Chiamata alla classe e alle funzioni del file ARACHNI")

            obj = arachni.arachni_class()

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Esecuzione della funzione arachni_http(id_j, ip_target, port_target ")

            obj.arachni_https(id_j, ip_target, port_target)

            connessione = DB_connect.database_connect()
            conn = connessione.database_connection()
            arac = conn.cursor()
            arachni_sql_report = "INSERT INTO arachni_report (id_arac_report, id_job) VALUES (NULL, %s);"
            bho = list()
            bho.append(id_j)
            arac.execute(arachni_sql_report, bho)
            conn.commit()

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Inserimento ID_Report nella tabella arachni_report del DB relativo al job " + str(
                            id_j) + " sull'host " + str(ip_target) + " e sulla porta " + str(port_target))

            arac.close()
            conn.close()
            eseguito_arachni = 'on'




    except:
        print('errore in arachni su servizio https')

        log = crealog.log_event()
        log.crealog(idprocess,
                    "ERRORE nella scansione con arachni del servizio HTTPS ")

    # ciclo if che si esegue solo se c'è stata una scansione con arachni e modifica i valori nel record del job

    if eseguito_arachni == 'on':
        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()
        arac = conn.cursor()
        sql_update_query = """UPDATE job SET arachni = %s WHERE id_job  = %s"""
        input_data = ('off', result[0])
        arac.execute(sql_update_query, input_data)

        conn.commit()

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Aggiornamento su OFF del campo arachni della tabella job del DB  ")

        sql_update_query = """UPDATE job SET eseguito_arachni = %s WHERE id_job  = %s"""
        input_data = ('on', result[0])
        arac.execute(sql_update_query, input_data)

        conn.commit()

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Aggiornamento su ON del campo eseguito_arachni della tabella job del DB  ")

        arac.close()

    print(
        """
 __        __  _____   ____      ____                                               
 \ \      / / | ____| | __ )    / ___|    ___    __ _   _ __    _ __     ___   _ __ 
  \ \ /\ / /  |  _|   |  _ \    \___ \   / __|  / _` | | '_ \  | '_ \   / _ \ | '__|
   \ V  V /   | |___  | |_) |    ___) | | (__  | (_| | | | | | | | | | |  __/ | |   
    \_/\_/    |_____| |____/    |____/   \___|  \__,_| |_| |_| |_| |_|  \___| |_|   
                                                                                    

    .........Web Scanner Active...Waiting for Jobs...  ZZZZZZ...ZZZZZ..ZZZ...\n""")
    time.sleep(20)
    os.system('clear')

    check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn_check = DB_connect.database_connect()
    conn2 = conn_check.database_connection()

    cur2 = conn2.cursor()

    sql_update_query = """UPDATE engines SET last_check_WS = %s WHERE engines.codeword = %s; """
    input_data = (check, id_ass)
    cur2.execute(sql_update_query, input_data)
    conn2.commit()
    cur2.close()
    conn2.close()
