#!/usr/bin/env python3
# Module Imports
import socket

def verifica_porta(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"La porta {port} è aperta sull'host {host}")
            sock.sendall(b"USER anonymous\r\n")
            response = sock.recv(1024)
            print(response)
        else:
            print(f"La porta {port} è chiusa sull'host {host}")
    except socket.gaierror:
        print(f"Impossibile stabilire una connessione con l'host {host}")
    finally:
        sock.close()

verifica_porta("www.google.com", 21)

