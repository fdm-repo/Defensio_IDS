#!/bin/sh

#download arachni
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

