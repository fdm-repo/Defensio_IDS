#!/usr/bin/env python3
# Module Imports
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from threading import Thread

import DB_connect
import SMBRUTE
import enum4linux_read_json

token_ver = ''
def test():

    global token_ver
    while True:
        try:
            data = json.load(open("eng_conf.json"))
        except:
            print("Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
            sys.exit(1)
        id_ass = data['id_ass']

        conn_check = DB_connect.database_connect()
        conn = conn_check.database_connection()
        cur = conn.cursor()


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
                sql_update_query = """UPDATE engines SET active_defensio = %s WHERE engines.codeword = %s; """
                input_data = (token, id_ass)
                cur.execute(sql_update_query, input_data)
                conn.commit()
                token_ver = token
            except:
                print("Verifica token non effettuata")

        print("++++++++++++++++++++++++++++++++++++")
        print("DataTime: " + str(datetime.now()))
        print("Token attuale verificato: " + token)
        print("++++++++++++++++++++++++++++++++++++")
        time.sleep(11)

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

    id_j = ''
    # estrazione parametri del job selezionato

    cur = conn.cursor()

    # esegue la scansione con enum4linux

    eseguito_enum4linux = ''

    # try:
    connessione = DB_connect.database_connect()
    conn = connessione.database_connection()

    enum4linuxqueryjob = conn.cursor()
    enum4linuxqueryjob.execute(
        "SELECT Port.id_job, Port.ip, port_n FROM `Port` INNER JOIN job ON job.id_job = Port.id_job WHERE Port.name = 'netbios-ssn' AND job.enumforlinux = 'on' AND job.net_discovery='on' AND job.eseguito_enum4linux='off' ;")

    if enum4linuxqueryjob.rowcount != 0:

        # genera la stringa di inizio del job
        start_job = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Time avvio job: " + str(start_job))


        result_enum_job = enum4linuxqueryjob.fetchone()
        print(result_enum_job)
        id_j = result_enum_job[0]
        ip_target = result_enum_job[1]

        file_name = str(id_j) + '_' + ip_target
        print(file_name)
        cmd = subprocess.run(["./enumforlinux/enum4linux-ng.py", "-A", ip_target, "-oJ", file_name])

        obj_enum4linux_json = enum4linux_read_json.enum4linux_read_json_class()
        obj_enum4linux_json.enum4linux_read_json(id_j, start_job, file_name + '.json')
        eseguito_enum4linux = 'on'
        try:
            os.remove(file_name + ".json")
        except:
            print("not remove Buffer")

        fileusers = "userlarge.txt"
        filepass = "passsmall.txt"

        bruteforce = SMBRUTE.smbbruteforce()
        bruteforce.bruteforce(id_j, ip_target, fileusers, filepass)

        if eseguito_enum4linux == 'on':

            enum4 = conn.cursor()

            sql_update_query = """UPDATE job SET eseguito_enum4linux = %s WHERE id_job  = %s"""
            input_data = ('on', id_j)
            enum4.execute(sql_update_query, input_data)

            conn.commit()
            enum4.close()


    enum4linuxqueryjob.close()
    conn.close()

    # except:
    # print('errore in enum4linux')

    print(
        """
  ____    _                      _                     ____    _                                                    
 / ___|  | |__     __ _   _ __  (_)  _ __     __ _    |  _ \  (_)  ___    ___    ___   __   __   ___   _ __   _   _ 
 \___ \  | '_ \   / _` | | '__| | | | '_ \   / _` |   | | | | | | / __|  / __|  / _ \  \ \ / /  / _ \ | '__| | | | |
  ___) | | | | | | (_| | | |    | | | | | | | (_| |   | |_| | | | \__ \ | (__  | (_) |  \ V /  |  __/ | |    | |_| |
 |____/  |_| |_|  \__,_| |_|    |_| |_| |_|  \__, |   |____/  |_| |___/  \___|  \___/    \_/    \___| |_|     \__, |
                                             |___/                                                            |___/ 

    .........Sharing_Discovery Active...Waiting for Jobs...  ZZZZZZ...ZZZZZ..ZZZ...\n""")
    time.sleep(20)
    os.system('clear')

    check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn_check = DB_connect.database_connect()
    conn2 = conn_check.database_connection()

    cur2 = conn2.cursor()

    sql_update_query = """UPDATE engines SET last_check_SS = %s WHERE engines.codeword = %s; """
    input_data = (check, id_ass)
    cur2.execute(sql_update_query, input_data)
    conn2.commit()
    cur2.close()
    conn2.close()

