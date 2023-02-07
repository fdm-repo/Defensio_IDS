#!/usr/bin/env python3

# dependency check for the modules

import os
import time
import DB_connect
import sys
import json
import subprocess





while True:

    print("************** SENTINEL DAEMON  ****************")

    try:
        data = json.load(open("eng_conf.json"))
    except:
        print("!!! Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
        sys.exit(1)

    id_ass = data['id_ass']


    C2 = os.popen("pgrep -fx \"python3 ./C2.py\"").read()

    if C2 == '':

        net_scanner_token = "ERR_C2_OFF"
        web_scanner_token = "ERR_C2_OFF"
        vuln_scanner_token = "ERR_C2_OFF"
        share_scanner_token = "ERR_C2_OFF"
        print("Processo C2 Defensio DISATTIVATO")

        c2_connect = DB_connect.database_connect()
        c2_conn = c2_connect.database_connection()

        c2_cur = c2_conn.cursor()

        sql_update_query = """UPDATE engines SET active_defensio = %s, active_webscanner = %s,active_openvas = %s,active_share_scanner=%s WHERE engines.codeword = %s; """
        input_data = (net_scanner_token, web_scanner_token, vuln_scanner_token, share_scanner_token, id_ass)
        c2_cur.execute(sql_update_query, input_data)
        c2_conn.commit()
        c2_conn.close()

    else:
        print("Processo C2 Defensio ATTIVO")


    time.sleep(5)
    os.system('clear')
