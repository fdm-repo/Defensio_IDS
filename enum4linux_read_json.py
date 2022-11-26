#!/usr/bin/env python3
# Module Imports
import sys
import time
from datetime import datetime
import DB_connect
import mariadb
import nmap
import json





#Database connection
try:

    connessione = DB_connect.database_connect()
    connDB = connessione.database_connection()
    enumDB = connDB.cursor()
except:
    print("enum4linux: errore connessione database" )

class enum4linux_read_json_class:

    def enum4linux_read_json(self, job_enum, start_job, file_json):
        job = job_enum
        start_job = start_job
        file_json = file_json
        with open(file_json, 'r') as json_file:
            enum_smb = json.load(json_file)
            target = str(enum_smb['target']['host'])
            credential = str(enum_smb['credentials']['user'])
            ldap = str(enum_smb['services']['LDAP']['accessible'])
            samba = str(enum_smb['services']['SMB']['accessible'])
            dominio = str(enum_smb['domain'])

            for i in range(len(enum_smb['nmblookup'])):
                nmblookup = enum_smb['nmblookup'][i]

            """                                                                                                                                                                                                                                                           
            "smb_domain_info": {                                                                                                                                                                                                                                          
                "NetBIOS computer name": "METASPLOITABLE",                                                                                                                                                                                                                
                "NetBIOS domain name": "",                                                                                                                                                                                                                                
                "DNS domain": "localdomain",                                                                                                                                                                                                                              
                "FQDN": "metasploitable.localdomain",                                                                                                                                                                                                                     
                "Derived membership": "workgroup member",                                                                                                                                                                                                                 
                "Derived domain": "unknown"                                                                                                                                                                                                                               
            """
            computer_name = str(enum_smb['smb_domain_info']['NetBIOS computer name'])
            domain_name = str(enum_smb['smb_domain_info']['NetBIOS domain name'])
            dns_domain = str(enum_smb['smb_domain_info']['DNS domain'])
            fqdn = str(enum_smb['smb_domain_info']['FQDN'])
            derived_membership = str(enum_smb['smb_domain_info']['Derived membership'])
            derived_domain = str(enum_smb['smb_domain_info']['Derived domain'])

            """                                                                                                                                                                                                                                                           
            "sessions": {                                                                                                                                                                                                                                                 
                "sessions_possible": true,                                                                                                                                                                                                                                
                "null": true,                                                                                                                                                                                                                                             
                "password": false,                                                                                                                                                                                                                                        
                "kerberos": false,                                                                                                                                                                                                                                        
                "nthash": false,                                                                                                                                                                                                                                          
                "random_user": false                                                                                                                                                                                                                                      


            """
            sessions_possible = str(enum_smb['sessions']['sessions_possible'])
            sessions_null = str(enum_smb['sessions']['null'])
            sessions_password = str(enum_smb['sessions']['password'])
            sessions_kerberos = str(enum_smb['sessions']['kerberos'])
            sessions_nthash = str(enum_smb['sessions']['nthash'])
            sessions_random_user = str(enum_smb['sessions']['random_user'])

            """                                                                                                                                                                                                                                                           
            "rpc_domain_info": {                                                                                                                                                                                                                                          
                "Domain": "WORKGROUP",                                                                                                                                                                                                                                    
                "Domain SID": "NULL SID",                                                                                                                                                                                                                                 
                "Membership": "workgroup member"                                                                                                                                                                                                                          
            """
            rpc_domain = str(enum_smb['rpc_domain_info']['Domain'])
            rpc_domain_sid = str(enum_smb['rpc_domain_info']['Domain SID'])
            rpc_membership = str(enum_smb['rpc_domain_info']['Membership'])

            """                                                                                                                                                                                                                                                           
            "os_info": {                                                                                                                                                                                                                                                  
                "OS": "Linux/Unix (Samba 3.0.20-Debian)",                                                                                                                                                                                                                 
                "OS version": "4.9",                                                                                                                                                                                                                                      
                "OS release": "not supported",                                                                                                                                                                                                                            
                "OS build": "not supported",                                                                                                                                                                                                                              
                "Native OS": "Unix",                                                                                                                                                                                                                                      
                "Native LAN manager": "Samba 3.0.20-Debian",                                                                                                                                                                                                              
                "Platform id": "500",                                                                                                                                                                                                                                     
                "Server type": "0x9a03",                                                                                                                                                                                                                                  
                "Server type string": "Wk Sv PrQ Unx NT SNT metasploitable server (Samba 3.0.20-Debian)"                                                                                                                                                                  
            """
            os_os = str(enum_smb['os_info']['OS'])
            os_version = str(enum_smb['os_info']['OS version'])
            os_release = str(enum_smb['os_info']['OS release'])
            os_build = str(enum_smb['os_info']['OS build'])
            os_native = str(enum_smb['os_info']['Native OS'])
            os_lan_manager_native = str(enum_smb['os_info']['Native LAN manager'])
            os_platform_id = str(enum_smb['os_info']['Platform id'])
            os_server_type = str(enum_smb['os_info']['Server type'])
            os_server_type_string = str(enum_smb['os_info']['Server type string'])

            """                                                                                                                                                                                                                                                           
            "users": {                                                                                                                                                                                                                                                    
                "1010": {                                                                                                                                                                                                                                                 
                    "username": "games",                                                                                                                                                                                                                                  
                    "name": "games",                                                                                                                                                                                                                                      
                    "acb": "0x00000011",                                                                                                                                                                                                                                  
                    "description": "(null)"                                                                                                                                                                                                                               
            """
            for user in enum_smb['users']:
                users_username = str(enum_smb['users'][user]['username'])
                users_name = str(enum_smb['users'][user]['name'])
                users_acb = str(enum_smb['users'][user]['acb'])
                users_description = str(enum_smb['users'][user]['description'])

                # insert user in db

                sql_insert_users = """INSERT INTO `smb_user` (`id_smb_user`, `job`, `host`, `id_smb_enum`, `username`, `name`, `acb`, `description`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);"""
                input_data = (job, target, start_job, users_username, users_name, users_acb, users_description)

                enumDB.execute(sql_insert_users, input_data)
                connDB.commit()

            """                                                                                                                                                                                                                                                           
            "groups": {},                                                                                                                                                                                                                                                 
            """
            groups = str(enum_smb['groups'])

            """                                                                                                                                                                                                                                                           
            "shares": {                                                                                                                                                                                                                                                   
                "print$": {                                                                                                                                                                                                                                               
                    "type": "Disk",                                                                                                                                                                                                                                       
                    "comment": "Printer Drivers",                                                                                                                                                                                                                         
                    "access": {                                                                                                                                                                                                                                           
                        "mapping": "denied",                                                                                                                                                                                                                              
                        "listing": "n/a"                                                                                                                                                                                                                                  
                    }                                                                                                                                                                                                                                                     
            """

            name_share = list(enum_smb['shares'].keys())
            print(len(name_share))
            for item in name_share:

                nome_condivisione = item
                print(nome_condivisione)

                try:
                    share_type = str(enum_smb['shares'][item]['type'])
                    print(share_type)
                except:
                    share_type = ''

                try:
                    share_comment = str(enum_smb['shares'][item]['comment'])
                    print(share_comment)
                except:
                    share_comment = ''
                try:
                    share_mapping = str(enum_smb['shares'][item]['access']['mapping'])
                    print(share_mapping)
                except:
                    share_mapping = ''
                try:
                    share_listing = str(enum_smb['shares'][item]['access']['listing'])
                    print(share_listing)
                except:
                    share_listing = ''
                # insert share in db

                sql_insert_share = """INSERT INTO `smb_share` (`id_smb_share`, `job`, `host`, `id_smb_enum`, nome_condivisione ,`type`, `comment`, `mapping`, `listing`) VALUES (NULL, %s, %s, %s, %s, %s,%s, %s, %s);"""
                input_data = (job, target, start_job, nome_condivisione, share_type, share_comment, share_mapping, share_listing)

                enumDB.execute(sql_insert_share, input_data)
                connDB.commit()


            """                                                                                                                                                                                                                                                           
            "policy": {                                                                                                                                                                                                                                                   
                "Domain password information": {                                                                                                                                                                                                                          
                    "Password history length": "None",                                                                                                                                                                                                                    
                    "Minimum password length": 5,                                                                                                                                                                                                                         
                    "Maximum password age": "not set",                                                                                                                                                                                                                    
                    "Password properties": [                                                                                                                                                                                                                              
                        {                                                                                                                                                                                                                                                 
                            "DOMAIN_PASSWORD_COMPLEX": false                                                                                                                                                                                                              
                        },                                                                                                                                                                                                                                                
                        {                                                                                                                                                                                                                                                 
                            "DOMAIN_PASSWORD_NO_ANON_CHANGE": false                                                                                                                                                                                                       
                        },                                                                                                                                                                                                                                                
                        {                                                                                                                                                                                                                                                 
                            "DOMAIN_PASSWORD_NO_CLEAR_CHANGE": false                                                                                                                                                                                                      
                        },                                                                                                                                                                                                                                                
                        {                                                                                                                                                                                                                                                 
                            "DOMAIN_PASSWORD_LOCKOUT_ADMINS": false                                                                                                                                                                                                       
                        },                                                                                                                                                                                                                                                
                        {                                                                                                                                                                                                                                                 
                            "DOMAIN_PASSWORD_PASSWORD_STORE_CLEARTEXT": false                                                                                                                                                                                             
                        },                                                                                                                                                                                                                                                
                        {                                                                                                                                                                                                                                                 
                            "DOMAIN_PASSWORD_REFUSE_PASSWORD_CHANGE": false                                                                                                                                                                                               
                        }                                                                                                                                                                                                                                                 
                    ]                                                                                                                                                                                                                                                     
                },                                                                                                                                                                                                                                                        
                "Domain lockout information": {                                                                                                                                                                                                                           
                    "Lockout observation window": "30 minutes",                                                                                                                                                                                                           
                    "Lockout duration": "30 minutes",                                                                                                                                                                                                                     
                    "Lockout threshold": "None"                                                                                                                                                                                                                           
                },                                                                                                                                                                                                                                                        
                "Domain logoff information": {                                                                                                                                                                                                                            
                    "Force logoff time": "not set"                                                                                                                                                                                                                        
                }                                                                                                                                                                                                                                                         

            """
            policy_password_history_length = str(enum_smb['policy']['Domain password information'][
                                                     'Password history length'])
            policy_minimun_password_length = str(enum_smb['policy']['Domain password information'][
                                                     'Minimum password length'])
            policy_maximun_password_age = str(enum_smb['policy']['Domain password information']['Maximum password age'])

            domain_pass_complex = str(enum_smb['policy']['Domain password information']['Password properties'][0])

            domain_pass_no_anon_change = str(
                enum_smb['policy']['Domain password information']['Password properties'][1])
            domain_pass_no_clear_change = str(
                enum_smb['policy']['Domain password information']['Password properties'][2])
            domain_pass_lockhout_admins = str(
                enum_smb['policy']['Domain password information']['Password properties'][3])
            domain_pass_store_cleartext = str(
                enum_smb['policy']['Domain password information']['Password properties'][4])
            domain_password_refuse_change = str(
                enum_smb['policy']['Domain password information']['Password properties'][5])
            # insert password rules in db

            sql_insert_password_rules = """INSERT INTO `smb_password_rules` (`id_smb_password_rules`, `job`, `host`, `id_smb_enum`, `domain_pass_complex`, `domain_pass_no_anon_change`, `domain_pass_no_clear_change`, `domain_pass_lockhout_admins`, `domain_pass_store_cleartext`, `domain_password_refuse_change`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            input_data = (
            job, target, start_job, domain_pass_complex, domain_pass_no_anon_change, domain_pass_no_clear_change,
            domain_pass_lockhout_admins, domain_pass_store_cleartext, domain_password_refuse_change)

            enumDB.execute(sql_insert_password_rules, input_data)
            connDB.commit()

            policy_lockout_observation_window = str(enum_smb['policy']['Domain lockout information'][
                                                        'Lockout observation window'])
            policy_lockout_duration = str(enum_smb['policy']['Domain lockout information']['Lockout duration'])
            policy_lockout_threshold = str(enum_smb['policy']['Domain lockout information']['Lockout threshold'])
            policy_force_logoff_time = str(enum_smb['policy']['Domain logoff information']['Force logoff time'])

            """                                                                                                                                                                                                                                                           
            "printers": {},                                                                                                                                                                                                                                               
            "errors": {                                                                                                                                                                                                                                                   
                "services": {                                                                                                                                                                                                                                             
                    "enum_services": [                                                                                                                                                                                                                                    
                        "Could not connect to LDAP on 389/tcp: connection refused",                                                                                                                                                                                       
                        "Could not connect to LDAPS on 636/tcp: connection refused"                                                                                                                                                                                       
                    ]                                                                                                                                                                                                                                                     
                },                                                                                                                                                                                                                                                        
                "sessions": {                                                                                                                                                                                                                                             
                    "enum_sessions": [                                                                                                                                                                                                                                    
                        "Could not establish random user session: STATUS_LOGON_FAILURE"                                                                                                                                                                                   
                    ]                                                                                                                                                                                                                                                     
            """
            printers_enum = str(enum_smb['printers'])

            for i in range(len(enum_smb['errors']['services']['enum_services'])):
                errors_enum_services = str(enum_smb['errors']["services"]['enum_services'][i])

                # insert error service in db

                sql_insert_error = """INSERT INTO `smb_errors` (`id_smb_error`, `job`, `host`, `id_smb_enum`, `services`, `sessions`) VALUES (NULL, %s, %s, %s, %s, NULL);"""
                input_data = (job, target, start_job, errors_enum_services)

                enumDB.execute(sql_insert_error, input_data)
                connDB.commit()

            try:
                for i in range(len(enum_smb['errors']['sessions']['enum_sessions'])):
                    error_enum_sessions = str(enum_smb['errors']['sessions']['enum_sessions'][i])

                    # insert error sessions in db
                    sql_insert_error = """INSERT INTO `smb_errors` (`id_smb_error`, `job`, `host`, `id_smb_enum`, `services`, `sessions`) VALUES (NULL, %s, %s, %s, NULL, %s);"""
                    input_data = (job, target, start_job, error_enum_sessions)

                    enumDB.execute(sql_insert_error, input_data)
                    connDB.commit()
            except:
                print("no sessions errors")


            # prepara la query

            sql_insert_enum_query = """INSERT INTO `smb_enum`(`id_smb_enum`, `job`, `host`, `user`, `ldap`, `samba`, `dominio`, `netbios_computer_name`,                                                                                                                       
                                                                                               `netbios_domain_name`, `dns_domain`, `fqdn`, `derived_membership`, `derived_domain`, `sessions_possible`,                                                                  
                                                                                               `sessions_null`, `sessions_password`, `sessions_kerberos`, `sessions_nthash`, `sessions_random_user`,                                                                      
                                                                                               `rpc_domain`, `rpc_domain_sid`, `rpc_membership`, `os`, `os_version`, `os_release`, `os_build`,                                                                            
                                                                                               `native_os`, `native_lan_manager`, `platform_id`, `server_type`, `server_type_sring`, `domain_group`,                                                                      
                                                                                               `policy_password_history_length`, `policy_minimum_password_length`, `policy_maximum_password_age`,                                                                         
                                                                                               `policy_lockout_observation_window`, `policy_lockout_duration`, `policy_lockout_threshold`,                                                                                
                                                                                               `policy_force_logoff_time`, `printers`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,               
                                                                                           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            # dati per la query

            input_data = (
            start_job, job, target, credential, ldap, samba, dominio, computer_name, domain_name, dns_domain, fqdn,
            derived_membership, derived_domain, sessions_possible, sessions_null, sessions_password,
            sessions_kerberos, sessions_nthash, sessions_random_user, rpc_domain, rpc_domain_sid,
            rpc_membership, os_os, os_version, os_release, os_build, os_native, os_lan_manager_native,
            os_platform_id, os_server_type, os_server_type_string, groups, policy_password_history_length,
            policy_minimun_password_length, policy_maximun_password_age,
            policy_lockout_observation_window, policy_lockout_duration,
            policy_lockout_threshold, policy_force_logoff_time, printers_enum)

            # invia query

            enumDB.execute(sql_insert_enum_query, input_data)
            connDB.commit()

        enumDB.close()
        connDB.close()
