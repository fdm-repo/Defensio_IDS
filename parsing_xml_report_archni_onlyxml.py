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
import xmltodict
import json


class parsing_xml_webscanner:
    def parsing_report_to_DB(report_XML_NS):

        file_xml = report_XML_NS

        data = json.load(open("eng_conf.json"))

        connessione = DB_connect.database_connect()
        conn = connessione.database_connection(data['user_db'], data['password_db'], data['host_db'],
                                               int(data['port_db']), data['database'])

        cur = conn.cursor()

        ################### genera l'oggetto relativo al file xml in forma dizionario##############

        id_job = 546

        tree = ET.parse(file_xml)
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
                    if(child2.tag == 'issue'):

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



                            if(child3.tag == 'references'):
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

        sql_update_query = """INSERT INTO web_scanner_report(id_report_web, id_job, start_scan, finish_scan, id_report_seed) VALUES(NULL,%s,%s,%s,%s);"""
        input_data = (id_job,  start_datetime, finish_datetime, seed)

        cur.execute(sql_update_query, input_data)
        conn.commit()



        conn.close()





obj_pars = parsing_xml_webscanner
obj_pars.parsing_report_to_DB("Arachni_xml.xml")

