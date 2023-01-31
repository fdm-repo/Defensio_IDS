#!/bin/python3

import whois

# dependency check for the modules
import DB_connect

connessione = DB_connect.database_connect()
conn = connessione.database_connection()

cur = conn.cursor()

id_job = 149


job = list()
job.append(id_job)

sql_select = """SELECT ip,public_ip FROM job where id_job = %s; """
cur.execute(sql_select, job)
result = cur.fetchone()
domain = result[0]
print(domain)
public_ip = result[1]
print(public_ip)

if public_ip == 'si':
    print(domain)
    result_whois = whois.whois(domain).text
    print(result_whois)
    print("porco")
    sql_update_query = """INSERT INTO `whois_result` (`id_result_whois`, `id_job`, `ip_domain`, `result`) VALUES (NULL,%s,%s,%s);"""
    input_data = (id_job, domain, result_whois)

    cur.execute(sql_update_query, input_data)
    conn.commit()

