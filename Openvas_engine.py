#!/usr/bin/env python3
# Module Imports
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from threading import Thread

import DB_connect
import parsing_xml_report_NetScanner

# username e password per il docker GVM

username = 'admin'
password = 'porcodio'


# definizione della funzione che estrae i valori dall'interrogazione sullo stato di progressione di una funzione
def statusscan(task):
    id_task = task

    # crea file xml di status
    status_buffer = open("status_scan.xml", "a")

    # crea la stringa xml monitorare la scansione con gvm-cli
    stringxmlscan = "<get_tasks task_id=\"" + id_task + "\"/>"

    # esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per monitorare il task, il risultato lo salva nel file xml di buffer
    cmd = subprocess.run(
        ["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli", "--gmp-username", username,
         "--gmp-password", password, "tls", "--xml", stringxmlscan], stdout=status_buffer)
    # chiude il file xml di buffer
    status_buffer.close()

    try:
        statustxml = ET.parse('status_scan.xml').getroot()

        # identifica la root del file xml
        # root = tree.getroot()

        # estrae l'attributo ID del task creato e lo salva nella variabile id_task
        due = statustxml.attrib['status_text']
        quattro = statustxml[1].attrib['id']
        sei = statustxml[1][1].text
        sette = statustxml[1][14].text
        otto = statustxml[1][15].text
        print(
            "Status (testo): " + due + " Task ID: " + quattro + " Nome: " + sei + " Stato scansione: " + sette + " Progressione scansione: " + otto)

        # aggiorna i valori della scansione sul DB di defensio

        # UPDATE `openvas_scan` SET `status` = 'remove', `progression` = '10' WHERE `openvas_scan`.`id_job` = '89';

        sql_update_openvas_scan_query = """UPDATE openvas_scan SET status = %s, progression = %s WHERE openvas_scan.id_task = %s; """
        input_data = (sette, otto, quattro)
        cur.execute(sql_update_openvas_scan_query, input_data)
        conn.commit()


    except:
        print("non funziona")

        # cancella il file xml di buffer
    try:
        scan_buffer.close()
        os.remove("status_scan.xml")
    except:
        print("not remove Buffer")

    return sette


def report_scan(task, id_j, report):
    # sudo  docker exec -t -u gvm openvas /usr/local/bin/gvm-cli  --gmp-username admin --gmp-password porcodio tls --xml "<get_reports report_id=\"57212fa8-9297-47e6-b0d1-991a827e3131\" format_id=\"5057e5cc-b825-11e4-9d0e-28d24461215b\"/>"
    print("ciao")
    id_task = task
    id_report = report
    id_job = id_j
    print("####################### Report della scansione " + id_task + " #######################")
    # crea file xml di status
    nomefile = "report_scan+" + id_report + ".xml"
    report_buffer = open(nomefile, "a")

    # crea la stringa xml monitorare la scansione con gvm-cli
    stringxmlreport = "<get_reports details='True' report_id=\"" + id_report + "\" format_id=\"a994b278-1f62-11e1-96ac-406186ea4fc5\"/>"

    # esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per monitorare il task, il risultato lo salva nel file xml di buffer
    cmd = subprocess.run(
        ["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli", "--gmp-username", username,
         "--gmp-password", password, "tls", "--xml", stringxmlreport], stdout=report_buffer)
    # chiude il file xml di buffer

    report_buffer.close()

    # richiama la funzione di parsing del file parsing_xml_report_Netscanner

    try:
        obj_pars = parsing_xml_report_NetScanner.parsing_xml_Netscanner()
        obj_pars.parsing_report_to_DB(id_job, nomefile)
        update_statistic_vul(id_j)

    except:
        print("errore nell'esecuzione del parsing sul file xml di report ")
    # test


def update_statistic_vul(id_j):
    id_job = id_j

    job_data = list()
    job_data.append(id_job)

    stat_host = conn.cursor()

    # estrae il numero di vuln di tipo Log trovati per lo specifico job
    sql_query_host_for_job = """ SELECT COUNT(openvas_result.threat) FROM openvas_result JOIN openvas_report ON openvas_result.id_report = openvas_report.id_report WHERE openvas_report.id_job = %s AND openvas_result.threat = 'Log'; """
    stat_host.execute(sql_query_host_for_job, job_data)
    result = stat_host.fetchone()
    Log_vuln = result[0]

    # estrae il numero di vuln di tipo Medium trovati per lo specifico job
    sql_query_host_for_job = """ SELECT COUNT(openvas_result.threat) FROM openvas_result JOIN openvas_report ON openvas_result.id_report = openvas_report.id_report WHERE openvas_report.id_job = %s AND openvas_result.threat = 'Medium'; """
    stat_host.execute(sql_query_host_for_job, job_data)
    result = stat_host.fetchone()
    Medium_vuln = result[0]

    # estrae il numero di vuln di tipo High trovati per lo specifico job
    sql_query_host_for_job = """ SELECT COUNT(openvas_result.threat) FROM openvas_result JOIN openvas_report ON openvas_result.id_report = openvas_report.id_report WHERE openvas_report.id_job = %s AND openvas_result.threat = 'High'; """
    stat_host.execute(sql_query_host_for_job, job_data)
    result = stat_host.fetchone()
    High_vuln = result[0]

    # aggiorna la tabella statistic_job del DB
    sql_update_query = """UPDATE statistic_job SET Log = %s, Medium = %s, High = %s WHERE statistic_job.id_job = %s; """
    update_data = (Log_vuln, Medium_vuln, High_vuln, id_job)
    stat_host.execute(sql_update_query, update_data)
    conn.commit()


