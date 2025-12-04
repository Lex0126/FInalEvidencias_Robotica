import sys
import cv2
import numpy as np
from PyQt5 import uic, QtWidgets, QtCore, QtGui




qtCreatorFile = "OpenCV.ui"  # nombre de tu archivo .ui
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)




class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # tamño de la ventana
        self.alto, self.largo = 300, 300


        self.modeloOP = cv2.face.EigenFaceRecognizer_create()
        self.modeloOP.read("./Modelo_face/modeloEigenFace.xml")
        #self.modeloOP = cv2.face.FisherFaceRecognizer_create()
        #self.modeloOP.read("./Modelo_face/modeloFisherFace.xml")
        #self.modeloOP = cv2.face.LBPHRecognizer_create()
        #self.modeloOP.read("./Modelo_face/modeloLBPHFace.xml")


        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        #diccionario de nombres
        self.nombres = {
            0: 'C01_Lexiss',
            1: 'C02_Rodrigo',
            2: 'C03_Victor',
            3: 'C04_Eduardo'
        }

        #camara
        self.captura = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.actualizar_frame)
        self.en_ejecucion = False

        # boton para inciar
        self.btn_iniciar.clicked.connect(self.toggle_camara)



    def toggle_camara(self):
        if not self.en_ejecucion:
            self.iniciar_camara()
        else:
            self.detener_camara()

    def iniciar_camara(self):
        self.captura = cv2.VideoCapture(0)
        if not self.captura.isOpened():
            self.lbl_resultado.setText("Cambiar la entrada de camara")
            return

        self.timer.start(60)  # cada 60 ms
        self.en_ejecucion = True
        self.btn_iniciar.setText("detener camara")

    def detener_camara(self):
        self.timer.stop()
        if self.captura:
            self.captura.release()
        self.lbl_video.clear()
        self.en_ejecucion = False
        self.btn_iniciar.setText("iniciar camara")

    def actualizar_frame(self):
        ret, frame = self.captura.read()
        if not ret:
            return

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros
        rostros = self.detector.detectMultiScale(frame_gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in rostros:
            rostro = frame_gray[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (self.alto, self.largo))

            label, confianza = self.modeloOP.predict(rostro)
            nombre = self.nombres.get(label, "Desconocido")


            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{nombre})", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            self.lbl_resultado.setText(f"Detectado: {nombre}")

        # Mostrar imagen en QLabel
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        altura, ancho, canal = frame_rgb.shape
        bytes_per_line = canal * ancho
        q_img = QtGui.QImage(frame_rgb.data, ancho, altura, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        self.lbl_video.setPixmap(pixmap.scaled(self.lbl_video.width(), self.lbl_video.height(), QtCore.Qt.KeepAspectRatio))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


