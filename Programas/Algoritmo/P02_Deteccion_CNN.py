import sys
import cv2
import numpy as np
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from keras.models import load_model
from keras.utils import img_to_array



# Configurar interfaz

qtCreatorFile = "DetectorTiempoReal.ui"  # nombre de tu archivo .ui
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)



# Clase principal

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.alto, self.largo = 300, 300
        self.modelo = "./modelo/modelo.keras"
        self.pesos = "./modelo/pesos.weights.h5"

        self.cnn = load_model(self.modelo)
        self.cnn.load_weights(self.pesos)


        self.captura = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.actualizar_frame)
        self.en_ejecucion = False


        self.btn_iniciar.clicked.connect(self.toggle_camara)


    # Metodos de cámara

    def toggle_camara(self):
        if not self.en_ejecucion:
            self.iniciar_camara()
        else:
            self.detener_camara()

    def iniciar_camara(self):
        self.captura = cv2.VideoCapture(0)
        if not self.captura.isOpened():
            self.lbl_resultado.setText("Verificar entrada de camara")
            return

        self.timer.start(60)
        self.en_ejecucion = True
        self.btn_iniciar.setText("Detener camara")

    def detener_camara(self):
        self.timer.stop()
        if self.captura:
            self.captura.release()
        self.lbl_video.clear()
        self.en_ejecucion = False
        self.btn_iniciar.setText("Iniciar camara")

    def actualizar_frame(self):
        ret, frame = self.captura.read()
        if not ret:
            return

        # Mostrar imagen en el QLabel
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        altura, ancho, canal = frame_rgb.shape
        bytes_per_line = canal * ancho
        q_img = QtGui.QImage(frame_rgb.data, ancho, altura, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        self.lbl_video.setPixmap(pixmap.scaled(self.lbl_video.width(), self.lbl_video.height(), QtCore.Qt.KeepAspectRatio))

        # Detectar persona
        self.detectar(frame)

    # Prediccion CNN

    def detectar(self, frame):
        try:
            imagen = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            imagen = cv2.resize(imagen, (self.alto, self.largo))
            imagen = img_to_array(imagen)
            imagen = np.expand_dims(imagen, axis=0)

            prediccion = self.cnn.predict(imagen, verbose=0)
            resultado = np.argmax(prediccion[0])

            nombres = {
                0: 'C01_Lexiss',
                1: 'C02_Rodrigo',
                2: 'C03_Victor',
                3: 'C04_Eduardo'
            }
            nombre = nombres.get(resultado, "Desconocido")
            #confianza = np.max(prediccion[0]) * 100

            self.lbl_resultado.setText(f"Detectado: {nombre}")
        except Exception as e:
            self.lbl_resultado.setText(f"Error: {e}")


# Programa principal

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
