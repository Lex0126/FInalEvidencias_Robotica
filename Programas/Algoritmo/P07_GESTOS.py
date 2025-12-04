import cv2
import mediapipe as mp
import collections
import socket
import time

# Configuracion UDP para enviar a Unity
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Configuracion de MediaPipe
FRAMES_SUAVIZADO = 5  # Aumenta para mas suavizado
PROCESAR_CADA = 2  # Optimizacion: procesar 2 de cada N frames
NUM_MAX_MANOS = 1

# Ajusta la sensibilidad del control
SENSIBILIDAD_X = 7.0
SENSIBILIDAD_Y = 5.0

mp_manos = mp.solutions.hands
mp_dibujo = mp.solutions.drawing_utils
posiciones = collections.deque(maxlen=FRAMES_SUAVIZADO)  # Cola para promediar el movimiento


def punio_cerrado(lista_landmarks):
    # Revisa si los 4 dedos estan doblados (punta > articulacion)
    try:
        index_tip = lista_landmarks[mp_manos.HandLandmark.INDEX_FINGER_TIP]
        index_pip = lista_landmarks[mp_manos.HandLandmark.INDEX_FINGER_PIP]
        middle_tip = lista_landmarks[mp_manos.HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = lista_landmarks[mp_manos.HandLandmark.MIDDLE_FINGER_PIP]
        ring_tip = lista_landmarks[mp_manos.HandLandmark.RING_FINGER_TIP]
        ring_pip = lista_landmarks[mp_manos.HandLandmark.RING_FINGER_PIP]
        pinky_tip = lista_landmarks[mp_manos.HandLandmark.PINKY_TIP]
        pinky_pip = lista_landmarks[mp_manos.HandLandmark.PINKY_PIP]

        # Compara la coordenada Y de la punta con la articulacion PIP
        fist_closed = (index_tip.y > index_pip.y and
                       middle_tip.y > middle_pip.y and
                       ring_tip.y > ring_pip.y and
                       pinky_tip.y > pinky_pip.y)
        return fist_closed
    except Exception as e:
        return False  # Si falla la deteccion, asume que no es punio


# Iniciar captura de camara
cap = cv2.VideoCapture(0)
cap.set(4, 480)
contador_frame = 0

with mp_manos.Hands(
        static_image_mode=False,
        max_num_hands=NUM_MAX_MANOS,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6) as manos:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Optimizacion para saltar frames
        contador_frame += 1
        if contador_frame % PROCESAR_CADA != 0:
            cv2.imshow("Control Mano", frame)  # Mostrar frame saltado
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue  # Continuar al siguiente ciclo

        # Procesar la imagen
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = manos.process(rgb)

        mensaje_udp = "0.0,0.0"  # Valor neutral por defecto
        gesto_parar_detectado = False

        if resultados.multi_hand_landmarks:
            for mano_landmarks in resultados.multi_hand_landmarks:

                # Gesto 1: Punio cerrado para derrapar ("parar")
                if punio_cerrado(mano_landmarks.landmark):
                    mensaje_udp = "parar"
                    gesto_parar_detectado = True
                    posiciones.clear()  # Resetea el suavizado

                # Gesto 2: Control analogico con dedo indice
                else:
                    base = mano_landmarks.landmark[mp_manos.HandLandmark.INDEX_FINGER_MCP]
                    punta = mano_landmarks.landmark[mp_manos.HandLandmark.INDEX_FINGER_TIP]
                    dx = punta.x - base.x
                    dy = punta.y - base.y
                    posiciones.append((dx, dy))  # Anadir a la cola de suavizado

                # Dibujar los landmarks de la mano
                mp_dibujo.draw_landmarks(frame, mano_landmarks, mp_manos.HAND_CONNECTIONS,
                                         mp_dibujo.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3))

            # Calcular el promedio suavizado si no es puño
            if not gesto_parar_detectado and len(posiciones) > 0:
                dx_prom = sum(p[0] for p in posiciones) / len(posiciones)
                dy_prom = sum(p[1] for p in posiciones) / len(posiciones)

                # Convertir movimiento a control (-1 a 1) e invertir ejes
                turn_val = -dx_prom * SENSIBILIDAD_X
                move_val = -dy_prom * SENSIBILIDAD_Y

                # Limitar los valores (clamp)
                turn_val = max(-1.0, min(1.0, turn_val))
                move_val = max(-1.0, min(1.0, move_val))

                mensaje_udp = f"{turn_val:.4f},{move_val:.4f}"

        else:
            # Si no se detecta mano, enviar neutral
            posiciones.clear()
            mensaje_udp = "0.0,0.0"

        # Enviar el mensaje a Unity
        sock.sendto(mensaje_udp.encode('utf-8'), (UDP_IP, UDP_PORT))

        # Mostrar la direccion en pantalla
        color_texto = (0, 0, 255) if mensaje_udp == "parar" else (0, 255, 0)
        cv2.putText(frame, f"Control: {mensaje_udp}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_texto, 2)
        cv2.imshow("Control Mano", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Salir con ESC
            break

# Limpiar al salir
cap.release()
cv2.destroyAllWindows()