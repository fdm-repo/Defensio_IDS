#!/usr/bin/bash
./inizializzazione_engine.py

gnome-terminal -- ./crea_token.py

gnome-terminal -- ./Defensio_engine.py

gnome-terminal -- ./Openvas_engine.py

gnome-terminal -- ./ShareScanner_engine.py

gnome-terminal -- ./WebScanner_engine.py