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




with open('porcofile.json', 'r') as fcc_file:
    prova = json.load(fcc_file)
    print(prova)
    print('target '+prova['target']['host'])
    print('user '+prova['credentials']['user'])
    print('LDAP Accessibile '+str(prova['services']['LDAP']['accessible']))
    print('SAMBA Accessibile '+str(prova['services']['SMB']['accessible']))
    print('Dominio '+prova['domain'])

    for i in range(len(prova['nmblookup'])):
        print(prova['nmblookup'][i])


    """
    "smb_domain_info": {
        "NetBIOS computer name": "METASPLOITABLE",
        "NetBIOS domain name": "",
        "DNS domain": "localdomain",
        "FQDN": "metasploitable.localdomain",
        "Derived membership": "workgroup member",
        "Derived domain": "unknown"
    """
    print(prova['smb_domain_info']['NetBIOS computer name'])
    print(prova['smb_domain_info']['NetBIOS domain name'])
    print(prova['smb_domain_info']['DNS domain'])
    print(prova['smb_domain_info']['FQDN'])
    print(prova['smb_domain_info']['Derived membership'])
    print(prova['smb_domain_info']['Derived domain'])

    """
    "sessions": {
        "sessions_possible": true,
        "null": true,
        "password": false,
        "kerberos": false,
        "nthash": false,
        "random_user": false
    
    
    """
    print(prova['sessions']['sessions_possible'])
    print(prova['sessions']['null'])
    print(prova['sessions']['password'])
    print(prova['sessions']['kerberos'])
    print(prova['sessions']['nthash'])
    print(prova['sessions']['random_user'])

    """
    "rpc_domain_info": {
        "Domain": "WORKGROUP",
        "Domain SID": "NULL SID",
        "Membership": "workgroup member"
    """
    print(prova['rpc_domain_info']['Domain'])
    print(prova['rpc_domain_info']['Domain SID'])
    print(prova['rpc_domain_info']['Membership'])

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
    print(prova['os_info']['OS'])
    print(prova['os_info']['OS version'])
    print(prova['os_info']['OS release'])
    print(prova['os_info']['OS build'])
    print(prova['os_info']['Native OS'])
    print(prova['os_info']['Native LAN manager'])
    print(prova['os_info']['Platform id'])
    print(prova['os_info']['Server type'])
    print(prova['os_info']['Server type string'])

    """
    "users": {
        "1010": {
            "username": "games",
            "name": "games",
            "acb": "0x00000011",
            "description": "(null)"
    """
    for user in prova['users']:
        print('*****************')
        print(prova['users'][user]['username'])
        print(prova['users'][user]['name'])
        print(prova['users'][user]['acb'])
        print(prova['users'][user]['description'])

    """
    "groups": {},
    """
    print(prova['groups'])

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
    for share in prova['shares']:
        print('*****************')
        print(prova['shares'][share]['type'])
        print(prova['shares'][share]['comment'])
        print(prova['shares'][share]['access']['mapping'])
        print(prova['shares'][share]['access']['listing'])

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
    print(prova['policy']['Domain password information']['Password history length'])
    print(prova['policy']['Domain password information']['Minimum password length'])
    print(prova['policy']['Domain password information']['Maximum password age'])
    for i in range(5):
        print(prova['policy']['Domain password information']['Password properties'][i])

    print(prova['policy']['Domain lockout information']['Lockout observation window'])
    print(prova['policy']['Domain lockout information']['Lockout duration'])
    print(prova['policy']['Domain lockout information']['Lockout threshold'])
    print(prova['policy']['Domain logoff information']['Force logoff time'])

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
    print(prova['printers'])

    for i in range(len(prova['errors']['services']['enum_services'])):
        print(prova['errors']["services"]['enum_services'][i])

    for i in range(len(prova['errors']['sessions']['enum_sessions'])):
        print(prova['errors']['sessions']['enum_sessions'][i])