token_ver = ''


def test():
    global token_ver
    while True:
        try:
            data = json.load(open("eng_conf.json"))
        except:
            print("Engine non inizializzato! eseguire: ./inizializzazione_engine.py ")
            sys.exit(1)
        id_ass = data['id_ass']

        conn_check = DB_connect.database_connect()
        conn = conn_check.database_connection()
        cur = conn.cursor()

        id_asset = list()
        id_asset.append(id_ass)

        try:
            sql_query_token = """SELECT token FROM engines WHERE engines.codeword = %s; """
            input_data = id_asset
            cur.execute(sql_query_token, input_data)

            token = cur.fetchone()
            token = token[0]

        except:
            print("nessun token rilevato")

        if token_ver != token:
            try:
                sql_update_query = """UPDATE engines SET active_openvas = %s WHERE engines.codeword = %s; """
                input_data = (token, id_ass)
                cur.execute(sql_update_query, input_data)
                conn.commit()
                token_ver = token
            except:
                print("verifica token non effettuata")

        print("++++++++++++++++++++++++++++++++++++++")
        print("DataTime: " + str(datetime.now()))
        print("Token attuale verificato: " + token)
        print("++++++++++++++++++++++++++++++++++++++")
        time.sleep(15)


t = Thread(target=test)
t.start()

