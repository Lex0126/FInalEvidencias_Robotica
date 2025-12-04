import cv2
import numpy as np

##REQUIERE : pip install opencv-contrib-python -> PARA UTILIZAR CV2.FACE

def train(images, labels):
	face_recognizer = cv2.face.EigenFaceRecognizer_create()

	print("Inicia Entrenamiento...")
	face_recognizer.train(images, np.array(labels))
	print("Entrenamiento Finalizado")
	dir = "../Modelo_face/"
	face_recognizer.write( dir + 'modeloEigenFace.xml')
	print("Programas almacenado!!!")