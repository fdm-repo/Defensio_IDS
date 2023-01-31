#!/usr/bin/env python3
# Module Imports
import subprocess
import sys
import time
import random
import string
import DB_connect
import os
import json
import whois

try:
    data = json.load(open("eng_conf.json"))
except:
    print("Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
    sys.exit(1)
id_ass = data['id_ass']

conn_check = DB_connect.database_connect()
conn = conn_check.database_connection()
cur = conn.cursor()


length_of_string = 12

while True:
    stringa = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))
    print("""
  ____            __                        _             _____    ___    _  __  _____   _   _ 
 |  _ \    ___   / _|   ___   _ __    ___  (_)   ___     |_   _|  / _ \  | |/ / | ____| | \ | |
 | | | |  / _ \ | |_   / _ \ | '_ \  / __| | |  / _ \      | |   | | | | | ' /  |  _|   |  \| |
 | |_| | |  __/ |  _| |  __/ | | | | \__ \ | | | (_) |     | |   | |_| | | . \  | |___  | |\  |
 |____/   \___| |_|    \___| |_| |_| |___/ |_|  \___/      |_|    \___/  |_|\_\ |_____| |_| \_|
                                                                                               
    
    """
          )
    print("++++++++++++++++++++++++++++++++")
    print("\nToken generato: "+stringa)
    print("++++++++++++++++++++++++++++++++")
    sql_update_query = """UPDATE engines SET token = %s WHERE engines.codeword = %s; """
    input_data = (stringa, id_ass)
    cur.execute(sql_update_query, input_data)
    conn.commit()
    time.sleep(300)
    os.system('clear')
cur.close()
conn.close()

