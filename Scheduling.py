#!/usr/bin/env python3
# Module Imports
import subprocess
import sys
import os
import time
from datetime import datetime
import arachni
import DB_connect
import enum4linux_read_json
import SMBRUTE
import mariadb
import nmap
import json
import whois
from threading import Thread

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

    cur = conn.cursor()

    cur.execute('SELECT * FROM scheduling JOIN job ON job.id_job = scheduling.id_job WHERE job.id_asset = %s', id_asset)
    if cur.rowcount != 0:
        adesso = datetime.now()
        time_totale = adesso.strftime('%Y-%m-%d %H:%M:%S')

        print("\nOrario attuale: " + time_totale)

        ora_attuale = adesso.strftime('%H:%M')
        print("Ora attuale: " + ora_attuale)

        giorno_settimana = adesso.strftime('%A')
        print("Giorno della settimana: " + giorno_settimana)

        giorno_mese = adesso.strftime('%d')
        print("Giorno del mese: " + giorno_mese)

        risultati = cur.fetchall()
        for job_schedulated in risultati:

            id_job = job_schedulated[1]
            print("\n____________Scheduling in coda per l'assetto " + str(id_ass) + " ______________\n")
            print("id job: " + str(id_job))
            en_day = job_schedulated[4]
            orario = job_schedulated[7]
            print("Abilitata scansione giornaliera: " + en_day + " Orario: " + orario)
            en_weekday = job_schedulated[2]
            weekday = job_schedulated[5]
            print("Abilitata scansione settimanale: " + en_weekday + " Giorno: " + weekday + " Orario: " + orario)
            en_monthday = job_schedulated[3]
            monthday = job_schedulated[6]
            print("Abilitata scansione mensile: " + en_monthday + " Giorno: " + monthday + " Orario: " + orario)

            if (en_day == 'on' and orario == ora_attuale):
                print("***************job giornaliero attivato*****************")
            if (en_weekday == 'on' and orario == ora_attuale and weekday == giorno_settimana):
                print("*****    ***********    job settimanale attivato   *****    ***********")
            if (en_monthday == 'on' and orario == ora_attuale and monthday == giorno_mese):
                print("*****++++++++***********    job mensile attivato   *****+++++++++***********")





    time.sleep(10)
    os.system('clear')
    print("Scheduling Active...Waiting for Jobs...  ZZZZZZ...ZZZZZ..ZZZ...")
    check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(check)
    time.sleep(10)
    os.system('clear')
