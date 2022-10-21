#!/usr/bin/env python3
import json


print("********************* Setup di inizializzazione dell'engine *********************")
print("++Connessione DATABASE\n")
user_db = input("Inserire Username: ")
password_db = input("Inserire Password: ")
host_db = input("Inserire IP del server DB: ")
port_db = input("Inserire la porta TCP: ")
database = input("Inserire il nome del database: ")


print("\n++Identificativo dell'Engine")

id_ass = input("inserisci il numero di assetto:")


config_data = {'user_db': user_db, 'password_db': password_db, 'host_db': host_db, 'port_db': port_db, 'database': database, 'id_ass': id_ass}

with open("eng_conf.json", "w") as outfile:
    json.dump(config_data, outfile)
