#!/usr/bin/env python3
# Module Imports
import subprocess
import time
from datetime import datetime
import DB_connect
import os
import bz2
import xml.etree.ElementTree as ET

from xml.etree import ElementTree as ET

connessione = DB_connect.database_connect()
conn = connessione.database_connection("operator", "!d3f3n510!", '185.245.183.75', 3306, "defensio")

id_j = ''
# estrazione parametri del job selezionato

cur = conn.cursor()






id_job="110"

id_report=id_task=scan_start=scan_end=id_result=name_vul=host=port=nvt=family=threat=severity=description=tags=solution=solution_type=ref=type_verification=''


tree = ET.parse('report_casa_test.xml')
root = tree.getroot()
for record in root:
        #print(record.tag, record.attrib, record.text)
        for record2 in record:
                if record2.tag == "report":
                        id_report = record2.attrib["id"]
                        print(record2.tag, ":", record2.attrib["id"])
                if record2.tag == "task":
                        id_task = record2.attrib["id"]
                        print(record2.tag, ":", record2.attrib["id"])

                for record3 in record2:

                        if record3.tag == "scan_start":
                                scan_start = record3.text
                                print(record3.tag, ":", record3.text)
                        if record3.tag == "scan_end":
                                scan_end = record3.text
                                print(record3.tag, ":", record3.text)

                        for record4 in record3:
                                 if record4.tag == "result":
                                        print("###############################################################################################################")
                                        id_result = record4.attrib['id']
                                        print(record4.tag, record4.attrib['id'])
                                        for record5 in record4:
                                                tags = solution = solution_type = family = type_verification = ''
                                                if record5.tag == "name":
                                                        name_vul = record5.text
                                                        print(record5.tag,":",  record5.text)
                                                if record5.tag == "host":
                                                        host = record5.text
                                                        print(record5.tag,":",  record5.text)
                                                if record5.tag == "port":
                                                        port = record5.text
                                                        print(record5.tag,":",  record5.text)
                                                if record5.tag == "nvt":
                                                        nvt = record5.attrib['oid']
                                                        print(record5.tag,":",  record5.attrib['oid'])
                                                if record5.tag == "threat":
                                                        threat = record5.text
                                                        print(record5.tag,":key:",  record5.text)
                                                if record5.tag == "severity":
                                                        severity = record5.text
                                                        print(record5.tag,":sev:",  record5.text)
                                                if record5.tag == "description":
                                                        description = record5.text
                                                        print(record5.tag,":",  record5.text)
                                                for record6 in record5:

                                                        if record6.tag == "type":
                                                                type_verification = record6.text
                                                                print(record6.tag,":",  record6.text)
                                                        if record6.tag == "family":
                                                                family = record6.text
                                                                print(record6.tag,":",  record6.text)
                                                        if record6.tag == "tags":
                                                                tags = record6.text
                                                                print(record6.tag,":",  record6.text)
                                                        if record6.tag == "solution":
                                                                solution = record6.text
                                                                print(record6.tag,":",  record6.text)
                                                                solution_type = record6.attrib["type"]
                                                                print(record6.tag,":",  record6.attrib["type"])
                                                        for record7 in record6:
                                                                if record7.tag == "ref":
                                                                        ref = record7.attrib["id"]
                                                                        print(record7.tag,":", record7.attrib["id"])
                                                                sql_update_query = """INSERT
                                                                INTO
                                                                `openvas_report`(`id_report_DB`, `id_job`, `id_report`,
                                                                                 `id_task`, `scan_start`, `scan_end`,
                                                                                 `id_result`, `name_vul`, `host`,
                                                                                 `port`, `type_verification`, `nvt`,
                                                                                 `family`, `threat`, `severity`,
                                                                                 `description`, `tags`, `solution_type`,
                                                                                 `solution`, `ref`)
                                                                VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                                                                input_data = (id_job,id_report,id_task,scan_start,scan_end,id_result,name_vul,host,port,type_verification,nvt,family,str(threat),str(severity),str(description),tags,solution_type,solution,ref)
                                                                cur.execute(sql_update_query, input_data)
                                                                conn.commit()
conn.close()
