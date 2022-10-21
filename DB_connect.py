#!/usr/bin/env python3
# Module Imports
import sys
import os
import mariadb


class database_connect:

    def database_connection(self, utente, password, ip_db, port_server, db):

        try:
            conn = mariadb.connect(
                user=utente,
                password=password,
                host=ip_db,
                database=db,
                port=port_server
            )
            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            file_pwd = './eng_conf.json'
            os.remove(file_pwd)
            print("Rimosso file di accesso, eseguire inizializzazione dell assetto. (./Inizializzazione_engine.py)")
            sys.exit(1)
