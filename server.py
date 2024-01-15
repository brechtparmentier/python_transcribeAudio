# server.py

from flask import Flask, render_template, jsonify
from flask import request
import signal
import sys
from shared import get_socketio
import threading
import json
from speech_recognition_thread import start_spraakherkenning, woorden_teller, laatste_tekst
 

app = Flask(__name__)
socketio = get_socketio()
socketio.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tellers')
def get_tellers():
    return jsonify(woorden_teller)

@app.route('/laatste_tekst')
def get_laatste_tekst():
    return jsonify({"laatsteTekst": laatste_tekst})

# Voeg een functie toe om updates naar de client te sturen
def send_update(laatste_tekst):
    socketio.emit('update', {'laatsteTekst': laatste_tekst})

def stop_server():
    print("Type 'exit' om de server te stoppen.")
    while True:
        command = input()
        if command == 'exit':
            socketio.stop()
            print("Server gestopt.")
    sys.exit(0)    

def signal_handler(sig, frame):
    print('Stopping server...')
    socketio.stop()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    threading.Thread(target=start_spraakherkenning).start()
    socketio.run(app, debug=True, port=5001)