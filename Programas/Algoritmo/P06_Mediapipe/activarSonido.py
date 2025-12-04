import cv2
import mediapipe as mp
import pyautogui
from mediapipe.python.solutions.drawing_utils import RED_COLOR, WHITE_COLOR, BLUE_COLOR
import math
import tkinter as tk
from PIL import Image, ImageTk
import pygame
pygame.mixer.init()

def count_fingers(hand_landmarks, handedness):
    """Cuenta los dedos levantados basado en la posición de los landmarks."""
    tips = [4, 8, 12, 16, 20]  # Índices de las puntas de los dedos en MediaPipe
    fingers = []

    # Comparar cada punta con su articulación anterior
    for tip in tips[1:]:  # Excluye el pulgar temporalmente
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)  # Dedo levantado
        else:
            fingers.append(0)  # Dedo doblado

    # Para el pulgar, se compara con su base y la orientación de la mano
    if handedness == 'Left':  # Mano izquierda
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            fingers.insert(0, 1)
        else:
            fingers.insert(0, 0)
    else:  # Mano derecha
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers.insert(0, 1)
        else:
            fingers.insert(0, 0)

    return sum(fingers)  # Retorna el número de dedos levantados


previous_gesture = None
current_sound = None
def get_gesture(finger_count):
    global previous_gesture, current_sound

    gestures_sounds = {
        0: ("gato", "./media/gato.mp3"),
        1: ("perro", "./media/perro.mp3"),
        2: ("pajaro", "./media/pajaro.mp3"),
        3: ("cuyo", "./media/cuyo.mp3"),
        4: ("serpiente", "./media/serpiente.mp3"),

    }

    if finger_count in gestures_sounds:
        animal, sonido = gestures_sounds[finger_count]

        # Si cambió el gesto, detener el anterior y reproducir el nuevo
        if previous_gesture != finger_count:
            if current_sound:
                current_sound.stop()
            current_sound = pygame.mixer.Sound(sonido)
            current_sound.play()
            previous_gesture = finger_count

        return animal
    else:
        return "Gesto desconocido"


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                # Determinar si la mano es izquierda o derecha
                handedness = result.multi_handedness[idx].classification[0].label

                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                       mp_draw.DrawingSpec(color=RED_COLOR, thickness=5),
                                       mp_draw.DrawingSpec(color=(0, 255, 0), thickness=6))

                finger_count = count_fingers(hand_landmarks, handedness)
                gesture = get_gesture(finger_count)
                min_x = min([hand_landmarks.landmark[i].x for i in range(21)])
                max_x = max([hand_landmarks.landmark[i].x for i in range(21)])
                min_y = min([hand_landmarks.landmark[i].y for i in range(21)])
                max_y = max([hand_landmarks.landmark[i].y for i in range(21)])


                h, w, _ = frame.shape
                min_x = int(min_x * w)
                max_x = int(max_x * w)
                min_y = int(min_y * h)
                max_y = int(max_y * h)

                # Dibujar un rectángulo alrededor de la mano
                cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)

                # Mostrar el gesto
                x1, y1 = 30, 60
                x2, y2 = 300, 200
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), thickness=cv2.FILLED)
                cv2.putText(frame, gesture, (x1 + 10, y1 + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame,f"Dedos: {finger_count}", (x1 + 10, y1 + 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                


        cv2.imshow("Deteccion y sonido", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Esc para salir
            break

ventana= tk.Tk()

cap.release()
cv2.destroyAllWindows()
