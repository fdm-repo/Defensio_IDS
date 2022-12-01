#!/usr/bin/env python3

import re
import DB_connect


class parsing_sqlmap():
    def parsing_sqlmap_report(self,id_job):

        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()

        patrn = "isDir"

        file_one = open("report_brute.txt", "r")

        for word in file_one:
            if re.search(patrn, word):
                # print(word)
                word2 = word.split(',')
                for x in word2:
                    # print(x)
                    x = x.split(':')

                    if x[0].replace(" ", "") == "host":
                        host = x[1]
                    if x[0].replace(" ", "") == "name":
                        nome_condivisione = x[1]

                    if x[0].replace(" ", "") == "isDir":
                        directory = x[1]
                    if x[0].replace(" ", "") == "privs":
                        diritti = x[1]
                    if x[0].replace(" ", "") == "fileSize":
                        dimensionefile = x[1]

                print(host+" | "+nome_condivisione + " | " + directory + " | " + diritti + " | " + dimensionefile)



