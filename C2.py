#!/bin/python3

# dependency check for the modules

import os
import subprocess
import time
import DB_connect
import sys
import json
from pathlib import Path

print(
        """
                                                                                           
   _|_|_|    _|_|          _|_|_|                        _|                                
 _|        _|    _|      _|        _|    _|    _|_|_|  _|_|_|_|    _|_|    _|_|_|  _|_|    
 _|            _|          _|_|    _|    _|  _|_|        _|      _|_|_|_|  _|    _|    _|  
 _|          _|                _|  _|    _|      _|_|    _|      _|        _|    _|    _|  
   _|_|_|  _|_|_|_|      _|_|_|      _|_|_|  _|_|_|        _|_|    _|_|_|  _|    _|    _|  
                                         _|                                                
                                     _|_|                                                  
        \n""")


user_no_admin = input("Inserire Username utente NON amministratore: ")

fileDaVerificare=Path("./eng_conf.json")
if fileDaVerificare.is_file():
   print("Esiste un file di configurazione!")
   edit_conf = input("Desideri comunque riconfigurare il sensore? Y/N")
   if edit_conf == 'Y':
       subprocess.run(["python3","./inizializzazione_engine.py"])
else:
    edit_conf2 = input("Bisogna procedere alla configurazione del sensore! Vuoi continuare? Y/N")
    if edit_conf2 == 'Y':
        subprocess.run(["python3","./inizializzazione_engine.py"])
    else:
        print("GoodbYe...")
        sys.exit(1)




os.system('clear')





while True:

    print(
        """
                                                                                           
   _|_|_|    _|_|          _|_|_|                        _|                                
 _|        _|    _|      _|        _|    _|    _|_|_|  _|_|_|_|    _|_|    _|_|_|  _|_|    
 _|            _|          _|_|    _|    _|  _|_|        _|      _|_|_|_|  _|    _|    _|  
 _|          _|                _|  _|    _|      _|_|    _|      _|        _|    _|    _|  
   _|_|_|  _|_|_|_|      _|_|_|      _|_|_|  _|_|_|        _|_|    _|_|_|  _|    _|    _|  
                                         _|                                                
                                     _|_|                                                  
        \n""")

    try:
        data = json.load(open("eng_conf.json"))
    except:
        print("!!! Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
        sys.exit(1)
    id_ass = data['id_ass']




    web_scanner = os.popen("pgrep -fx \"python3 ./WebScanner_engine.py\"").read()

    if web_scanner == '':
        web_scanner_token = "Disattivato"
        print("Avvio processo WebScanner_engine.py")
        subprocess.run(["gnome-terminal","--","bash", "-c","sudo -u "+user_no_admin+" ./WebScanner_engine.py"])
    else:
        web_scanner_token = "Attivo"
        print("Processo WebScanner_engine.py attivo con PID: "+str(web_scanner))

    scheduling = os.popen("pgrep -fx \"python3 ./Scheduling.py\"").read()

    if scheduling == '':
        print("Avvio processo Scheduling.py")
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "sudo -u "+user_no_admin+" ./Scheduling.py"])
    else:
        print("Processo Scheduling.py attivo con PID: " + str(scheduling))


    email_leak = os.popen("pgrep -fx \"python3 ./Email_Leaks.py\"").read()

    if email_leak == '':
        print("Avvio processo Email_Leaks.py")
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "sudo -u "+user_no_admin+" ./Email_Leaks.py"])
    else:
        print("Processo Email_Leaks.py attivo con PID: " + str(email_leak))


    defensio_engine = os.popen("pgrep -fx \"python3 ./Defensio_engine.py\"").read()

    if defensio_engine == '':
        net_scanner_token = "Disattivato"
        print("Avvio processo Defensio_engine.py")
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "sudo ./Defensio_engine.py"])
    else:
        net_scanner_token = "Attivo"
        print("Processo Defensio_engine.py attivo con PID: " + str(defensio_engine))


    openvas_engine = os.popen("pgrep -fx \"python3 ./Openvas_engine.py\"").read()

    if openvas_engine == '':
        vuln_scanner_token = "Disattivato"
        print("Avvio processo VulnScan_engine.py")
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "sudo ./Openvas_engine.py"])
    else:
        vuln_scanner_token = "Attivo"
        print("Processo VulnScan_engine.py attivo con PID: " + str(openvas_engine))


    sharescanner_engine = os.popen("pgrep -fx \"python3 ./ShareScanner_engine.py\"").read()

    if sharescanner_engine == '':
        share_scanner_token = "Disattivato"
        print("Avvio processo ShareScanner_engine.py")
        subprocess.run(["gnome-terminal", "--", "bash", "-c", "sudo ./ShareScanner_engine.py"])
    else:
        share_scanner_token = "Attivo"
        print("Processo ShareScanner_engine.py attivo con PID: " + str(sharescanner_engine))

    c2_connect = DB_connect.database_connect()
    c2_conn = c2_connect.database_connection()

    c2_cur = c2_conn.cursor()

    sql_update_query = """UPDATE engines SET active_defensio = %s, active_webscanner = %s,active_openvas = %s,active_share_scanner=%s WHERE engines.codeword = %s; """
    input_data = (net_scanner_token,web_scanner_token,vuln_scanner_token,share_scanner_token, id_ass)
    c2_cur.execute(sql_update_query, input_data)
    c2_conn.commit()
    c2_conn.close()




    time.sleep(20)
    os.system('clear')