#!/usr/bin/env python3
import os
import signal
import subprocess
from flask import Flask, render_template,send_file, request
from flask_socketio import SocketIO


app = Flask(__name__, template_folder='./')
socketio = SocketIO(app)


@app.route('/status')
def status():
    ids_engine = os.popen("pgrep -fx \"python3 ./IDS.py\"").read()
    if ids_engine == '':
        ids_token = "Disattivato"
        ids_status = "Non attivo"
        return ids_status
    else:
        ids_token = "Attivato"
        ids_status = "Attivo con PID: " + str(ids_engine)
        return ids_status

@app.route('/status_suricata')
def is_suricata_active():
    # Esegui il comando systemctl status suricata
    result = subprocess.run(['systemctl', 'status', 'suricata'], stdout=subprocess.PIPE)

    # Analizza l'output per determinare lo stato del servizio
    output = result.stdout.decode('utf-8')
    if 'Active: active' in output:
        suricata_active = "Attivo";
        return suricata_active
    else:
        suricata_active = "Non attivo";
        return suricata_active

@app.route('/start_suricata')
def start_suricata():
    # Esegui il comando systemctl status suricata
    subprocess.run(['systemctl', 'start', 'suricata'])

    return index()

@app.route('/stop_suricata')
def stop_suricata():
    # Esegui il comando systemctl status suricata
    subprocess.run(['systemctl', 'stop', 'suricata'])

    return index()

@app.route('/')
def index():

    return render_template('./web_c2.html')


@app.route('/eng_conf.json')
def test():
    return send_file('eng_conf.json', mimetype='text/plain')


@app.route('/start')
def start():
    ids_engine = os.popen("pgrep -fx \"python3 ./IDS.py\"").read()
    index()
    if ids_engine == '':
        # Avvia il processo IDS e salva l'oggetto Popen in una variabile
        ids_process = subprocess.Popen(["sudo", "python3", "./IDS.py"], stdout=subprocess.PIPE)

        # Invia i messaggi del processo IDS al browser utilizzando SocketIO
        @socketio.on('message')
        def handle_message(message):
            socketio.send(message)

        # Leggi i messaggi del processo IDS in tempo reale e inviali al browser
        while True:
            output = ids_process.stdout.readline()
            if not output:
                break
            socketio.emit('message', output.decode())

    return index()

@app.route('/stop')
def stop():
    ids_engine = os.popen("pgrep -fx \"python3 ./IDS.py\"").read()
    if ids_engine != '':
        ids_engine = int(ids_engine)
        os.kill(ids_engine, signal.SIGKILL)
    return index()

if __name__ == '__main__':
    app.run(debug=True)
