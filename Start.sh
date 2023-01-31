#!/usr/bin/bash
echo "
 ______  _______ _______ _______ __   _ _______ _____  _____       _______ __   _  ______ _____ __   _ _______ _______
 |     \ |______ |______ |______ | \  | |______   |   |     |      |______ | \  | |  ____   |   | \  | |______ |______
 |_____/ |______ |       |______ |  \_| ______| __|__ |_____|      |______ |  \_| |_____| __|__ |  \_| |______ ______|

By FIDEM.srl
"
echo "Si deve inizializzare l'engine?"
read -p 'Y/N: ' input

if [[ $input == "Y" || $input == "y" ]]; then
    ./inizializzazione_engine.py
fi

gnome-terminal --tab --title="GenerazioneToken" -- ./crea_token.py
gnome-terminal --tab --title="WebScanner" -- ./WebScanner_engine.py
gnome-terminal --tab --title="Scheduling" -- ./Scheduling.py
gnome-terminal --tab --title="DPI" -- ./Email_Leaks.py
gnome-terminal --tab --title="NetScanner" -- sudo ./Defensio_engine.py
gnome-terminal --tab --title="VulnScan" -- sudo ./Openvas_engine.py
gnome-terminal --tab --title="ShareScan" -- sudo ./ShareScanner_engine.py

