#!/usr/bin/bash

echo "Install Nmap, Nikto and SmbMap\n";
sudo apt install -y docker.io pip npm git nmap nikto smbmap wapiti ldap-utils polenum smbclient wget ncrack arp-scan xsltproc wkhtmltopdf libmariadb-dev ;
sudo pip install python-nmap python-libnmap pdfkit XlsxWriter json2html flask impacket xmltodict ldap3 PyYAML>=5.1;
sudo pip3 install schedule mariadb whois;

pip install python-nmap python-libnmap pdfkit XlsxWriter json2html flask impacket xmltodict ldap3 PyYAML>=5.1;
pip3 install schedule mariadb whois;
npm install pwned -g

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
sudo docker run --detach --publish 8080:9392 -e PASSWORD="porcodio" --volume openvas:/data --name openvas immauss/openvas



