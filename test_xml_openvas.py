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

with open('report_scan+4cdc1d7f-8871-40f1-9301-1ca0867d8c79.xml', 'r') as myfile:
    obj = xmltodict.parse(myfile.read())
    #print(json.dumps(obj))


obj = untangle.parse('report_scan+4cdc1d7f-8871-40f1-9301-1ca0867d8c79.xml')
print(obj.get_reports_response.report.task.name)


if False :
    tree = ET.parse('report_scan+4cdc1d7f-8871-40f1-9301-1ca0867d8c79.xml')
    root = tree.getroot()
    for record in root:
        print("####### UNO ########")
        print(record.tag, record.attrib, record.text)
        for record2 in record:
            print("----####### DUE ########")
            print(record2.tag, record2.attrib, record2.text)
            for record3 in record2:
                print("--------####### TRE ########")
                print(record3.tag, record3.attrib, record3.text)
                for record4 in record3:
                    print("------------####### QUATTRO ########")
                    print(record4.tag, record4.attrib, record4.text)
                    for record5 in record4:
                        print("----------------####### CINQUE ########")
                        print(record5.tag, record5.attrib, record5.text)
                        for record6 in record5:
                            print("--------------------####### SEI ########")
                            print(record6.tag, record6.attrib, record6.text)
                            for record7 in record6:
                                print("------------------------####### SETTE ########")
                                print(record7.tag, record7.attrib, record7.text)
                                for record8 in record7:
                                    print("----------------------------####### OTTO ########")
                                    print(record8.tag, record8.attrib, record8.text)


