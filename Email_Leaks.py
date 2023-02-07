#!/usr/bin/env python3

import datetime
import json
import os
import subprocess
import time
import crealog

import DB_connect

idprocess = "Email_Leaks"

while True:
    connessione = DB_connect.database_connect()
    conn = connessione.database_connection()
    log = crealog.log_event()
    log.crealog(idprocess,
                "Connessione al Database")
    cur = conn.cursor()

    cur.execute("SELECT email FROM email_leak_target")
    result = cur.fetchall()

    log = crealog.log_event()
    log.crealog(idprocess,
                "Ricerca Email da verificare")

    if cur.rowcount != 0:
        print(
            """
 +-++-++-++-++-++-++-++-+ +-++-++-+
 |V||e||r||i||f||i||c||a| |D||P||I|
 +-++-++-++-++-++-++-++-+ +-++-++-+
                                                                                                           
by DEFENSIO Scanner        
            """
        )
        for i in result:
            email = i[0]

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Email in esame: "+ str(email))

            print("Email in esame: " + email)
            f = open(email, "a")
            try:
                cmd = subprocess.run(["pwned", "pa", email, "-r"], stdout=f)

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Processo di ricerca concluso, creato file risultato email")

            except:
                print("Errore.. prossimo tentativo....")

                log = crealog.log_event()
                log.crealog(idprocess,
                            "ERRORE Processo di ricerca non eseguito")

            f.close()

            email_list = list()
            email_list.append(email)
            sql_del = "DELETE FROM email_leak_result WHERE email = %s"
            cur.execute(sql_del, email_list)
            conn.commit()

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Record pregressi dell Email in esame cancellati")

            with open(email, 'r') as handle:

                json_data = [json.loads(line) for line in handle]
                lenght_file = len(json_data)



                for riga in range(lenght_file):
                    log = crealog.log_event()
                    log.crealog(idprocess,
                                "N° " + str(len(json_data[riga])) + " Risultati trovati")
                    for x in range(len(json_data[riga])):
                        print("****************************************************************")
                        Id = str(json_data[riga][x]["Id"])
                        print("Id: " + Id)
                        Source = str(json_data[riga][x]["Source"])
                        print("Source: " + Source)
                        Title = str(json_data[riga][x]["Title"])
                        print("Title: " + Title)
                        Date = str(json_data[riga][x]["Date"])
                        print("Date: " + Date)
                        EmailCount = str(json_data[riga][x]["EmailCount"])
                        print("EmailCount: " + EmailCount)

                        sql_ins = "INSERT INTO `email_leak_result` (`Id_leak_result`, `email`, `Id_leak_HBP`, `source`, `title`, `date`, `emailcount`) VALUES (NULL,%s,%s,%s,%s,%s,%s);"
                        data_input = (email, Id, Source, Title, Date, EmailCount)
                        cur.execute(sql_ins, data_input)
                        conn.commit()

                        log = crealog.log_event()
                        log.crealog(idprocess,
                                    "Inserito Risultato per email: "+str(email)+" ID: "+Id)

            os.remove(email)
            log = crealog.log_event()
            log.crealog(idprocess,
                        "Rimosso file risultato email")
            print("******************************************")
            print("Verifica Email ATTIVO... ZZZzzz...zzzz...")
            print("*^^^^^^****_____****^^^$$$****************")
            time.sleep(10)
    os.system('clear')
    print(
        """
 +-++-++-++-++-++-++-++-+ +-++-++-+
 |V||e||r||i||f||i||c||a| |D||P||I|
 +-++-++-++-++-++-++-++-+ +-++-++-+
                                                             


    .........DPI Check...Waiting for Jobs...  ZZZZZZ...ZZZZZ..ZZZ...\n""")
    print("Orario ultima esecuzione: " + str(datetime.datetime.now()))
    print("PROSSIMA ESECUZIONE.... TRA 24 ORE...")
    time.sleep(86400)
    os.system('clear')
