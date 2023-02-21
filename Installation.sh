#!/usr/bin/bash

echo "Install Nmap, Nikto and SmbMap\n";
sudo apt install -y docker.io dbus-x11 pip npm git nmap nikto wapiti ldap-utils polenum smbclient wget ncrack arp-scan xsltproc wkhtmltopdf libmariadb-dev ;
sudo pip install python-nmap python-libnmap pdfkit XlsxWriter json2html flask impacket xmltodict ldap3 PyYAML>=5.1;
sudo pip3 install schedule mariadb whois;
sudo npm install pwned -g;
pwned apiKey 03af89d1aa944a0d8703050f5475fcb4;

pip install python-nmap python-libnmap pdfkit XlsxWriter json2html flask impacket xmltodict ldap3 PyYAML>=5.1;
pip3 install schedule mariadb whois;

echo "\nDownload SMBmap \n";
git clone https://github.com/ShawnDEvans/smbmap.git

echo "\nDownload Arachni \n";
mkdir temp_folder;
cd temp_folder;
git clone https://github.com/n3tSh4d3/VulnWebScan.git;
cd  VulnWebScan;
cat Arachni.tar.gz.* > Arachni.tar.gz
tar -xzvf Arachni.tar.gz;
mv arachni/ ../../;
cd ../../;
sudo rm -R temp_folder/;

echo "download e start Portainer\n"
sudo docker volume create portainer_data
sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:2.9.3

echo "download  e start immauss\n"
sudo docker pull immauss/openvas
sudo docker run --detach --publish 8080:9392 -e PASSWORD="D3f3n510" --volume openvas:/data --name openvas immauss/openvas



