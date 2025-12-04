import sys
import os
import time

from vosk import Model, KaldiRecognizer
import pyaudio
import serial

from Control_de_ventilador_por_voz import control_ventilador as cv

arduino = serial.Serial("COM3",9600)
time.sleep(2)

print("Conexion correcta")

if not os.path.exists("model"):
    print("Descargar modelo de https://alphacephei.com/vosk/models")
    sys.exit(1)

model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

# Start audio stream
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Listening...")



fin = True
while fin:
    data = stream.read(4000)

    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()  # "INSTRUCCION"
        result = result.replace("\"", "")
        result = result.upper()
        posDosPuntos = result.index(":") + 2
        result = result[posDosPuntos:-2]
        print(result)

        comandos = result.split(" ")
        codigo_arduino = cv(comandos)

        if codigo_arduino:
            arduino.write((codigo_arduino + "\n").encode())
            print("Enviando a arduino",codigo_arduino)

    else:
        pass
        #partial_result = recognizer.PartialResult()
        #print(partial_result)