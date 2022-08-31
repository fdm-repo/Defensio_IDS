#!/bin/python3

# dependency check for the modules

try:
    import os
    import subprocess
    import sys
    import re
    import requests
    from colorama import Fore, Back, Style
    import fileinput
    import requests
    from urllib.request import urlopen
    from urllib.error import *
    import datetime
    import schedule
    import time
    import pdfkit
    import http.server
    import socketserver
    from json2html import *
    import json

except ModuleNotFoundError:
    print('run the requirements.txt file to have all the requirements satisfied')

class arachni_class:

    def arachni_http(self, id_target, ip, port_n):

        repDir = str(id_target)
        ipScan = ip
        port = port_n
        print(repDir+' '+ipScan+' '+port)
        print(Fore.CYAN + '''
---"Start Arachni enumeration web service,  please wait!
                                                ''' + Style.RESET_ALL)
        try:  # arachni_reporter ../../example.com.afr --reporter=html:outfile=../../my_report.html.zip

                        print(
                            Fore.YELLOW + "\nExecute Arachni (HTTP mode) on port " + port + " .\n" + Style.RESET_ALL)
                        cmd = subprocess.run(["mkdir", repDir])
                        cmd = subprocess.run(["mkdir", repDir + "/Arachni_http"])
                        cmd = subprocess.run(["mkdir", "/var/www/html/report/" + repDir])
                        cmd = subprocess.run(["mkdir", "/var/www/html/report/" + repDir + "/Arachni_http"])
                        cmd = subprocess.run(["./arachni/bin/arachni", "--output-verbose", "--scope-include-subdomains",
                                              "http://" + ipScan + ":" + port,
                                              "--report-save-path=" + repDir + "/Arachni_http/Arachni_http.afr"])
                        cmd = subprocess.run(["./arachni/bin/arachni_reporter",
                                              repDir + "/Arachni_http/Arachni_http.afr",
                                              "--reporter=html:outfile=" + repDir + "/Arachni_http/Arachni_http.zip"])
                        cmd = subprocess.run(["unzip",
                                              repDir + "/Arachni_http/Arachni_http.zip",
                                              "-d", "/var/www/html/report/" + repDir + "/Arachni_http"])

        except KeyboardInterrupt:
            sys.exit()

    def arachni_https(self, id_target, ip, port_n):
        repDir = str(id_target)
        ipScan = ip
        port = port_n
        print(Fore.CYAN + '''
    ---"Start Arachni enumeration web service,  please wait!
                                                    ''' + Style.RESET_ALL)
        try:  # arachni_reporter ../../example.com.afr --reporter=html:outfile=../../my_report.html.zip


                        print(
                            Fore.YELLOW + "\nExecute Arachni (HTTPS mode) on port " + port + " .\n" + Style.RESET_ALL)
                        cmd = subprocess.run(["mkdir", repDir])
                        cmd = subprocess.run(["mkdir", repDir + "/Arachni_https"])
                        cmd = subprocess.run(["mkdir", "/var/www/html/report/"+repDir + "/Arachni_https"])
                        cmd = subprocess.run(["./arachni/bin/arachni", "--output-verbose", "--scope-include-subdomains",
                                              "https://" + ipScan + ":" + port,
                                              "--report-save-path=" + repDir + "/Arachni_https/Arachni_https.afr"])
                        cmd = subprocess.run(["./arachni/bin/arachni_reporter",
                                              repDir + "/Arachni_https/Arachni_https.afr",
                                              "--reporter=html:outfile=" + repDir + "/Arachni_https/Arachni_https.zip"])
                        cmd = subprocess.run(["unzip",
                                              repDir + "/Arachni_https/Arachni_https.zip",
                                              "-d", "/var/www/html/report/"+repDir + "/Arachni_https"])
        except KeyboardInterrupt:
            sys.exit()