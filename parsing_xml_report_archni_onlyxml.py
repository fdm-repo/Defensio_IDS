#!/usr/bin/env python3
# Module Imports
import json
import crealog
from xml.etree import ElementTree as ET

import DB_connect

idprocess = "parsing_xml_report_archni_onlyxml"

class parsing_xml_webscanner:
    def parsing_report_to_DB(report_XML_NS, id_j, ip_j, port_j):

        id_job = id_j
        ip = ip_j
        port = port_j

        file_xml = report_XML_NS

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Definizione del file di report: "+str(file_xml)+" relativo al job: "+str(id_job))

        data = json.load(open("eng_conf.json"))

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Connessione al DB")

        connessione = DB_connect.database_connect()
        conn = connessione.database_connection()

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Connessione aal database riuscita")

        cur = conn.cursor()

        ################### genera l'oggetto relativo al file xml in forma dizionario##############

        tree = ET.parse(file_xml)

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Apertura del file e generazione di un oggetto a dizionario")

        root = tree.getroot()

        for child in root:
            if child.tag == "seed":
                print(child.text)
                seed = child.text

            if child.tag == "start_datetime":
                print(child.text)
                start_datetime = child.text

            if child.tag == "finish_datetime":
                print(child.text)
                finish_datetime = child.text

            if child.tag == 'issues':
                for child2 in child:
                    if (child2.tag == 'issue'):

                        for child3 in child2:
                            if child3.tag == "name":
                                print(child3.text)
                                name = child3.text
                            if child3.tag == "description":
                                print(child3.text)
                                description = child3.text
                            if child3.tag == "remedy_guidance":
                                print(child3.text)
                                remedy_guidance = child3.text
                            if child3.tag == "severity":
                                print(child3.text)
                                severity = child3.text
                            if child3.tag == "cwe":
                                print(child3.text)
                                cwe = child3.text
                            if child3.tag == "digest":
                                print(child3.text)
                                digest = child3.text

                            if (child3.tag == 'references'):
                                for child4 in child3:
                                    print("____reference____")
                                    print(child4.attrib["title"])
                                    title = child4.attrib["title"]
                                    print(child4.attrib["url"])
                                    url_ref = child4.attrib["url"]

                                    sql_update_query = """INSERT INTO `web_scanner_ref` (`id_ref`, `digest`, `title`, `url`) VALUES (NULL,%s,%s,%s);"""
                                    input_data = (digest, title, url_ref)

                                    cur.execute(sql_update_query, input_data)
                                    conn.commit()

                                    log = crealog.log_event()
                                    log.crealog(idprocess,
                                                "Inserimento nella tabella web_scanner_ref del reference: "+str(digest)+" "+str(title)+" "+str(url_ref))

                            if (child3.tag == 'vector'):
                                for child4 in child3:
                                    if child4.tag == "class":
                                        print(child4.text)
                                        vector_class = child4.text
                                    if child4.tag == "type":
                                        print(child4.text)
                                        vector_type = child4.text
                                    if child4.tag == "url":
                                        print(child4.text)
                                        vector_url = child4.text
                                    if child4.tag == "action":
                                        print(child4.text)
                                        vector_action = child4.text

                        sql_update_query = """INSERT INTO `web_scanner_result` (`id_result`, `seed`, `name`, `description`, `remedy_guidance`, `severity`, `cwe`, `digest`, `vector_class`, `vector_type`, `vector_url`, `vector_action`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
                        input_data = (
                            seed, name, description, remedy_guidance, severity, cwe, digest, vector_class, vector_type,
                            vector_url, vector_action)



                        cur.execute(sql_update_query, input_data)
                        conn.commit()

                        log = crealog.log_event()
                        log.crealog(idprocess,
                                    "Inserimento nella tabella web_scanner_result del result: " + str(
                                        seed) + " " + str(name))

        sql_update_query = """INSERT INTO web_scanner_report(id_report_web, id_job, ip, port, start_scan, finish_scan, id_report_seed) VALUES(NULL,%s,%s,%s,%s,%s,%s);"""
        input_data = (id_job, ip, port, start_datetime, finish_datetime, seed)

        cur.execute(sql_update_query, input_data)
        conn.commit()

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Inserimento nella tabella web_scanner_report del report: " + str(
                        id_job) + " " + str(seed))

        conn.close()

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Chiusura della connessione al DB")
