#!/usr/bin/bash
./inizializzazione_engine.py

gnome-terminal -- ./crea_token.py
gnome-terminal -- ./WebScanner_engine.py

gnome-terminal -- sudo ./Defensio_engine.py

gnome-terminal -- sudo ./Openvas_engine.py

gnome-terminal -- sudo ./ShareScanner_engine.py

