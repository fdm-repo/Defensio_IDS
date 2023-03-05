#!/usr/bin/env python3

import csv
import crealog
import DB_connect

idprocess = "extrac_dir_file_bruteforce"
class parsing_sqlmap():
    def parsing_sqlmap_report(self, id_job, user, password, start_time):
        id_job = id_job
        user = user
        password = password
        start_scan =start_time


        log = crealog.log_event()
        log.crealog(idprocess,
                    "Estrazione risultati bruteforce sqlmap del Job: "+str(id_job)+" User: "+str(user)+" Pass: "+password)


        with open('report_brute_smb.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Aperture File report bruteforce")


            for row in spamreader:
                print("____________________________")
                ip_target = row[0]

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Estrazione dei risultati per l'IP: "+str(ip_target))

                print("Target: " + ip_target)
                print("User: " + user)
                print("Password: " + password)
                nome_condivisione = row[1]
                print("Nome condivisione: " + nome_condivisione)
                diritti = row[2]
                print("Diritti lettura/scrittura: " + diritti)
                dir_file = row[3]
                print("Directory/File: " + dir_file)
                percorso = row[4]
                print("Percorso della condivisione: " + percorso)
                dimensione = row[5]
                print("Dimensione del File: " + dimensione)

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Tentativo di connessione al DB")

                connessione_brute_sharing = DB_connect.database_connect()
                conn_brute_sharing = connessione_brute_sharing.database_connection()

                cur_brute_sharing = conn_brute_sharing.cursor()

                log = crealog.log_event()
                log.crealog(idprocess,
                            "Connessione al DB accettata")

                sql_update_query = """INSERT INTO `smb_sharing_bruteforce`(`id_share_bruteforce`, `id_job`, `ip_host`, `username`, `password`,`nome_condivisione`, `diritti`, `file_dir`, `percorso`, `dimensione_file`, `start_scan`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                input_data = (
                id_job, ip_target, user, password, nome_condivisione, diritti, dir_file, percorso, dimensione,start_scan)

                cur_brute_sharing.execute(sql_update_query, input_data)
                conn_brute_sharing.commit()
                log = crealog.log_event()
                log.crealog(idprocess,
                            "Inserimento risultati nella tabella smb_sharing_bruteforce")


                conn_brute_sharing.close()
                log = crealog.log_event()
                log.crealog(idprocess,
                            "Chiusura della connessione al DB")
