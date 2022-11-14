#!/usr/bin/env python3

#this file is connector between suricata and mysql db


# Module Imports
import subprocess
import sys
import time
from datetime import datetime
import DB_connect
import mariadb
import nmap
import json
import yaml





timestamp_limit = ''

while True :

    file_json = "/var/log/suricata/eve.json"
    try:
        with open(file_json, 'r') as handle:
            json_data = [json.loads(line) for line in handle]
            lenght_file = len(json_data)
            for x in range(lenght_file):
                if json_data[x]['timestamp'] > timestamp_limit:
                    if json_data[x]["event_type"] == 'alert':
                        print('+++++++++++++++++++++++ record +++++++++++++++++++++++++')
                        timestamp = json_data[x]['timestamp']
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

                        # Database connection
                        try:
                            data = json.load(open("eng_conf.json"))

                            connessione = DB_connect.database_connect()
                            connDB = connessione.database_connection(data['user_db'], data['password_db'],
                                                                     data['host_db'],
                                                                     int(data['port_db']),
                                                                     data['database'])
                            suricataDB = connDB.cursor()
                        except:
                            print("suricata: errore connessione database")

                        id_asset = data['id_ass']

                        sql_insert_record = "INSERT INTO `suricata_alert` (`id_result_alert`, `id_asset`, `timestamp`, `src_ip`, `src_port`, `dest_ip`, `dest_port`, `proto`, `action`, `gid`, `signature_id`, `rev`, `signature`, `category`, `severity`) VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"

                        input_data = (id_asset,timestamp,src_ip,src_port,dest_ip,dest_port,proto,action,gid,signature_id,rev,signature,category,severity)
                        suricataDB.execute(sql_insert_record, input_data)
                        connDB.commit()

                        suricataDB.close()
                        connDB.close()


                        timestamp_limit = timestamp
        print('SURICATA ACTIVE....  Last record: ' + timestamp_limit+'...ZZZzzzz.....zzz...zz...z..')
        time.sleep(20)
    except:
        print("errore: file /var/log/suricata/eve.json no found")


    







