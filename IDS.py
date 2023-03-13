#!/usr/bin/env python3
# Module Imports
import json
import time
import os
import DB_connect
import crealog
import sys

timestamp_limit = ''

idprocess = "IDS"

try:
    data = json.load(open("eng_conf.json"))
except:
    print("Engine vulnscan non inizializzato! eseguire: ./inizializzazione_engine.py ")
    sys.exit(1)


ip_exclude_ids = data['ip_no_suricata']








while True:



    folder_path = "/var/log/suricata/"  # percorso della cartella

    name_prefix = "eve-"  # prefisso del nome del file

    # Ottiene i nomi dei file nella cartella con i relativi timestamp di creazione e filtra per nome iniziale
    files_with_timestamps = [(f, os.path.getctime(os.path.join(folder_path, f))) for f in os.listdir(folder_path) if
                             f.startswith(name_prefix)]

    # Ordina i file in base al timestamp di creazione
    sorted_files = sorted(files_with_timestamps, key=lambda x: x[1])

    # Elenca i nomi dei file in ordine di creazione
    for file in sorted_files[:-1]:

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Apertura del file "+str(file))


        file_json = file[0]
        print(file_json)
        file_json = folder_path+file_json

        with open(file_json, 'r') as handle:
            json_data = [json.loads(line) for line in handle]
            lenght_file = len(json_data)

            prev_src_ip = None
            prev_dest_ip = None
            prev_signature = None


            for x in range(lenght_file):
                if json_data[x]['timestamp'] > timestamp_limit:
                    if json_data[x]["event_type"] == 'alert':
                        print('+++++++++++++++++++++++ record +++++++++++++++++++++++++')
                        print('IP exclude: '+str(ip_exclude_ids))
                        timestamp = json_data[x]['timestamp']
                        timestamp_limit = timestamp

                        print('Time: ' + timestamp)
                        src_ip = json_data[x]['src_ip']
                        print('Source IP: ' + src_ip)
                        src_port = json_data[x]['src_port']
                        print('Source PORT: ' + str(src_port))
                        dest_ip = json_data[x]['dest_ip']
                        print('Destination IP: ' + dest_ip)
                        dest_port = json_data[x]['dest_port']
                        print('Destination PORT: ' + str(dest_port))
                        proto = json_data[x]['proto']
                        print('Proto: ' + proto)
                        action = json_data[x]['alert']['action']
                        print('Action: ' + action)
                        gid = json_data[x]['alert']['gid']
                        print('GID: ' + str(gid))
                        signature_id = json_data[x]['alert']['signature_id']
                        print('ID Signature: ' + str(signature_id))
                        rev = json_data[x]['alert']['rev']
                        print('Revision: ' + str(rev))
                        signature = json_data[x]['alert']['signature']
                        print('Signature: ' + signature)
                        category = json_data[x]['alert']['category']
                        print('Category: ' + category)
                        severity = json_data[x]['alert']['severity']
                        print('Severity: ' + str(severity))

                        if src_ip == prev_src_ip and dest_ip == prev_dest_ip and signature == prev_signature:
                            print('___________________________________________________________________');
                            print(' Record not inserted as it is a duplicate of the previous record.');
                            print('___________________________________________________________________');
                            time.sleep(0.2)
                            os.system('clear')
                            # ignora il record corrente se i valori sono uguali ai precedenti
                            continue

                        prev_src_ip = src_ip
                        prev_dest_ip = dest_ip
                        prev_signature = signature

                        if(src_ip == ip_exclude_ids or dest_ip == ip_exclude_ids) :
                            print('___________________________________________________________________');
                            print('Record not inserted as host excluded by the administrator')
                            print('___________________________________________________________________');

                        else:
                            # Database connection
                            try:
                                data = json.load(open("eng_conf.json"))

                                connessione = DB_connect.database_connect()
                                connDB = connessione.database_connection()
                                suricataDB = connDB.cursor()

                            except:
                                print("suricata: errore connessione database")

                            id_asset = data['id_ass']

                            sql_insert_record = "INSERT INTO `suricata_alert` (`id_result_alert`, `id_asset`, `timestamp`, `src_ip`, `src_port`, `dest_ip`, `dest_port`, `proto`, `action`, `gid`, `signature_id`, `rev`, `signature`, `category`, `severity`) VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"

                            input_data = (
                                id_asset, timestamp, src_ip, src_port, dest_ip, dest_port, proto, action, gid, signature_id,
                                rev,
                                signature, category, severity)
                            try:
                                suricataDB.execute(sql_insert_record, input_data)
                                connDB.commit()
                                print('___________________________________________________________________');
                                print('Record inserted in the database')
                                print('___________________________________________________________________');
                            except:
                                print('___________________________________________________________________');
                                print('Record duplicated in the database')
                                print('___________________________________________________________________');


                            suricataDB.close()
                            connDB.close()
                        time.sleep(0.2)
                        os.system('clear')


        log = crealog.log_event()
        log.crealog(idprocess,
                    "Caricamento degli alert sul DB completato.")


        os.remove(file_json)

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Rimozione del file "+str(file_json))

        print('SURICATA ACTIVE....  Last record: ' + timestamp_limit + '...ZZZzzzz.....zzz...zz...z..')
        time.sleep(1)
        os.system('clear')
    print('SURICATA ACTIVE....  Last record: ' + timestamp_limit + '...ZZZzzzz.....zzz...zz...z..')
    time.sleep(0.5)
    os.system('clear')
