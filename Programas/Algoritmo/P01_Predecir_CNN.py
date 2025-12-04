import os

import numpy as np
#from keras.preprocessing.image import load_img, img_to_array  #deprecated en tf 2.9
#from tensorflow.keras.utils import load_img  #alternative 1
from keras.utils import load_img, img_to_array #alternative 2

from keras.models import load_model

alto, largo = 300, 300
modelo = "./modelo/modelo.keras" #./modelo/modelo.h5'
pesos = './modelo/pesos.weights.h5'

cnn = load_model(modelo)
cnn.load_weights(pesos)

def predict(file):
    imagen_a_predecir = load_img(file, target_size = (alto, largo), color_mode="grayscale")
    imagen_a_predecir = img_to_array(imagen_a_predecir)
    imagen_a_predecir = np.expand_dims(imagen_a_predecir, axis=0) #agrega una dimension adicional
    arreglo = cnn.predict(imagen_a_predecir) ## [[1,0,0,0,0,0]]
    resultado = arreglo[0]
    respuesta = np.argmax(resultado) #indice del valor mas alto

    match respuesta:
        case 0:
            return 'C01_Lexiss'
        case 1:
            return 'C02_Rodrigo'
        case 2:
            return 'C03_Victor'
        case 3:
            return 'C04_Eduardo'
        case _:
            return '----'

#predict('C:/Users/lexis/PycharmProjects/imagenes/Programas/Algoritmo/C03_Test/C01_Lexiss/foto_401.png')

def get_folders_name_from(from_location):
    list_dir = os.listdir(from_location)
    # folders = [archivo for archivo in listDir if os.path.splitext(archivo)[1] == ""]
    # the above is equals to ....
    folders = []
    for file in list_dir:
        temp = os.path.splitext(file)
        if temp[1] == "":
            folders.append(temp[0])
    folders.sort()
    #folders.remove('.DS_Store') #solo en mac
    return folders


def probar_red_neuronal():
    base_location = "./C03_Test/" #'./F3-Prueba/'

    folders = get_folders_name_from(base_location)

    correct = 0
    count_predictions = 0
    for folder in folders:
        files = [archivo for archivo in os.listdir(base_location + '/' + folder) if archivo.endswith(".jpg") or archivo.endswith(".jpeg") or archivo.endswith(".png")]
        for file in files:
            composed_location = base_location + folder + '/' + file
            prediction =  predict(composed_location)
            print('Folder Name: ', folder, ' Prediction: ',  prediction, " Resulto: ", prediction in folder)
            count_predictions += 1
            if prediction in folder:
                correct +=1

    print("Efficiency: ", (correct/count_predictions*100))

probar_red_neuronal()