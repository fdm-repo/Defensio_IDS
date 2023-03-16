#!/usr/bin/bash

echo "Install Nmap, Nikto and SmbMap\n";
sudo apt install -y docker.io dbus-x11 pip npm git nmap nikto wapiti ldap-utils polenum smbclient wget ncrack arp-scan xsltproc wkhtmltopdf libmariadb-dev ;
sudo pip install flask flask-socketio python-nmap python-libnmap pdfkit XlsxWriter json2html flask impacket xmltodict ldap3 PyYAML>=5.1;
sudo pip3 install schedule mariadb whois;


pip install python-nmap python-libnmap pdfkit XlsxWriter json2html flask impacket xmltodict ldap3 PyYAML>=5.1;
pip3 install schedule mariadb whois;



