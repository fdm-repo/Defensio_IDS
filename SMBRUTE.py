#!/usr/bin/env python3

import os
import sys
import crealog
import DB_connect
import extrac_dir_file_bruteforce


idprocess = "SMBRUTE"

class smbbruteforce:
    def bruteforce(self, id_j, ip, username, password):

        id_job = id_j
        target = ip

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Esecuzione del job "+str(id_job)+" sull'host "+str(target))


        found = []
        try:
            users = open(username, 'r')
            users = users.read().split("\n")
            users.pop()
        except:
            print("[!]  Unable to open File ==> {}".format(username))

            log = crealog.log_event()
            log.crealog(idprocess,
                        "ERRORE impossibile trovare il file username")

            sys.exit()

        try:
            passwd = open(password, 'r')
            passwd = passwd.read().split("\n")
            passwd.pop()
        except:
            print("[!]  Unable to open File ==> {}".format(password))

            log = crealog.log_event()
            log.crealog(idprocess,
                        "ERRORE impossibile trovare il file pasword")

            sys.exit()
        os.system("mkdir DUMP")

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Creazione cartella temporanea DUMP")

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Testing della connessione a SMB tramite tramite coppia di credenziali presenti nei dizionari username e password")

        for u in users:
            p = ' '
            try:



                if os.system("smbclient -L {} -U {}%{}".format(ip, u, p)) == 256:
                    for p in passwd:
                        try:
                            print("test " + u + " on password " + p)
                            if os.system("smbclient -L {} -U {}%{}".format(ip, u, p)) != 256:
                                found.append("{}:{}".format(u, p))
                        except:
                            print("error on utente:{} and pass: {} ".format(u, p))
            except:
                print("error on utente:{} and pass: {} ".format(u, p))

        os.system("clear")
        os.system("rm -rf DUMP")

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Rimozione cartella temporanea DUMP")


        print("user: " + str(found))
        if found == []:
            print("[*] NO MATCH FOUND ! ")

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Nessun user trovato")

        else:
            print("[!!]MATCH FOUND ! GETTING SHARES ....\n")
            print("+----------------------------------------------------------------------+")

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Trovate corrispondenze USER PASS")


            log = crealog.log_event()
            log.crealog(idprocess,
                        "Avvio SMBMap sulle corrispondenze trovate")

            for x in found:
                u = x.split(":")[0]
                p = x.split(":")[1]
                print("[*] SHARES FOR USER : \033[30;42m {} \033[m  AND PASSWORD : \033[30;42m {} \033[m".format(u, p))
                os.system(
                    "./smbmap/smbmap.py  --no-banner --no-update --no-color  -u {} -p {} -H {} -r --csv report_brute_smb.csv".format(
                        u, p, ip, ))
                print("+----------------------------------------------------------------------+")

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Avvio SMBMap con user "+str(u)+" e password "+str(p)+" sull'host "+str(ip))

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Connessione al DB")
                connessione_brute = DB_connect.database_connect()
                conn_brute = connessione_brute.database_connection()

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Connessione al DB riuscita")

                cur_brute = conn_brute.cursor()

                sql_update_query = """INSERT INTO`smb_bruteforce`(`id_bruteforce`, `id_job`, `ip_host` ,`user`, `password`) VALUES (NULL,%s,%s,%s,%s);"""
                input_data = (id_job, target, u, p)

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Inserimento nella tabella smb_buteforce del record relativo al job "+str(id_job)+" relativo all'host "+str(target)+" con user "+str(u)+" e password "+str(p))

                cur_brute.execute(sql_update_query, input_data)
                conn_brute.commit()
                conn_brute.close()

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Chiusura della connessione al DB")

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Chiamata alla classe e alle funzioni del file EXTRACT_DIR_FILE_BRUTEFORCE")

                parsing_sqlmap = extrac_dir_file_bruteforce.parsing_sqlmap()

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Esecuzione della funzione parsing_sqlmap_report(id_j, u, p) ")

                parsing_sqlmap.parsing_sqlmap_report(id_j, u, p)

        print("\n")
