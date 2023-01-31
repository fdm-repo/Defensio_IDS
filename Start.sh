#!/usr/bin/bash
./inizializzazione_engine.py

gnome-terminal \
--tab --title="GenerazioneToken" -e "./crea_token.py" \
--tab --title="WebScanner" -e "./WebScanner_engine.py" \
--tab --title="Scheduling" -e "./Scheduling.py" \
--tab --title="DPI" -e "./Email_Leaks.py" \
--tab --title="NetScanner" -e "sudo ./Defensio_engine.py" \
--tab --title="VulnScan" -e "sudo ./Openvas_engine.py" \
--tab --title="ShareScan" -e "sudo ./ShareScanner_engine.py --tab"

