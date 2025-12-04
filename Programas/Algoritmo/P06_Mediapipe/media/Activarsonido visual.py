import cv2
import mediapipe as mp
import math
import pygame
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# Inicializar pygame mixer
pygame.mixer.init()

# Variables globales
gesto_previo = None
sonido_actual = None
current_gif = None
gif_frames = []
gif_index = 0

# Diccionario de gestos con sonido y GIF
gestures_media = {
    0: ("Gato", "./media/gato.mp3", "./media/gato.gif"),
    1: ("Perro", "./media/perro.mp3", "./media/perro.gif"),
    2: ("Pajaro", "./media/pajaro.mp3", "./media/pajaro.gif"),
    3: ("Cuyo", "./media/cuyo.mp3", "./media/cuyo.gif"),
    4: ("Serpiente", "./media/serpiente.mp3", "./media/serpiente.gif"),
   # 5: ("Goldship", "./media/goldship.mp3", "./media/goldship1.gif")
}

# Función para contar dedos
def count_fingers(hand_landmarks, handedness):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    for tip in tips[1:]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    if handedness == 'Left':
        fingers.insert(0, 1 if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x else 0)
    else:
        fingers.insert(0, 1 if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x else 0)

    return sum(fingers)

# Funcion para reproducir sonido y cargar GIF
def gesture(finger_count):
    global gesto_previo, sonido_actual, current_gif, gif_frames, gif_index

    if finger_count in gestures_media:
        animal, sonido, gif_file = gestures_media[finger_count]

        if gesto_previo != finger_count:
            # Sonido
            if sonido_actual:
                sonido_actual.stop()
            sonido_actual = pygame.mixer.Sound(sonido)
            sonido_actual.play()

            # GIF
            current_gif = Image.open(gif_file)
            gif_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA"))
                          for frame in ImageSequence.Iterator(current_gif)]
            gif_index = 0

            gesto_previo = finger_count

        return animal
    else:
        return "Gesto desconocido"

# Funcion para actualizar la camara y los gifs
def update_frame():
    global gif_index

    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    gesture_text = ""
    finger_count_text = ""

    if result.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
            handedness = result.multi_handedness[idx].classification[0].label
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_count = count_fingers(hand_landmarks, handedness)
            gesture_text = gesture(finger_count)
            finger_count_text = f"Dedos: {finger_count}"

            # Mostrar rectángulo y texto en cámara
            x1, y1 = 30, 60
            x2, y2 = 300, 200
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), thickness=cv2.FILLED)
            cv2.putText(frame, gesture_text, (x1 + 10, y1 + 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, finger_count_text, (x1 + 10, y1 + 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Convertir OpenCV a Tkinter
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    lbl_video.imgtk = imgtk
    lbl_video.configure(image=imgtk)

    # Mostrar GIF
    if gif_frames:
        lbl_gif.configure(image=gif_frames[gif_index])
        gif_index = (gif_index + 1) % len(gif_frames)

    root.after(50, update_frame)  # Actualizar cada 50ms

# Configuracion MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(min_detection_confidence=0.7,
                       min_tracking_confidence=0.7,
                       max_num_hands=1)

# Configuracion Tkinter
root = tk.Tk()
root.title("Gestos y sonidos")
root.geometry("1200x700")
root.config(bg="#222831")
lbl_video = tk.Label(root)
lbl_video.pack()
lbl_gif = tk.Label(root)
lbl_gif.pack()

root.after(10, update_frame)
root.mainloop()


cap.release()
hands.close()

