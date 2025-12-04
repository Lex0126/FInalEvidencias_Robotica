import cv2
import numpy as np
import os


alto, largo = 300, 300
MODELO_EIGEN_PATH = "./Modelo_face/modeloEigenFace.xml"
MODELO_FISHER_PATH = "./Modelo_face/modeloFisherFace.xml"
MODELO_LBPH_PATH = "./Modelo_face/modeloLBPHFace.xml"
TEST_DATA_PATH = "./C03_Test/"



def get_folders_name_from(from_location):
    """Obtiene los nombres de las subcarpetas en una ubicacio   n."""
    if not os.path.isdir(from_location):
        print(f"Error: El directorio no existe - {from_location}")
        return []

    list_dir = os.listdir(from_location)
    folders = []
    for file in list_dir:
        full_path = os.path.join(from_location, file)
        if os.path.isdir(full_path):
            # Ignora carpetas ocultas como .git o __pycache__
            if not file.startswith('.'):
                folders.append(file)

    folders.sort()
    return folders


# --- Mapeo de Etiquetas (Labels) ---
# Asumimos que las etiquetas 0, 1, 2... corresponden
# al orden alfabético de las carpetas.
FOLDERS_LIST = get_folders_name_from(TEST_DATA_PATH)
if FOLDERS_LIST:
    LABEL_MAP = {i: name for i, name in enumerate(FOLDERS_LIST)}
    print("Mapeo de etiquetas cargado:", LABEL_MAP)
else:
    LABEL_MAP = {}
    print(f"Advertencia: No se encontraron carpetas en {TEST_DATA_PATH}")

# --- Carga de TODOS los Modelos ---
print("\nCargando modelos de OpenCV...")

eigen_recognizer = cv2.face.EigenFaceRecognizer_create()
fisher_recognizer = cv2.face.FisherFaceRecognizer_create()
lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()

try:
    eigen_recognizer.read(MODELO_EIGEN_PATH)
    print(f"Programas EigenFace cargado.")
except cv2.error:
    print(f"ERROR No se pudo cargar {MODELO_EIGEN_PATH}")
    eigen_recognizer = None  # Desactivar si falla la carga

try:
    fisher_recognizer.read(MODELO_FISHER_PATH)
    print(f"Programas FisherFace cargado.")
except cv2.error:
    print(f"ERROR! No se pudo cargar {MODELO_FISHER_PATH}")
    fisher_recognizer = None  # Desactivar si falla la carga

try:
    lbph_recognizer.read(MODELO_LBPH_PATH)
    print(f"Programas LBPH cargado.")
except cv2.error:
    print(f"ERROR! No se pudo cargar {MODELO_LBPH_PATH}")
    lbph_recognizer = None  # Desactivar si falla la carga


def predict(model_recognizer, image):
    """
    Función de predicción genérica para un modelo OpenCV.
    Recibe el objeto del modelo y la imagen ya procesada.
    """
    if model_recognizer is None:
        return "---- (NO CARGADO)"

    try:
        label, confidence = model_recognizer.predict(image)
        # Devuelve el nombre de la carpeta (ej: 'C02_Rodrigo')
        return LABEL_MAP.get(label, f"Etiqueta desconocida {label}")
    except cv2.error as e:
        print(f"Error durante la predicción: {e}")
        return "---- (ERROR)"


def probar_red_neuronal():
    """Prueba la eficiencia de todos los modelos cargados."""
    base_location = TEST_DATA_PATH
    if not FOLDERS_LIST:
        print(f"No se encontraron carpetas en {base_location}. Abortando prueba.")
        return

    # Usamos un diccionario para guardar las estadísticas de cada modelo
    stats = {
        'Eigen': {'correct': 0, 'model': eigen_recognizer},
        'Fisher': {'correct': 0, 'model': fisher_recognizer},
        'LBPH': {'correct': 0, 'model': lbph_recognizer}
    }
    count_predictions = 0

    print("\n--- Iniciando Pruebas de Modelos ---")

    for folder in FOLDERS_LIST:
        folder_path = os.path.join(base_location, folder)

        try:
            files = [f for f in os.listdir(folder_path) if f.endswith((".jpg", ".jpeg", ".png"))]
        except FileNotFoundError:
            print(f"Advertencia: Carpeta no encontrada {folder_path}")
            continue

        if not files:
            print(f"No se encontraron imágenes en {folder_path}")
            continue

        print(f"\nProcesando Carpeta: {folder}")

        for file in files:
            composed_location = os.path.join(folder_path, file)

            # 1. Cargar y procesar la imagen UNA VEZ
            imagen = cv2.imread(composed_location, cv2.IMREAD_GRAYSCALE)
            if imagen is None:
                print(f"  Advertencia: No se pudo leer {file}")
                continue

            # Todos los modelos de OpenCV fueron entrenados con imágenes
            # redimensionadas, así que aplicamos lo mismo a la prueba.
            imagen_procesada = cv2.resize(imagen, (largo, alto))
            count_predictions += 1

            print(f"  Archivo: {file:<25}")

            # 2. Probar cada modelo que se haya cargado correctamente
            for model_name, data in stats.items():
                if data['model']:  # Si el modelo no es None
                    prediction = predict(data['model'], imagen_procesada)
                    is_correct = (prediction == folder)

                    if is_correct:
                        data['correct'] += 1

                    print(f"    - {model_name:<7}: {prediction:<15} {'(Correcto)' if is_correct else '(Incorrecto)'}")

    # --- Reporte Final ---
    print("\n======================================")
    print("--- Resultados Finales ---")
    print("======================================")

    if count_predictions > 0:
        print(f"Total de Imágenes Probadas: {count_predictions}\n")

        # Imprimir resultados para cada modelo
        for model_name, data in stats.items():
            if data['model']:
                efficiency = (data['correct'] / count_predictions) * 100
                print(f"Resultados {model_name}Face:")
                print(f"   Correctas: {data['correct']} / {count_predictions}")
                print(f"   Eficiencia: {efficiency:.2f}%")
            else:
                print(f"Resultados {model_name}Face:")
                print("   Programas no fue cargado. Prueba omitida.")
    else:
        print("No se realizaron predicciones")


if LABEL_MAP:
    probar_red_neuronal()