#!/usr/bin/env python3
# Module Imports
import subprocess
import time
from datetime import datetime
import DB_connect
import os
import bz2
import xml.etree.ElementTree as ET
import json
import untangle
from xml.etree import ElementTree as ET
import xmltodict


connessione = DB_connect.database_connect()
conn = connessione.database_connection("operator", "!d3f3n510!", '185.245.183.75', 3306, "defensio")

cur = conn.cursor()



id_job = '123'

################### genera l'oggetto relativo al file xml in forma dizionario##############


with open('report_scan+4cdc1d7f-8871-40f1-9301-1ca0867d8c79.xml', 'r') as filereport:
    obj = xmltodict.parse(filereport.read())

#################### estrazione dati del report ####################

    print('######################## Inizio Header Report #######################')

    # estrae l'ID Report
    id_report=obj["get_reports_response"]['report']['report']['@id']
    print('id_report: ',id_report)

    #estrae il Task

    id_task = obj["get_reports_response"]['report']['report']['task']['@id']
    print('id_task: ',id_task)

    #estrae scan_start

    scan_start = obj["get_reports_response"]['report']['report']['scan_start']
    print('scan_start: ',scan_start)

    # estrae scan_end

    scan_end = obj["get_reports_response"]['report']['report']['scan_end']
    print('scan_end: ', scan_end)

#__ qui si mette il codice SQL per caricare il record nella tabella "openvas_report"___

    sql_update_query = """INSERT INTO `openvas_report`(`id_report_DB`, `id_job`, `id_report`, `id_task`, `scan_start`, `scan_end`) VALUES(NULL,%s,%s,%s,%s,%s)"""
    input_data = (id_job, id_report, id_task, scan_start, str(scan_end))
    cur.execute(sql_update_query, input_data)
    conn.commit()


#____________________________________________________________________________________

#################### estrazione dati del result ####################

    print('######################## Fine Header Report #######################')

    print('\n######################## Inizio Result Report #######################')

    result = obj["get_reports_response"]['report']['report']['results']['result']

    a = 0
    for x in result:
        print('------------------------Result n° ',a,' ---------------------------')
        # estrae id_result
        id_result = result[a]['@id']
        print('Id_result: ', id_result)

        # estrae name
        name_vul = result[a]['name']
        print('Name_Vul: ', name_vul)

        # estrae host
        hostname = result[a]['host']['hostname']
        print('Hostname: ', hostname)

        # estrae IP
        host = result[a]['host']['#text']
        print('IP: ', host)

        # estrae Port
        port = result[a]['port']
        print('Port: ', port)

        # estrae NVT
        type_verification = result[a]['nvt']['type']
        print('Type Verificatione: ', type_verification)

        # estrae NVT
        nvt = result[a]['nvt']['@oid']
        print('NVT: ', nvt)

        # estrae family
        family = result[a]['nvt']['family']
        print('Family: ', family)

        # estrae CVSS_base
        cvss_base = result[a]['nvt']['cvss_base']
        print('CVSS_Base: ', cvss_base)

        # estrae TAGS
        tags = result[a]['nvt']['tags']
        print('Tags: ', tags)

        # estrae Solution
        solution_type = result[a]['nvt']['solution']['@type']
        print('Solution Type: ', solution_type)

        try:
            solution = result[a]['nvt']['solution']['#text']
            print('Solution: ', solution)
        except:
            solution = ''
            print('Solution: ', solution)

        # estrae Threat
        threat = result[a]['threat']
        print('Threat: ', threat)

        # estrae Severity
        severity = result[a]['severity']
        print('Threat: ', severity)

        # estrae Description
        description = result[a]['description']
        print('Description: ', description)
        # __ qui si mette il codice SQL per caricare il record nella tabella "openvas_result"___

        sql_update_query = """INSERT INTO `openvas_result`(`id_result_DB`, `id_report`, `id_result`, `name_vul`, `host`,`port`, `type_verification`, `nvt`,`family`, `threat`, `severity`,
                                                                                                                                                 `description`, `tags`, `solution_type`,
                                                                                                                                                 `solution`)
                                                                                                                                VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        input_data = (
        id_report, id_result, name_vul, host, port, type_verification, nvt, family, threat, severity,
        description, tags, solution_type, solution)
        cur.execute(sql_update_query, input_data)
        conn.commit()



        # ____________________________________________________________________________________

        #ciclo di estrazione dei reference di ogni result
        try:
            referen = result[a]['nvt']['refs']['ref']
            b = 0
            for x in referen:
                # estrae ref
                ref = referen[b]['@id']
                print('REF: ', ref)

                # __ qui si mette il codice SQL per caricare il record nella tabella "openvas_ref"___

                sql_update_query = """INSERT INTO `openvas_ref`(`id_ref_DB`, `id_result`, `ref`) VALUES(NULL,%s,%s)"""
                input_data = (id_result, ref)
                cur.execute(sql_update_query, input_data)
                conn.commit()
                # ____________________________________________________________________________________

                b+=1
        except:
            print("not references")


        a+=1    #incremento ciclo result


conn.close()






