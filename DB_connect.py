#!/usr/bin/env python3
# Module Imports
import sys
import os
import time

import mariadb


class database_connect:

    def database_connection(self, utente, password, ip_db, port_server, db):

        for i in range(4):
            try:
                conn = mariadb.connect(
                    user=utente,
                    password=password,
                    host=ip_db,
                    database=db,
                    port=port_server
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
