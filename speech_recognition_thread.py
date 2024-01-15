# speech_recognition_thread.py

import speech_recognition as sr
import json
from datetime import datetime
import time
import threading  # Importeer threading
from flask_socketio import SocketIO
from shared import get_socketio

woorden_teller = {}  # Globale variabele voor tellerstanden
laatste_tekst = ""   # Globale variabele voor de laatst gedetecteerde tekst
socketio = get_socketio()

def laad_woorden(filename):
    with open(filename, 'r') as file:
        return [line.strip().lower() for line in file]

def start_spraakherkenning():
    global woorden_teller, laatste_tekst, socketio
    woorden = laad_woorden("woorden.txt")
    woorden_teller = laad_tellerstanden("tellerstanden.json")
    r = sr.Recognizer()
    virtuele_audio_device = 2

    with sr.Microphone(device_index=virtuele_audio_device) as bron:
        print("Luisteren naar systeemaudio...")
        while True:
            try:
                audio = r.listen(bron, phrase_time_limit=5)
                text = r.recognize_google(audio, language='nl-NL').lower()
                print(f"Gedetecteerd: {text}")
                laatste_tekst = text  # Update de laatst gedetecteerde tekst
                socketio.emit('update', {'laatsteTekst': laatste_tekst})
                

                for woord in woorden:
                    if woord in text:
                        woorden_teller[woord] = woorden_teller.get(woord, 0) + 1
                        print(f"\"{woord}\" gedetecteerd! Totaal aantal keren gehoord: {woorden_teller[woord]}")
            except sr.UnknownValueError:
                print("Spraakherkenning kon geen tekst interpreteren uit audio")
            except sr.RequestError as e:
                print(f"Spraakherkenningsservice kan niet worden opgevraagd; {e}")
            except Exception as e:
                print(f"Onverwachte fout bij spraakherkenning: {e}")


def laad_tellerstanden(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {woord: 0 for woord in laad_woorden("woorden.txt")}

def sla_tellerstanden_op(filename, tellerstanden):
    with open(filename, 'w') as file:
        json.dump(tellerstanden, file)

def maak_verslag():
    global laatste_tekst

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    verslag_naam = f"verslag_{timestamp}.txt"
    
    with open(verslag_naam, 'w') as file:
        for woord, aantal in woorden_teller.items():
            file.write(f"{woord}: {aantal}\n")

        # Voeg een regel toe om de laatste tekst ook op te slaan in het verslag
        file.write(f"\nLaatst Gedetecteerde Tekst: {laatste_tekst}")

def periodieke_opslag():
    global woorden_teller
    while True:
        time.sleep(300)  # 5 minuten wachten
        sla_tellerstanden_op("tellerstanden.json", woorden_teller)
        print("Tellerstanden opgeslagen")

if __name__ == '__main__':
    threading.Thread(target=start_spraakherkenning).start()
    threading.Thread(target=periodieke_opslag, daemon=True).start()