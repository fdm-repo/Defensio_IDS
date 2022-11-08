#!/bin/python3

# dependency check for the modules

ip = "scanme.nmap.org"

import bane

site_info = bane.info(ip, timeout=1)
print(site_info)

keys = list(site_info.keys())
print(keys)

uno = keys[0]
due = keys[1]
tre = keys[2]

print("*****************" + uno + "******************")
print(site_info[uno]["IP address"])
print(site_info[uno]["Host name"])
print(site_info[uno]["IP range"])
print(site_info[uno]["ISP"])
print(site_info[uno]["Organization"])
print(site_info[uno]["Country"])
print(site_info[uno]["Region"])
print(site_info[uno]["City"])
print(site_info[uno]["Time zone"])
print(site_info[uno]["Local time"])
print(site_info[uno]["Postal Code"])
print("*****************" + due + "******************")
print(site_info[due]["IP address"])
print(site_info[due]["Host name"])
print(site_info[due]["IP range"])
print(site_info[due]["ISP"])
print(site_info[due]["Organization"])
print(site_info[due]["Country"])
print(site_info[due]["Region"])
print(site_info[due]["City"])
print(site_info[due]["Time zone"])
print(site_info[due]["Local time"])
print(site_info[due]["Postal Code"])
print("*****************" + tre + "******************")
print(site_info[tre]["IP address"])
print(site_info[tre]["Host name"])
print(site_info[tre]["IP range"])
print(site_info[tre]["ISP"])
print(site_info[tre]["Organization"])
print(site_info[tre]["Country"])
print(site_info[tre]["Region"])
print(site_info[tre]["City"])
print(site_info[tre]["Time zone"])
print(site_info[tre]["Local time"])
print(site_info[tre]["Postal Code"])

whois = bane.whois(ip)

print(whois)


link = "http://nmap.org/"

link_pages = bane.crawl(link, timeout=10)

print(link_pages)

from badpy import * # importing badpy module

print(locate("185.245.183.75","operator"))


