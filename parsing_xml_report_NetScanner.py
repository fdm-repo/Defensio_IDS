#!/usr/bin/env python3
# Module Imports
import json
import os

import xmltodict

import DB_connect


class parsing_xml_Netscanner:
    def parsing_report_to_DB(self, id_j, report_XML_NS):

        file_xml = report_XML_NS
        id_job = id_j

        data = json.load(open("eng_conf.json"))

        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()

        cur = conn.cursor()

        ################### genera l'oggetto relativo al file xml in forma dizionario##############

        with open(file_xml, 'r') as filereport:
            obj = xmltodict.parse(filereport.read())

            #################### estrazione dati del report ####################

            print('######################## Inizio Header Report #######################')

            # estrae l'ID Report
            try:
                id_report = obj["get_reports_response"]['report']['report']['@id']
                print('id_report: ', id_report)
            except:
                print("id_report non disponibile")
                id_report = 'NULL'


            # estrae il Task
            try:
                id_task = obj["get_reports_response"]['report']['report']['task']['@id']
                print('id_task: ', id_task)
            except:
                print("id_task non disponibile")
                id_task = 'NULL'

            # estrae scan_start
            try:
                scan_start = obj["get_reports_response"]['report']['report']['scan_start']
                print('scan_start: ', scan_start)
            except:
                print("scan_start non disponibile")
                scan_start = 'NULL'

            # estrae scan_end
            try:
                scan_end = obj["get_reports_response"]['report']['report']['scan_end']
                print('scan_end: ', scan_end)
            except:
                print("scan_end non disponibile")
                scan_end = 'NULL'

            # __ qui si mette il codice SQL per caricare il record nella tabella "openvas_report"___

            try:
                sql_update_query = """INSERT INTO `openvas_report`(`id_report_DB`, `id_job`, `id_report`, `id_task`, `scan_start`, `scan_end`) VALUES(NULL,%s,%s,%s,%s,%s)"""
                input_data = (id_job, id_report, id_task, scan_start, str(scan_end))
                cur.execute(sql_update_query, input_data)
                conn.commit()
            except:
                print("ERRORE:record in openvas_report non inserito")

            # ____________________________________________________________________________________

            #################### estrazione dati del result ####################

            print('######################## Fine Header Report #######################')

            print('\n######################## Inizio Result Report #######################')

            try:
                result = obj["get_reports_response"]['report']['report']['results']['result']

                a = 0
                for x in result:
                    print('------------------------Result n° ', a, ' ---------------------------')
                    # estrae id_result
                    try:
                        id_result = result[a]['@id']
                        print('Id_result: ', id_result)
                    except:
                        print('id_result non disponibile')
                        id_result = 'NULL'

                    # estrae name
                    try:
                        name_vul = result[a]['name']
                        print('Name_Vul: ', name_vul)
                    except:
                        print('name_vul non disponibile')
                        name_vul = 'NULL'

                    # estrae host
                    try:
                        hostname = result[a]['host']['hostname']
                        print('Hostname: ', hostname)
                    except:
                        print('hostname non disponibile')
                        hostname = 'NULL'

                    # estrae IP
                    try:
                        host = result[a]['host']['#text']
                        print('IP: ', host)
                    except:
                        print('host non disponibile')
                        host = 'NULL'

                    # estrae Port
                    try:
                        port = result[a]['port']
                        print('Port: ', port)
                    except:
                        print('port non disponibile')
                        host = 'NULL'

                    # estrae NVT
                    try:
                        type_verification = result[a]['nvt']['type']
                        print('Type Verificatione: ', type_verification)
                    except:
                        print('type_verification non disponibile')
                        type_verification = 'NULL'

                    # estrae NVT
                    try:
                        nvt = result[a]['nvt']['@oid']
                        print('NVT: ', nvt)
                    except:
                        print('NVT non disponibile')
                        nvt = 'NULL'

                    # estrae family
                    try:
                        family = result[a]['nvt']['family']
                        print('Family: ', family)
                    except:
                        print('family non disponibile')
                        family = 'NULL'

                    # estrae CVSS_base
                    try:
                        cvss_base = result[a]['nvt']['cvss_base']
                        print('CVSS_Base: ', cvss_base)
                    except:
                        print('CVSS non disponibile')
                        cvss_base = 'NULL'

                    # estrae TAGS e decompone gli elementi
                    try:
                        tags = result[a]['nvt']['tags']
                        print('Tags: ', tags)
                        single_tag = tags.split("|")
                        for x in single_tag:
                            uguale_split = x.split("=")
                            if (uguale_split[0] == 'cvss_base_vector'):
                               t_cvss_base_vector = uguale_split[1]
                            if (uguale_split[0] == 'summary'):
                                t_summary = uguale_split[1]
                            if (uguale_split[0] == 'insight'):
                                t_insight = uguale_split[1]
                            if (uguale_split[0] == 'affected'):
                                t_affected = uguale_split[1]
                            if (uguale_split[0] == 'impact'):
                                t_impact = uguale_split[1]
                            if (uguale_split[0] == 'solution'):
                                t_solution = uguale_split[1]
                            if (uguale_split[0] == 'vuldetect'):
                                t_vuldetect = uguale_split[1]
                            if (uguale_split[0] == 'solution_type'):
                                t_solution_type = uguale_split[1]
                    except:
                        print('TAGS non disponibile')
                        tags = 'NULL'

                    # estrae Solution_type
                    try:
                        solution_type = result[a]['nvt']['solution']['@type']
                        print('Solution Type: ', solution_type)
                    except:
                        print('solution_type non disponibile')
                        solution_type = 'NULL'

                    # estrae Solution_type
                    try:
                        solution = result[a]['nvt']['solution']['#text']
                        print('Solution: ', solution)
                    except:
                        print('solution non disponibile')
                        solution = 'NULL'

                    # estrae Threat
                    try:
                        threat = result[a]['threat']
                        print('Threat: ', threat)
                    except:
                        print('threat non disponibile')
                        threat = 'NULL'

                    # estrae Severity
                    try:
                        severity = result[a]['severity']
                        print('Threat: ', severity)
                    except:
                        print('severity non disponibile')
                        severity = 'NULL'

                    # estrae Description
                    try:
                        description = result[a]['description']
                        print('Description: ', description)
                    except:
                        print('description non disponibile')
                        description = 'NULL'

                    # __ qui si mette il codice SQL per caricare il record nella tabella "openvas_result"___
                    try:

                        sql_update_query = """INSERT INTO `openvas_result`(`id_result_DB`, `id_report`, `id_result`, `name_vul`, `host`, `port`, `nvt`, `threat`,
                                                                     `severity`, `description`, `type_verification`, `family`, `t_summary`, `t_insight`,
                                                                     `t_affected`, `t_impact`, `t_solution`, `t_vuldetect`, `t_solution_type`, `solution`,
                                                                     `solution_type`) VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        input_data = (
                            id_report, id_result, name_vul, host, port, nvt, threat, severity, description,
                            type_verification, family,
                            t_summary, t_insight, t_affected, t_impact, t_solution,
                            t_vuldetect, t_solution_type, solution, solution_type)
                        cur.execute(sql_update_query, input_data)
                        conn.commit()
                    except:
                        print("ERRORE:record in openvas_result non inserito")

                    # ____________________________________________________________________________________

                    # ciclo di estrazione dei reference di ogni result
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

                            b += 1
                    except:
                        print("not references")

                    a += 1  # incremento ciclo result
            except:
                print("ERROR no result")
        os.remove(file_xml)
        conn.close()
