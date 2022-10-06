#!/usr/bin/env python3
# Module Imports
import subprocess
import time
from datetime import datetime
import DB_connect
import os
import xml.etree.ElementTree as ET

#username e password per il docker GVM

username = 'admin'
password = 'porcodio'


# definizione della funzione che estrae i valori dall'interrogazione sullo stato di progressione di una funzione
def statusscan(task):
    id_task=task

    # crea file xml di status
    status_buffer = open("status_scan.xml", "a")

    # crea la stringa xml monitorare la scansione con gvm-cli
    stringxmlscan = "<get_tasks task_id=\"" + id_task + "\"/>"

    # esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per monitorare il task, il risultato lo salva nel file xml di buffer
    cmd = subprocess.run(["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli", "--gmp-username", username, "--gmp-password", password, "tls", "--xml", stringxmlscan], stdout=status_buffer)
    # chiude il file xml di buffer
    status_buffer.close()

    try:
        statustxml = ET.parse('status_scan.xml').getroot()

        # identifica la root del file xml
        # root = tree.getroot()

        # estrae l'attributo ID del task creato e lo salva nella variabile id_task
        due = statustxml.attrib['status_text']
        print("Status (testo): " + due)
        quattro = statustxml[1].attrib['id']
        print("Task ID: " + quattro)
        sei = statustxml[1][1].text
        print("Nome: " + sei)
        sette = statustxml[1][14].text
        print("Stato scansione: " + sette)
        otto = statustxml[1][15].text
        print("Progressione scansione: " + otto)


    except:
        print("non funziona")

        # cancella il file xml di buffer
    try:
        scan_buffer.close()
        os.remove("status_scan.xml")
    except:
        print("not remove Buffer")

    return sette

while True:

    connessione = DB_connect.database_connect()
    conn=connessione.database_connection("operator","!d3f3n510!", '185.245.183.75', 3306, "defensio")

    id_j=''
    # estrazione parametri del job selezionato

    cur = conn.cursor()

    cur.execute('SELECT id_job,ip,netmask FROM job  WHERE abilitato="on" AND openvas="off"')
    if cur.rowcount != 0:
        result = cur.fetchone()
        print(result)

        id_j=result[0]
        ip=result[1]
        netmask=result[2]
        ip_net=ip+'/'+netmask
        print(ip_net)
        # genera la stringa di inizio del job
        start_job = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(start_job)
        # variabile None da utilizzare nelle interrogazioni SQL per i campi autoincrementali
        vuoto = None

        #crea variabili per step creazione target

        id_target = ''
        id_task = ''
        id_report = ''



       ###################################################### crea target ########################################################

        #crea file xml buffer target
        target_buffer = open("target_buffer.xml", "a")

        #crea la stringa xml per creare il target con gvm-cli
        stringxmltarget="<create_target><name>"+str(id_j)+"</name><hosts>"+ip+"</hosts><port_list id=\"33d0cd82-57c6-11e1-8ed1-406186ea4fc5\"></port_list></create_target>"

        #esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per creare il target, il risultato lo salva nel file xml di buffer
        cmd = subprocess.run(["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli",  "--gmp-username",username, "--gmp-password",password,"tls", "--xml",stringxmltarget], stdout=target_buffer)
        # chiude il file xml di buffer
        target_buffer.close()
        # richiama il file xml di buffer
        try:
            tree = ET.parse('target_buffer.xml')

        #identifica la root del file xml
            root = tree.getroot()

        #estrae l'attributo ID del target creato e lo salva nella variabile id_target
            id_target = root.attrib['id']
            print("ID_Target: "+id_target)
        except:
            print("target non creato")
        #cancella il file xml di buffer
        try:
            target_buffer.close()
            os.remove("target_buffer.xml")
        except:
            print("not remove Buffer")

        # se il target è stato creato si prosegue a creare il task
        if id_target != '':

            ###################################################### crea task ########################################################

            # crea file xml buffer task
            task_buffer = open("task_buffer.xml", "a")

            # crea la stringa xml per creare il target con gvm-cli
            stringxmltask = "<create_task><name>"+str(id_j)+"</name><target id=\""+id_target+"\"/><config id=\"daba56c8-73ec-11df-a475-002264764cea\"/><scanner id=\"08b69003-5fc2-4037-a479-93b440211c73\"/></create_task>"

            # esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per creare il task, il risultato lo salva nel file xml di buffer
            cmd = subprocess.run(["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli", "--gmp-username", username,"--gmp-password", password, "tls", "--xml", stringxmltask], stdout=task_buffer)
            # chiude il file xml di buffer
            task_buffer.close()
            # richiama il file xml di buffer
            tree = ET.parse('task_buffer.xml')

            # identifica la root del file xml
            root = tree.getroot()

            # estrae l'attributo ID del task creato e lo salva nella variabile id_task
            id_task = root.attrib['id']
            print("ID_Task: "+id_task)

            # cancella il file xml di buffer
            try:
                task_buffer.close()
                os.remove("task_buffer.xml")
            except:
                print("not remove Buffer")


            # se il task è stato creato si prosegue ad avviarlo
            if id_task != '':

                ###################################################### avvia la scansione ########################################################

                # crea file xml buffer scan
                scan_buffer = open("scan_buffer.xml", "a")

                # crea la stringa xml per creare il target con gvm-cli
                stringxmlscan ="<start_task task_id=\""+id_task+"\"/>"

                # esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per avviare il task, il risultato lo salva nel file xml di buffer
                cmd = subprocess.run(["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli", "--gmp-username", username, "--gmp-password", password, "tls", "--xml", stringxmlscan], stdout=scan_buffer)
                # chiude il file xml di buffer
                scan_buffer.close()
                # richiama il file xml di buffer
                try:
                    reportxml = ET.parse('scan_buffer.xml').getroot()

                # identifica la root del file xml
                #root = tree.getroot()

                # estrae l'attributo ID del task creato e lo salva nella variabile id_task
                    id_report = reportxml[0].text
                    print("ID_report: " + id_report)
                except:
                    print("non funziona")


                # cancella il file xml di buffer
                try:
                    scan_buffer.close()
                    os.remove("scan_buffer.xml")
                except:
                    print("not remove Buffer")


                #ciclo while che verifica lo status della scansione ogni 5 secondi

                status_scan="running"

                while (status_scan != "Done"):

                    try:
                        status_scan = statusscan(id_task)
                    except:
                        print("non funziona")

                    time.sleep(5)

        # scrive il tag esecuzione sul record del job
        sql_update_query = """UPDATE job SET openvas = %s WHERE id_job  = %s"""
        input_data = ('on', result[0])
        #cur.execute(sql_update_query, input_data)
        #conn.commit()
        cur.close()


    time.sleep(5)