#!/usr/bin/env python3

import datetime
import subprocess
import DB_connect
import json
import os
import time







while True:
    connessione = DB_connect.database_connect()
    conn = connessione.database_connection()

    cur = conn.cursor()

    cur.execute("SELECT email FROM email_leak_target")
    result = cur.fetchall()
    if cur.rowcount != 0:
        for i in result:
            email = i[0]
            print("Email in esame: "+email)
            f = open(email, "a")
            try:
                cmd = subprocess.run(["pwned", "pa", email, "-r"], stdout=f)
            except:
                print("errore.. prossimo tentativo....")
            f.close()

            email_list = list()
            email_list.append(email)
            sql_del = "DELETE FROM email_leak_result WHERE email = %s"
            cur.execute(sql_del, email_list)
            conn.commit()

            with open(email, 'r') as handle:

                json_data = [json.loads(line) for line in handle]
                lenght_file = len(json_data)
                for riga in range(lenght_file):
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

            os.remove(email)
            print("******************************************")
            print("Verifica Email ATTIVO... ZZZzzz...zzzz...")
            print("*^^^^^^****_____****^^^$$$****************")
            time.sleep(10)
    os.system('clear')
    print("Orario ultima esecuzione: "+str(datetime.datetime.now()))
    print("PROSSIMA ESECUZIONE.... TRA 24 ORE...")
    time.sleep(86400)












