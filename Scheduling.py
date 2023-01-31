#!/usr/bin/env python3
# Module Imports
import json
import os
import sys
import time
from datetime import datetime

import DB_connect

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
        print("""
  ____           _                  _           _   _                 
 / ___|    ___  | |__     ___    __| |  _   _  | | (_)  _ __     __ _ 
 \___ \   / __| | '_ \   / _ \  / _` | | | | | | | | | | '_ \   / _` |
  ___) | | (__  | | | | |  __/ | (_| | | |_| | | | | | | | | | | (_| |
 |____/   \___| |_| |_|  \___|  \__,_|  \__,_| |_| |_| |_| |_|  \__, |
                                                                |___/ 
by DEFENSIO Scanner

        """)
        adesso = datetime.now()
        time_totale = adesso.strftime('%Y-%m-%d %H:%M:%S')
        print("#############################################")
        print("\nOrario attuale: " + time_totale)

        ora_attuale = adesso.strftime('%H:%M')
        print("Ora attuale: " + ora_attuale)

        giorno_settimana = adesso.strftime('%A')
        print("Giorno della settimana: " + giorno_settimana)

        giorno_mese = adesso.strftime('%d')
        print("Giorno del mese: " + giorno_mese)
        print("#############################################")
        risultati = cur.fetchall()
        for job_schedulated in risultati:

            id_job = job_schedulated[1]

            print("\nId job: " + str(id_job))
            en_day = job_schedulated[4]
            orario = job_schedulated[7]
            if en_day == 'on':
                print("* Abilitata scansione giornaliera  Orario: " + orario)
            en_weekday = job_schedulated[2]
            weekday = job_schedulated[5]
            if en_weekday == 'on':
                print("* Abilitata scansione settimanale  Giorno: " + weekday + " Orario: " + orario)
            en_monthday = job_schedulated[3]
            monthday = job_schedulated[6]
            if en_monthday == 'on':
                print("* Abilitata scansione mensile  Giorno: " + monthday + " Orario: " + orario)

            id_job_list = list()
            id_job_list.append(id_job)

            if (en_day == 'on' and orario == ora_attuale):
                print("***************job "+ str(id_job) +" giornaliero attivato*****************")

                connessione2 = DB_connect.database_connect()
                conn2 = connessione2.database_connection()


                cur2 = conn2.cursor()

                sql_delete_query = "DELETE FROM host WHERE id_job = %s"
                cur2.execute(sql_delete_query, id_job_list)
                conn2.commit()
                print(cur2.rowcount, "host record(s) deleted")

                sql_delete2_query = "DELETE FROM Port WHERE id_job = %s"
                cur2.execute(sql_delete2_query, id_job_list)
                conn2.commit()
                print(cur2.rowcount, "service record(s) deleted")


                print("*->record assets pregressi eliminati")

                # scrive il tag esecuzione sul record del job

                sql_update_query = """UPDATE job SET net_discovery = %s WHERE id_job  = %s"""
                input_data = ('off', id_job)
                cur2.execute(sql_update_query, input_data)
                conn2.commit()
                cur2.close()
                conn2.close()
                avvio_job_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("----> Job "+str(id_job)+" avviato alle: "+avvio_job_time)
                time.sleep(60)



            if (en_weekday == 'on' and orario == ora_attuale and weekday == giorno_settimana):
                print("*****     ***********    job "+ str(id_job) +" settimanale attivato   *****    ***********")

                connessione2 = DB_connect.database_connect()
                conn2 = connessione2.database_connection()

                # scrive il tag esecuzione sul record del job
                cur2 = conn2.cursor()

                sql_delete_query = "DELETE FROM host WHERE id_job = %s"
                cur2.execute(sql_delete_query, id_job_list)
                conn2.commit()
                print(cur2.rowcount, "host record(s) deleted")

                sql_delete2_query = "DELETE FROM Port WHERE id_job = %s"
                cur2.execute(sql_delete2_query, id_job_list)
                conn2.commit()
                print(cur2.rowcount, "service record(s) deleted")

                print("*->record assets pregressi eliminati")

                sql_update_query = """UPDATE job SET net_discovery = %s WHERE id_job  = %s"""
                input_data = ('off', id_job)
                cur2.execute(sql_update_query, input_data)
                conn2.commit()
                cur2.close()
                conn2.close()
                avvio_job_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("----> Job " + str(id_job) + " avviato alle: " + avvio_job_time)
                time.sleep(60)

            if (en_monthday == 'on' and orario == ora_attuale and monthday == giorno_mese):
                print("*****++++++++***********    job "+ str(id_job) +" mensile attivato   *****+++++++++***********")

                connessione2 = DB_connect.database_connect()
                conn2 = connessione2.database_connection()

                # scrive il tag esecuzione sul record del job
                cur2 = conn2.cursor()

                sql_delete_query = "DELETE FROM host WHERE id_job = %s"
                cur2.execute(sql_delete_query, id_job_list)
                conn2.commit()
                print(cur2.rowcount, "host record(s) deleted")

                sql_delete2_query = "DELETE FROM Port WHERE id_job = %s"
                cur2.execute(sql_delete2_query, id_job_list)
                conn2.commit()
                print(cur2.rowcount, "service record(s) deleted")

                print("*->record assets pregressi eliminati")

                sql_update_query = """UPDATE job SET net_discovery = %s WHERE id_job  = %s"""
                input_data = ('off', id_job)
                cur2.execute(sql_update_query, input_data)
                conn2.commit()
                cur2.close()
                conn2.close()
                avvio_job_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("----> Job " + str(id_job) + " avviato alle: " + avvio_job_time)
                time.sleep(60)






    time.sleep(10)
    os.system('clear')

