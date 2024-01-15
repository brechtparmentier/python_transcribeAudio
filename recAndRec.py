import os
import speech_recognition as sr
from datetime import datetime

# Globale variabelen
opname_lengte = 10  # Lengte van de opname in seconden
opname_directory = "opnames"  # Map waar de opnames opgeslagen worden

# Zorg ervoor dat de opnamedirectory bestaat
if not os.path.exists(opname_directory):
    os.makedirs(opname_directory)

def neem_op_en_bewaar(r, bron):
    global opname_lengte, opname_directory
    while True:
        try:
            # Neem audio op
            print("Opname begonnen...")
            audio = r.listen(bron, timeout=None, phrase_time_limit=opname_lengte)
            opname_tijd = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            opname_bestand = f"{opname_directory}/opname_{opname_tijd}.wav"
            
            # Sla de audio op
            with open(opname_bestand, "wb") as f:
                f.write(audio.get_wav_data())
            print(f"Opname opgeslagen als {opname_bestand}")

            # Verwerk de audio (kan ook later in een aparte functie of script)
            verwerk_audio(r, opname_bestand)
            
        except Exception as e:
            print(f"Fout bij het opnemen: {e}")

def verwerk_audio(r, audio_bestand):
    try:
        with sr.AudioFile(audio_bestand) as bron:
            audio = r.record(bron)  # Lees de hele audiofile
        text = r.recognize_google(audio, language='nl-NL').lower()
        print(f"Tekst gedetecteerd: {text}")

        # Hier zou je de gedetecteerde tekst kunnen verwerken, zoals het tellen van woorden of het opslaan van de tekst voor analyse.

    except sr.UnknownValueError:
        print("Google Speech Recognition kon geen tekst interpreteren uit audio.")
    except sr.RequestError as e:
        print(f"Kon geen verzoek maken aan Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Onverwachte fout bij het verwerken van audio: {e}")

def start_spraakherkenning():
    r = sr.Recognizer()
    virtuele_audio_device = 2 # De index van je virtuele audio device

    with sr.Microphone(device_index=virtuele_audio_device) as bron:
        # Je kunt hier enige audio-voorverwerking toevoegen als dat nodig is, zoals ruisreductie
        neem_op_en_bewaar(r, bron)

if __name__ == '__main__':
    start_spraakherkenning()
