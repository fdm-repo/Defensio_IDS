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
    import parsing_xml_report_archni_onlyxml

except ModuleNotFoundError:
    print('run the requirements.txt file to have all the requirements satisfied')

class arachni_class:

    def arachni_http(self, id_target, ip, port_n):

        id_job = id_target
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

                        cmd = subprocess.run(["./arachni/bin/arachni", "--output-verbose", "--scope-include-subdomains",
                                              "http://" + ipScan + ":" + port,
                                              "--report-save-path=" + repDir + "/Arachni_http.afr"])
                        cmd = subprocess.run(["./arachni/bin/arachni_reporter",
                                              repDir + "/Arachni_http.afr",
                                              "--reporter=xml:outfile=Arachni_http.xml"])
                        file = "Arachni_http.xml"
                        obj_parsing = parsing_xml_report_archni_onlyxml
                        obj_parsing.parsing_xml_webscanner.parsing_report_to_DB(file,id_job,ipScan,port)

        except KeyboardInterrupt:
            sys.exit()

    def arachni_https(self, id_target, ip, port_n):

        id_job = id_target
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

                        cmd = subprocess.run(["./arachni/bin/arachni", "--output-verbose", "--scope-include-subdomains",
                                              "https://" + ipScan + ":" + port,
                                              "--report-save-path=" + repDir + "/Arachni_https.afr"])

                        cmd = subprocess.run(["./arachni/bin/arachni_reporter",
                                              repDir + "/Arachni_https.afr",
                                              "--reporter=xml:outfile=Arachni_https.xml"])

                        file = "Arachni_https.xml"
                        obj_parsing = parsing_xml_report_archni_onlyxml
                        obj_parsing.parsing_xml_webscanner.parsing_report_to_DB(file,id_job,ipScan,port)

        except KeyboardInterrupt:
            sys.exit()