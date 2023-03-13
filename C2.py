#!/usr/bin/env python3

# dependency check for the modules

import os
import signal
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


fileDaVerificare=Path("./eng_conf.json")
if fileDaVerificare.is_file():
   print("Esiste un file di configurazione!")

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
    Version OnlyIDS 13/03/2023 n3TSh4d3 \n""")

    try:
        data = json.load(open("eng_conf.json"))
    except:
        print("!!! Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
        sys.exit(1)

    id_ass = data['id_ass']
    id_asset = list()
    id_asset.append(id_ass)

    user_no_admin = data['user_no_root']

    c2_connect = DB_connect.database_connect()
    c2_conn = c2_connect.database_connection()

    c2_cur = c2_conn.cursor()

    c2_cur.execute('SELECT defensio_ATTIVO FROM engines WHERE codeword = %s', id_asset)
    result = c2_cur.fetchone()

    status = result[0]

    if status == 'on':
        
        IDS_engine = os.popen("pgrep -fx \"python3 ./IDS.py\"").read()

        if IDS_engine == '':
            ids_token = "Disattivato"
            print("Avvio processo IDS_engine.py")
            subprocess.run(["gnome-terminal", "--title=IDS", "--", "bash", "-c", "sudo ./IDS.py"])
        else:
            ids_token = "Attivo"
            print("Processo IDS_engine.py attivo con PID: " + str(IDS_engine))

        c2_connect = DB_connect.database_connect()
        c2_conn = c2_connect.database_connection()

        c2_cur = c2_conn.cursor()

        sql_update_query = """UPDATE engines SET active_suricata = %s WHERE engines.codeword = %s; """
        input_data = (ids_token , id_ass)
        c2_cur.execute(sql_update_query, input_data)
        c2_conn.commit()

    elif status == 'off':


        IDS_engine = os.popen("pgrep -fx \"python3 ./IDS_engine.py\"").read()

        if IDS_engine != '':
            print("termina processo IDS_engine.py PID " + IDS_engine)
            IDS_engine = int(IDS_engine)
            os.kill(IDS_engine, signal.SIGKILL)

        net_scanner_token = web_scanner_token = vuln_scanner_token = share_scanner_token = ids_token = "Disattivato"

        c2_connect = DB_connect.database_connect()
        c2_conn = c2_connect.database_connection()

        c2_cur = c2_conn.cursor()

        sql_update_query = """UPDATE engines SET active_suricata = %s WHERE engines.codeword = %s; """
        input_data = (ids_token, id_ass)
        c2_cur.execute(sql_update_query, input_data)
        c2_conn.commit()

        print("Sistema DEFENSIO disattivato dall'Amministratore")



    else:
        print("ERRORE Nessuna operazione eseguibile.")

    c2_conn.close()




    time.sleep(20)
    os.system('clear')