#!/usr/bin/env python3
# Module Imports
import subprocess
import sys
import time
import random
import string
import DB_connect

import json
import whois

try:
    data = json.load(open("eng_conf.json"))
except:
    print("Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
    sys.exit(1)


conn_check = DB_connect.database_connect()
conn = conn_check.database_connection(data['user_db'], data['password_db'], data['host_db'],
                                           int(data['port_db']), data['database'])

cur = conn.cursor()


length_of_string = 12
id_ass = "144"

while True:
    stringa = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    print(stringa)
    sql_update_query = """UPDATE engines SET token = %s WHERE engines.codeword = %s; """
    input_data = (stringa, id_ass)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    time.sleep(60)
cur.close()
conn.close()

