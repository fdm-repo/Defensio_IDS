#!/usr/bin/env python3
# Module Imports
import json
import subprocess
import time
from datetime import datetime

import DB_connect

while True:

    conn_IdentityProtection = DB_connect.database_connect()
    conn1 = conn_IdentityProtection.database_connection()

    cur1 = conn1.cursor()

    cur1.execute('SELECT id_job_identity_protection, method, query FROM identity_protection_job  WHERE abilitato="on"')

    if cur1.rowcount != 0:
        result = cur1.fetchone()
        id_job = result[0]
        method = result[1]
        query = result[2]

        """ inserire email, domain, username oppure ip"""

        key_API = 'ad4e472070d19040d58a5aa272723833'

        string_query = 'https://breachdirectory.com/api_usage?method=' + method + '&key=' + key_API + '&query=' + query

        cmd = subprocess.run(["wget", string_query, '-O', 'result_databranch.json'])

        time.sleep(1)

        conn_IdentityProtection = DB_connect.database_connect()
        conn2 = conn_IdentityProtection.database_connection()

        cur2 = conn2.cursor()

        with open('result_databranch.json', 'r') as json_file:
            result = json.load(json_file)
            numero_record = len(result)
            check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for i in range(numero_record):
                print("______________________")
                title = result[i]['title']
                print("titolo: " + title)
                domain = result[i]['domain']
                print("dominio: " + domain)
                email = result[i]['email']
                print("email: " + email)
                username = result[i]['username']
                print("username: " + username)
                ip = result[i]['ip']
                print("IP: " + ip)
                try:
                    sql_update_query = """INSERT INTO `identity_protection` (`id_result_identity_protection`, `id_job_identity_protection`, `time`, `titolo`, `dominio`, `email`, `username`, `ip`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s); """
                    input_data = (id_job, check, title, domain, email, username, ip)
                    cur2.execute(sql_update_query, input_data)
                    conn2.commit()
                except:
                    print("error to load result in the identity protection tabel")


        sql_update_query = """UPDATE identity_protection_job  SET abilitato = %s WHERE id_job_identity_protection = %s; """
        input_data = ('off', id_job)
        cur2.execute(sql_update_query, input_data)
        conn2.commit()
        cur2.close()
        conn2.close()

    cur1.close()
    conn1.close()



    time.sleep(5)
    print("Databranch engine Active...Waiting for Jobs...  ZZZZZZ...ZZZZZ..ZZZ...")
    check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(check)