import cv2  ##opencv
cam = cv2.VideoCapture(0) ##videocamara ---

contFotos = 1
frame_count = 0   # contador de frames
capturando = False   # bandera: solo inicia cuando se presione espacio

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def face_detect_box(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    faces_frames = []
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)

        aux = image.copy()
        faces_frames.append(aux[y:y+h, x:x+w])

    return faces, faces_frames


while True:
    result, image = cam.read()
    if not result:
        print("no se detecta la cara")
        break

    # deteccion de rostros
    faces_detected, img_faces = face_detect_box(image)

    cv2.imshow("Camara_Principal", image)

    frame_count += 1

    # Solo toma fotos si diste espacio
    if capturando and frame_count % 2 == 0 and contFotos <= 500:
        if len(img_faces) == 0:
            cv2.imwrite("foto_" + str(contFotos) + ".png", image)
            contFotos += 1
        else:
            for img in img_faces:
                imagen_cara = cv2.resize(img, (400, 400), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite("foto_" + str(contFotos) + ".png", imagen_cara)
                contFotos += 1

    # Terminar cuando llegue a 500 fotos
    if contFotos > 500:
        print("Captura completa (500 fotos)")
        break

    res = cv2.waitKey(1)
    if res == ord("q"):  # salir manualmente
        break
    elif res == ord(" "):  #iniciar
        print("Iniciando captura de 500 fotos...")
        capturando = True

cam.release()
cv2.destroyAllWindows()
