#!/usr/bin/env python3
# Module Imports
import subprocess
import sys
import os
import time
from datetime import datetime
import arachni
import DB_connect
import enum4linux_read_json
import SMBRUTE
import extrac_dir_file_bruteforce
import mariadb
import nmap
import json
import whois
from threading import Thread

# setup di configurazione all avvio dell'engine


token_ver = ''
def test():

    global token_ver
    while True:
        conn_check = DB_connect.database_connect()
        conn = conn_check.database_connection()
        cur = conn.cursor()
        try:
            data = json.load(open("eng_conf.json"))
        except:
            print("Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
            sys.exit(1)
        id_ass = data['id_ass']
        id_asset = list()
        id_asset.append(id_ass)

        try:
            sql_query_token = """SELECT token FROM engines WHERE engines.codeword = %s; """
            input_data = id_asset
            cur.execute(sql_query_token, input_data)

            token = cur.fetchone()
            token = token[0]

        except:
            print("nessun token rilevato")

        if token_ver != token:
            try:
                sql_update_query = """UPDATE engines SET active_webscanner = %s WHERE engines.codeword = %s; """
                input_data = (token, id_ass)
                cur.execute(sql_update_query, input_data)
                conn.commit()
                token_ver = token
            except:
                print("verifica token non effettuata")

        print(datetime.now())
        print("\ntoken attuale verificato: "+token)
        time.sleep(10)

t = Thread(target=test)
t.start()

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
            obj = arachni.arachni_class()
            obj.arachni_http(id_j, ip_target, port_target)

            connessione = DB_connect.database_connect()
            conn = connessione.database_connection()
            arac = conn.cursor()
            arachni_sql_report = "INSERT INTO arachni_report (id_arac_report, id_job) VALUES (NULL, %s);"
            bho = list()
            bho.append(id_j)
            arac.execute(arachni_sql_report, bho)
            arac.close()
            conn.close()
            eseguito_arachni = 'on'



    except:
        print('errore in arachni su servizio http')

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

            obj = arachni.arachni_class()
            obj.arachni_https(id_j, ip_target, port_target)

            connessione = DB_connect.database_connect()
            conn = connessione.database_connection()
            arac = conn.cursor()
            arachni_sql_report = "INSERT INTO arachni_report (id_arac_report, id_job) VALUES (NULL, %s);"
            bho = list()
            bho.append(id_j)
            arac.execute(arachni_sql_report, bho)
            conn.commit()
            arac.close()
            conn.close()
            eseguito_arachni = 'on'




    except:
        print('errore in arachni su servizio https')

    # ciclo if che si esegue solo se c'è stata una scansione con arachni e modifica i valori nel record del job

    if eseguito_arachni == 'on':
        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()
        arac = conn.cursor()
        sql_update_query = """UPDATE job SET arachni = %s WHERE id_job  = %s"""
        input_data = ('off', result[0])
        arac.execute(sql_update_query, input_data)

        conn.commit()

        sql_update_query = """UPDATE job SET eseguito_arachni = %s WHERE id_job  = %s"""
        input_data = ('on', result[0])
        arac.execute(sql_update_query, input_data)

        conn.commit()
        arac.close()





    time.sleep(5)
    print("Web Scanner Active...Waiting for Jobs...  ZZZZZZ...ZZZZZ..ZZZ...")
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
