#!/usr/bin/env python3
# Module Imports
import sys
import time
from datetime import datetime
import arachni
import DB_connect
import mariadb
import nmap
import json
import re




class enum4linux_read_json:

    def enum4linux_read_json(self, job_enum, file_json):
        job = job_enum
        with open(file_json, 'r') as json_file:
            enum_smb = json.load(json_file)
            target = enum_smb['target']['host']
            credential = enum_smb['credentials']['user']
            ldap = str(enum_smb['services']['LDAP']['accessible'])
            samba = str(enum_smb['services']['SMB']['accessible'])
            dominio = enum_smb['domain']

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
            computer_name = enum_smb['smb_domain_info']['NetBIOS computer name']
            domain_name = enum_smb['smb_domain_info']['NetBIOS domain name']
            dns_domain = enum_smb['smb_domain_info']['DNS domain']
            fqdn = enum_smb['smb_domain_info']['FQDN']
            derived_membership = enum_smb['smb_domain_info']['Derived membership']
            derived_domain = enum_smb['smb_domain_info']['Derived domain']




            """
            "sessions": {
                "sessions_possible": true,
                "null": true,
                "password": false,
                "kerberos": false,
                "nthash": false,
                "random_user": false


            """
            sessions_possible = enum_smb['sessions']['sessions_possible']
            sessions_null = enum_smb['sessions']['null']
            sessions_password = enum_smb['sessions']['password']
            sessions_kerberos = enum_smb['sessions']['kerberos']
            sessions_nthash = enum_smb['sessions']['nthash']
            sessions_random_user = enum_smb['sessions']['random_user']



            """
            "rpc_domain_info": {
                "Domain": "WORKGROUP",
                "Domain SID": "NULL SID",
                "Membership": "workgroup member"
            """
            rpc_domain = enum_smb['rpc_domain_info']['Domain']
            rpc_domain_sid = enum_smb['rpc_domain_info']['Domain SID']
            rpc_membership = enum_smb['rpc_domain_info']['Membership']


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
            os_os = enum_smb['os_info']['OS']
            os_version = enum_smb['os_info']['OS version']
            os_release = enum_smb['os_info']['OS release']
            os_build = enum_smb['os_info']['OS build']
            os_native = enum_smb['os_info']['Native OS']
            os_lan_manager_native = enum_smb['os_info']['Native LAN manager']
            os_platform_id = enum_smb['os_info']['Platform id']
            os_server_type = enum_smb['os_info']['Server type']
            os_server_type_string = enum_smb['os_info']['Server type string']



            """
            "users": {
                "1010": {
                    "username": "games",
                    "name": "games",
                    "acb": "0x00000011",
                    "description": "(null)"
            """
            for user in enum_smb['users']:
                users_username = enum_smb['users'][user]['username']
                users_name = enum_smb['users'][user]['name']
                users_acb = enum_smb['users'][user]['acb']
                users_description = enum_smb['users'][user]['description']

            """
            "groups": {},
            """
            groups = enum_smb['groups']

            sql_update_query = """INSERT INTO `smb_enum`(`id_smb_enum`, `job`, `host`, `user`, `ldap`, `samba`, `dominio`, `netbios_computer_name`,
                                                                                   `netbios_domain_name`, `dns_domain`, `fqdn`, `derived_membership`, `derived_domain`, `sessions_possible`,
                                                                                   `sessions_null`, `sessions_password`, `sessions_kerberos`, `sessions_nthash`, `sessions_random_user`,
                                                                                   `rpc_domain`, `rpc_domain_sid`, `rpc_membership`, `os`, `os_version`, `os_release`, `os_build`,
                                                                                   `native_os`, `native_lan_manager`, `platform_id`, `server_type`, `server_type_sring`, `domain_group`,
                                                                                   `policy_password_history_length`, `policy_minimum_password_length`, `policy_maximum_password_age`,
                                                                                   `policy_lockout_observation_window`, `policy_lockout_duration`, `policy_lockout_threshold`,
                                                                                   `policy_force_logoff_time`, `printers`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                                               %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            input_data = (job, target, credential, ldap, samba, dominio, computer_name, domain_name, dns_domain, fqdn,
                          derived_membership, derived_domain, sessions_possible, sessions_null, sessions_password,
                          sessions_kerberos, sessions_nthash, sessions_random_user, rpc_domain, rpc_domain_sid,
                          rpc_membership, os_os, os_version, os_release, os_build, os_native, os_lan_manager_native, os_platform_id, os_server_type, os_server_type_string, groups, )

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
            for share in enum_smb['shares']:
                share_type = enum_smb['shares'][share]['type']
                share_comment = enum_smb['shares'][share]['comment']
                share_mapping = enum_smb['shares'][share]['access']['mapping']
                share_listing = enum_smb['shares'][share]['access']['listing']

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
            policy_password_history_length = enum_smb['policy']['Domain password information'][
                'Password history length']
            policy_minimun_password_length = enum_smb['policy']['Domain password information'][
                'Minimum password length']
            policy_maximun_password_age = enum_smb['policy']['Domain password information']['Maximum password age']
            for i in range(5):
                policy_password_properties = enum_smb['policy']['Domain password information']['Password properties'][i]

            policy_lockout_observation_window = enum_smb['policy']['Domain lockout information'][
                'Lockout observation window']
            policy_lockout_duration = enum_smb['policy']['Domain lockout information']['Lockout duration']
            policy_lockout_threshold = enum_smb['policy']['Domain lockout information']['Lockout threshold']
            policy_force_logoff_time = enum_smb['policy']['Domain logoff information']['Force logoff time']

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
            printers_enum = enum_smb['printers']

            for i in range(len(enum_smb['errors']['services']['enum_services'])):
                errors_enum_services = enum_smb['errors']["services"]['enum_services'][i]

            for i in range(len(enum_smb['errors']['sessions']['enum_sessions'])):
                error_enum_sessions = enum_smb['errors']['sessions']['enum_sessions'][i]

            sql_update_query = """INSERT INTO `smb_enum`(`id_smb_enum`, `job`, `host`, `user`, `ldap`, `samba`, `dominio`, `netbios_computer_name`,
                                                                                               `netbios_domain_name`, `dns_domain`, `fqdn`, `derived_membership`, `derived_domain`, `sessions_possible`,
                                                                                               `sessions_null`, `sessions_password`, `sessions_kerberos`, `sessions_nthash`, `sessions_random_user`,
                                                                                               `rpc_domain`, `rpc_domain_sid`, `rpc_membership`, `os`, `os_version`, `os_release`, `os_build`,
                                                                                               `native_os`, `native_lan_manager`, `platform_id`, `server_type`, `server_type_sring`, `domain_group`,
                                                                                               `policy_password_history_length`, `policy_minimum_password_length`, `policy_maximum_password_age`,
                                                                                               `policy_lockout_observation_window`, `policy_lockout_duration`, `policy_lockout_threshold`,
                                                                                               `policy_force_logoff_time`, `printers`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                                                                           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            input_data = (job, target, credential, ldap, samba, dominio, computer_name, domain_name, dns_domain, fqdn,
                          derived_membership, derived_domain, sessions_possible, sessions_null, sessions_password,
                          sessions_kerberos, sessions_nthash, sessions_random_user, rpc_domain, rpc_domain_sid,
                          rpc_membership, os_os, os_version, os_release, os_build, os_native, os_lan_manager_native,
                          os_platform_id, os_server_type, os_server_type_string, groups, policy_password_history_length,
                          policy_minimun_password_length, policy_maximun_password_age,
                          policy_lockout_observation_window, policy_lockout_duration, policy_lockout_duration,
                          policy_lockout_threshold, policy_force_logoff_time,printers_enum)