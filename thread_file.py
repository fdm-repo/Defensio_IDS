#!/usr/bin/env python3
# Module Imports
import datetime
import json
import sys
import time
from threading import Thread

import DB_connect

try:
    data = json.load(open("eng_conf.json"))
except:
    print("Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
    sys.exit(1)

token_ver = ''


def test():
    global token_ver
    while True:
        conn_check = DB_connect.database_connect()
        conn = conn_check.database_connection(data['user_db'], data['password_db'], data['host_db'],
                                              int(data['port_db']), data['database'])
        cur = conn.cursor()

        id_ass = "144"
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
                print("verifica token non effettuata")

        print(datetime.datetime.now())
        print("\ntoken attuale verificato: " + token)
        time.sleep(10)


t = Thread(target=test)
t.start()