while True:

    try:
        data = json.load(open("eng_conf.json"))
    except:
        print("Engine vulnscan non inizializzato! eseguire: ./inizializzazione_engine.py ")
        sys.exit(1)

    connessione = DB_connect.database_connect()
    conn = connessione.database_connection()

    id_ass = data['id_ass']
    id_asset = list()
    id_asset.append(id_ass)

    id_j = ''
    # estrazione parametri del job selezionato

    cur = conn.cursor()

    cur.execute(
        'SELECT id_job,id_asset,ip,netmask,exclude_ip FROM job  WHERE abilitato="on" AND net_discovery="on" AND openvas = "on" AND eseguito_openvas="off" AND id_asset = %s',
        (id_asset))
    if cur.rowcount != 0:
        result = cur.fetchone()
        print("Scansione OPENVAS")

        id_j = result[0]
        ip = result[2]
        netmask = result[3]
        ip_net = ip + '/' + netmask
        print("Target: " + ip_net)
        white_ip = result[4]
        print("Host esclusi: " + white_ip)
        if white_ip == 'none':
            white_ip = ''
        else:
            white_ip = "<exclude_hosts>" + str(white_ip) + "</exclude_hosts>"

        # genera la stringa di inizio del job
        start_job = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("StartJob: " + start_job)
        # variabile None da utilizzare nelle interrogazioni SQL per i campi autoincrementali
        vuoto = None

        # crea variabili per step creazione target

        id_target = ''
        id_task = ''
        id_report = ''

        ###################################################### crea target ########################################################

        if int(netmask) > 30 or int(netmask) < 20:
            host_target = ip
        else:
            host_target = ip_net

        # crea file xml buffer target
        target_buffer = open("target_buffer.xml", "a")

        # crea la stringa xml per creare il target con gvm-cli
        stringxmltarget = "<create_target><name>" + str(
            id_j) + "_" + start_job + "</name><hosts>" + host_target + "</hosts>" + white_ip + "<port_list id=\"33d0cd82-57c6-11e1-8ed1-406186ea4fc5\"></port_list></create_target>"

        # esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per creare il target, il risultato lo salva nel file xml di buffer
        cmd = subprocess.run(
            ["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli", "--gmp-username", username,
             "--gmp-password", password, "tls", "--xml", stringxmltarget], stdout=target_buffer)
        # chiude il file xml di buffer
        target_buffer.close()
        # richiama il file xml di buffer
        try:
            tree = ET.parse('target_buffer.xml')

            # identifica la root del file xml
            root = tree.getroot()

            # estrae l'attributo ID del target creato e lo salva nella variabile id_target
            id_target = root.attrib['id']
            print("ID_Target: " + id_target)
        except:
            print("target non creato")
        # cancella il file xml di buffer
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
            stringxmltask = "<create_task><name>" + str(
                id_j) + "_" + start_job + "</name><target id=\"" + id_target + "\"/><config id=\"daba56c8-73ec-11df-a475-002264764cea\"/><scanner id=\"08b69003-5fc2-4037-a479-93b440211c73\"/></create_task>"

            # esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per creare il task, il risultato lo salva nel file xml di buffer
            cmd = subprocess.run(
                ["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli", "--gmp-username", username,
                 "--gmp-password", password, "tls", "--xml", stringxmltask], stdout=task_buffer)
            # chiude il file xml di buffer
            task_buffer.close()
            # richiama il file xml di buffer
            tree = ET.parse('task_buffer.xml')

            # identifica la root del file xml
            root = tree.getroot()

            # estrae l'attributo ID del task creato e lo salva nella variabile id_task
            id_task = root.attrib['id']
            print("ID_Task: " + id_task)

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
                stringxmlscan = "<start_task task_id=\"" + id_task + "\"/>"

                # esegue il subprocesso sul docker gvm utilizzando gvm-cli e la stringa per avviare il task, il risultato lo salva nel file xml di buffer
                cmd = subprocess.run(
                    ["docker", "exec", "-t", "-u", "gvm", "openvas", "/usr/local/bin/gvm-cli", "--gmp-username",
                     username, "--gmp-password", password, "tls", "--xml", stringxmlscan], stdout=scan_buffer)
                # chiude il file xml di buffer
                scan_buffer.close()
                # richiama il file xml di buffer
                try:
                    reportxml = ET.parse('scan_buffer.xml').getroot()

                    # identifica la root del file xml
                    # root = tree.getroot()

                    # estrae l'attributo ID del task creato e lo salva nella variabile id_task
                    id_report = reportxml[0].text
                    print("ID_report: " + id_report)
                except:
                    print("Task non creato")

                # cancella il file xml di buffer
                try:
                    scan_buffer.close()
                    os.remove("scan_buffer.xml")
                except:
                    print("not remove Buffer")

                ############################################## crea il record della scansione sul DB defensio ##############################

                sql_insert_openvas_scan_query = """INSERT INTO `openvas_scan` (`id_job`, `id_task`, `status`, `progression`) VALUES (%s, %s, %s, %s); """
                input_data = (id_j, id_task, 'running', '0')
                cur.execute(sql_insert_openvas_scan_query, input_data)
                conn.commit()

                # ciclo while che verifica lo status della scansione ogni 10 secondi

                status_scan = "running"
                print(
                    "####################### Stato e progessione della scansione " + id_task + " #######################")
                while (status_scan != "Done"):

                    try:
                        status_scan = statusscan(id_task)

                    except:
                        print("Status scansione non disponibile")
                        break

                    if (status_scan == "Interrupted"):
                        break
                    if (status_scan == "Stopped"):
                        break
                    if (status_scan == "Stop Requested"):
                        break

                    time.sleep(10)
                # genera il report della scansione

                if (status_scan == "Done"):
                    try:
                        report_scan(id_task, id_j, id_report)
                    except:
                        print("Report non disponibile o errore")

        # scrive il tag esecuzione sul record del job

        sql_update_query = """UPDATE job SET eseguito_openvas = %s WHERE id_job  = %s"""
        input_data = ('on', result[0])
        cur.execute(sql_update_query, input_data)
        conn.commit()
        cur.close()

    print(
        """
 __     __          _                   ____                                               
 \ \   / /  _   _  | |  _ __    ___    / ___|    ___    __ _   _ __    _ __     ___   _ __ 
  \ \ / /  | | | | | | | '_ \  / __|   \___ \   / __|  / _` | | '_ \  | '_ \   / _ \ | '__|
   \ V /   | |_| | | | | | | | \__ \    ___) | | (__  | (_| | | | | | | | | | |  __/ | |   
    \_/     \__,_| |_| |_| |_| |___/   |____/   \___|  \__,_| |_| |_| |_| |_|  \___| |_|   
                                                                                           


    .........Vulnerability Scanner Active...Waiting for Jobs...  ZZZZZZ...ZZZZZ..ZZZ...\n""")
    time.sleep(20)
    os.system('clear')
    check = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn_check = DB_connect.database_connect()
    conn2 = conn_check.database_connection()

    cur2 = conn2.cursor()

    sql_update_query = """UPDATE engines SET last_check_VA = %s WHERE engines.codeword = %s; """
    input_data = (check, id_ass)
    cur2.execute(sql_update_query, input_data)
    conn2.commit()
    cur2.close()
    conn2.close()
