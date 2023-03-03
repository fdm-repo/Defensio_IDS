#!/usr/bin/env python3
# Module Imports
import json
import crealog
import DB_connect

idprocess = "enum4linux_read_json"
class enum4linux_read_json_class:

    def enum4linux_read_json(self, job_enum, start_job, file_json, start_scan):

        # Database connection
        try:

            connessione = DB_connect.database_connect()
            connDB = connessione.database_connection()
            enumDB = connDB.cursor()
        except:
            print("enum4linux: errore connessione database")

            log = crealog.log_event()
            log.crealog(idprocess,
                        "ERRORE connessione aal database non riuscita")

        job = job_enum
        start_job = start_job
        file_json = file_json
        start_scan = start_scan

        log = crealog.log_event()
        log.crealog(idprocess,
                    "Apertura del file "+str(file_json)+" relativo al Job "+str(job)+" avviato alle "+str(start_job))

        with open(file_json, 'r') as json_file:
            enum_smb = json.load(json_file)
            try:
                target = str(enum_smb['target']['host'])
            except:
                print("no target value")
                target = ''
            try:
                credential = str(enum_smb['credentials']['user'])
            except:
                print("no credential value")
                credential = ''
            try:
                ldap = str(enum_smb['services']['LDAP']['accessible'])
            except:
                print("no ldap accessible")
                ldap = ''
            try:
                samba = str(enum_smb['services']['SMB']['accessible'])
            except:
                print("no samba service")
                samba = ''
            try:
                dominio = str(enum_smb['domain'])
            except:
                print("no domain accessible")
                dominio = ''

            try:
                for i in range(len(enum_smb['nmblookup'])):
                    nmblookup = enum_smb['nmblookup'][i]
            except:
                print(" no nmblookup disponibile")
                nmblookup = ''

            """                                                                                                                                                                                                                                                           
            "smb_domain_info": {                                                                                                                                                                                                                                          
                "NetBIOS computer name": "METASPLOITABLE",                                                                                                                                                                                                                
                "NetBIOS domain name": "",                                                                                                                                                                                                                                
                "DNS domain": "localdomain",                                                                                                                                                                                                                              
                "FQDN": "metasploitable.localdomain",                                                                                                                                                                                                                     
                "Derived membership": "workgroup member",                                                                                                                                                                                                                 
                "Derived domain": "unknown"                                                                                                                                                                                                                               
            """
            try:
                computer_name = str(enum_smb['smb_domain_info']['NetBIOS computer name'])
            except:
                print("no computer name")
                computer_name = ''
            try:
                domain_name = str(enum_smb['smb_domain_info']['NetBIOS domain name'])
            except:
                print("no domain name")
                domain_name = ''
            try:
                dns_domain = str(enum_smb['smb_domain_info']['DNS domain'])
            except:
                print("no dns domain info")
                dns_domain = ''
            try:
                fqdn = str(enum_smb['smb_domain_info']['FQDN'])
            except:
                print("no fqdn value")
                fqdn = ''
            try:
                derived_membership = str(enum_smb['smb_domain_info']['Derived membership'])
            except:
                print("no derived membership value")
                derived_membership = ''
            try:
                derived_domain = str(enum_smb['smb_domain_info']['Derived domain'])
            except:
                print("no derived domain")
                derived_domain = ''

            """                                                                                                                                                                                                                                                           
            "sessions": {                                                                                                                                                                                                                                                 
                "sessions_possible": true,                                                                                                                                                                                                                                
                "null": true,                                                                                                                                                                                                                                             
                "password": false,                                                                                                                                                                                                                                        
                "kerberos": false,                                                                                                                                                                                                                                        
                "nthash": false,                                                                                                                                                                                                                                          
                "random_user": false                                                                                                                                                                                                                                      


            """
            try:
                sessions_possible = str(enum_smb['sessions']['sessions_possible'])
            except:
                print(" no sessions possible value")
                sessions_possible = ''
            try:
                sessions_null = str(enum_smb['sessions']['null'])
            except:
                print("no sessions null value")
                sessions_null = ''
            try:
                sessions_password = str(enum_smb['sessions']['password'])
            except:
                print("no sessions password value")
                sessions_password = ''
            try:
                sessions_kerberos = str(enum_smb['sessions']['kerberos'])
            except:
                print(" no sessions kerberos value")
                sessions_kerberos = ''
            try:
                sessions_nthash = str(enum_smb['sessions']['nthash'])
            except:
                print(" no sessions nthash value")
                sessions_nthash = ''
            try:
                sessions_random_user = str(enum_smb['sessions']['random_user'])
            except:
                print(" no random user value")
                sessions_random_user = ''

            """                                                                                                                                                                                                                                                           
            "rpc_domain_info": {                                                                                                                                                                                                                                          
                "Domain": "WORKGROUP",                                                                                                                                                                                                                                    
                "Domain SID": "NULL SID",                                                                                                                                                                                                                                 
                "Membership": "workgroup member"                                                                                                                                                                                                                          
            """
            try:
                rpc_domain = str(enum_smb['rpc_domain_info']['Domain'])
            except:
                print("no rpc domain value")
                rpc_domain = ''
            try:
                rpc_domain_sid = str(enum_smb['rpc_domain_info']['Domain SID'])
            except:
                print(" no rpc SID domain value")
                rpc_domain_sid = ''
            try:
                rpc_membership = str(enum_smb['rpc_domain_info']['Membership'])
            except:
                print("no rpc domain info value")
                rpc_membership = ''

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
            try:
                os_os = str(enum_smb['os_info']['OS'])
            except:
                print("no os info value")
                os_os = ''
            try:
                os_version = str(enum_smb['os_info']['OS version'])
            except:
                print(" no os version value")
                os_version = ''
            try:
                os_release = str(enum_smb['os_info']['OS release'])
            except:
                print(" no os release value")
                os_release = ''
            try:
                os_build = str(enum_smb['os_info']['OS build'])
            except:
                print(" no os build value")
                os_build = ''
            try:
                os_native = str(enum_smb['os_info']['Native OS'])
            except:
                print("no os native value")
                os_native = ''
            try:
                os_lan_manager_native = str(enum_smb['os_info']['Native LAN manager'])
            except:
                print("no native la manager value")
                os_lan_manager_native = ''
            try:
                os_platform_id = str(enum_smb['os_info']['Platform id'])
            except:
                print(" no os platform id value")
                os_platform_id = ''
            try:
                os_server_type = str(enum_smb['os_info']['Server type'])
            except:
                print("no server type value")
                os_server_type = ''
            try:
                os_server_type_string = str(enum_smb['os_info']['Server type string'])
            except:
                print("no server type string value")
                os_server_type_string = ''
            """                                                                                                                                                                                                                                                           
            "users": {                                                                                                                                                                                                                                                    
                "1010": {                                                                                                                                                                                                                                                 
                    "username": "games",                                                                                                                                                                                                                                  
                    "name": "games",                                                                                                                                                                                                                                      
                    "acb": "0x00000011",                                                                                                                                                                                                                                  
                    "description": "(null)"                                                                                                                                                                                                                               
            """
            try:
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



            except:
                print("no smb users")

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Inserimento dei risultati nella tabella smb_user")

            """                                                                                                                                                                                                                                                           
            "groups": {},                                                                                                                                                                                                                                                 
            """
            try:
                groups = str(enum_smb['groups'])
            except:
                print("no group value")
                groups = ''

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
            try:
                name_share = list(enum_smb['shares'].keys())
                print(len(name_share))
            except:
                print(" no share value")
                name_share = ''
            try:
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
                    input_data = (
                        job, target, start_job, nome_condivisione, share_type, share_comment, share_mapping,
                        share_listing)

                    enumDB.execute(sql_insert_share, input_data)
                    connDB.commit()



            except:
                print("no share value")

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Inserimento dei risultati nella tabella smb_share")

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
            try:
                policy_password_history_length = str(enum_smb['policy']['Domain password information'][
                                                         'Password history length'])
            except:
                print(" no policy password history length value")
                policy_password_history_length = ''
            try:
                policy_minimun_password_length = str(enum_smb['policy']['Domain password information'][
                                                         'Minimum password length'])
            except:
                print("no policy minimun password length value")
                policy_minimun_password_length = ''
            try:
                policy_maximun_password_age = str(
                    enum_smb['policy']['Domain password information']['Maximum password age'])
            except:
                print(" no policy maximun password age")
                policy_maximun_password_age = ''
            try:
                domain_pass_complex = str(enum_smb['policy']['Domain password information']['Password properties'][0])
            except:
                print(" no domain pass complex value")
                domain_pass_complex = ''

            try:
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
            except:
                print(" no policies domain values")

            # insert password rules in db
            try:
                sql_insert_password_rules = """INSERT INTO `smb_password_rules` (`id_smb_password_rules`, `job`, `host`, `id_smb_enum`, `domain_pass_complex`, `domain_pass_no_anon_change`, `domain_pass_no_clear_change`, `domain_pass_lockhout_admins`, `domain_pass_store_cleartext`, `domain_password_refuse_change`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                input_data = (
                    job, target, start_job, domain_pass_complex, domain_pass_no_anon_change,
                    domain_pass_no_clear_change,
                    domain_pass_lockhout_admins, domain_pass_store_cleartext, domain_password_refuse_change)

                enumDB.execute(sql_insert_password_rules, input_data)
                connDB.commit()
            except:
                print(" no update DB value smb_password_rules")

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Inserimento dei risultati nella tabella smb_password_rules")


            try:
                policy_lockout_observation_window = str(enum_smb['policy']['Domain lockout information'][
                                                            'Lockout observation window'])
            except:
                print("no policy lockout observation values")
                policy_lockout_observation_window = ''
            try:
                policy_lockout_duration = str(enum_smb['policy']['Domain lockout information']['Lockout duration'])
            except:
                print(" no policy lockout duration")
                policy_lockout_duration = ''
            try:
                policy_lockout_threshold = str(enum_smb['policy']['Domain lockout information']['Lockout threshold'])
            except:
                print(" no polyci lockout threshold")
                policy_lockout_threshold = ''
            try:
                policy_force_logoff_time = str(enum_smb['policy']['Domain logoff information']['Force logoff time'])
            except:
                print("no policy force logoff time")
                policy_force_logoff_time = ''

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
            try:
                printers_enum = str(enum_smb['printers'])
            except:
                print("no printers value")
                printers_enum = ''

            try:
                for i in range(len(enum_smb['errors']['services']['enum_services'])):
                    errors_enum_services = str(enum_smb['errors']["services"]['enum_services'][i])

                    # insert error service in db

                    sql_insert_error = """INSERT INTO `smb_errors` (`id_smb_error`, `job`, `host`, `id_smb_enum`, `services`, `sessions`) VALUES (NULL, %s, %s, %s, %s, NULL);"""
                    input_data = (job, target, start_job, errors_enum_services)

                    enumDB.execute(sql_insert_error, input_data)
                    connDB.commit()
            except:
                print(" no errors services value")

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Inserimento dei risultati nella tabella smb_error")


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

            log = crealog.log_event()
            log.crealog(idprocess,
                        "Inserimento dei risultati nella tabella smb_error")

            # prepara la query

            sql_insert_enum_query = """INSERT INTO `smb_enum`(`id_smb_enum`, `job`, `host`, `user`, `ldap`, `samba`, `dominio`, `netbios_computer_name`,                                                                                                                       
                                                                                               `netbios_domain_name`, `dns_domain`, `fqdn`, `derived_membership`, `derived_domain`, `sessions_possible`,                                                                  
                                                                                               `sessions_null`, `sessions_password`, `sessions_kerberos`, `sessions_nthash`, `sessions_random_user`,                                                                      
                                                                                               `rpc_domain`, `rpc_domain_sid`, `rpc_membership`, `os`, `os_version`, `os_release`, `os_build`,                                                                            
                                                                                               `native_os`, `native_lan_manager`, `platform_id`, `server_type`, `server_type_sring`, `domain_group`,                                                                      
                                                                                               `policy_password_history_length`, `policy_minimum_password_length`, `policy_maximum_password_age`,                                                                         
                                                                                               `policy_lockout_observation_window`, `policy_lockout_duration`, `policy_lockout_threshold`,                                                                                
                                                                                               `policy_force_logoff_time`, `printers` , `start_scan`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,               
                                                                                           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            # dati per la query

            input_data = (
                start_job, job, target, credential, ldap, samba, dominio, computer_name, domain_name, dns_domain, fqdn,
                derived_membership, derived_domain, sessions_possible, sessions_null, sessions_password,
                sessions_kerberos, sessions_nthash, sessions_random_user, rpc_domain, rpc_domain_sid,
                rpc_membership, os_os, os_version, os_release, os_build, os_native, os_lan_manager_native,
                os_platform_id, os_server_type, os_server_type_string, groups, policy_password_history_length,
                policy_minimun_password_length, policy_maximun_password_age,
                policy_lockout_observation_window, policy_lockout_duration,
                policy_lockout_threshold, policy_force_logoff_time, printers_enum, start_scan)

            # invia query

            enumDB.execute(sql_insert_enum_query, input_data)
            connDB.commit()
            log = crealog.log_event()
            log.crealog(idprocess,
                        "Inserimento dei risultati nella tabella smb_enum")
        enumDB.close()
        connDB.close()
