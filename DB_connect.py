#!/usr/bin/env python3
# Module Imports
import json
import os
import sys
import time

import mariadb


class database_connect:

    def database_connection(self):

        try:
            data = json.load(open("eng_conf.json"))
        except:
            print("Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
            sys.exit(1)


        for i in range(4):
            try:
                conn = mariadb.connect(
                    user=data['user_db'],
                    password=data['password_db'],
                    host=data['host_db'],
                    database=data['database'],
                    port=int(data['port_db'])
                )
                return conn
                break
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                if i < 3:
                    print("tentivo n° "+ str(i) + " di connessione al server.... ")

                    time.sleep(30)
                    continue
                else:
                    file_pwd = './eng_conf.json'
                    os.remove(file_pwd)
                    print("!!!!! Connessione non riuscita per 5 tentativi...")
                    print("Rimosso file di accesso, eseguire inizializzazione dell assetto. (./Inizializzazione_engine.py)")
                    sys.exit(1)
