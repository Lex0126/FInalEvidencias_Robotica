

acciones = {
    "PV": "PRENDE VENTILADOR SALA",
    "EV": "ENCIENDE VENTILADOR SALA",
    "AV": "APAGA VENTILADOR SALA",
    "PV1": "VENTILADOR UNO SALA",
    "PV2": "VENTILADOR DOS SALA",
    "PV3": "VENTILADOR TRES SALA",
    "PO": "PRENDE OSCILADOR SALA",
    "EO": "ENCIENDE OSCILADOR SALA",
    "AO": "APAGA OSCILADOR SALA",
}

diccionario = {
    "ACCION": ["PRENDE", "ENCIENDE", "ENCENDER", "PON", "APAGA"],
    "LUGAR": ["SALA", "COMEDOR", "COCINA", "CUARTO"],
    "NIVEL": ["UNO", "DOS", "TRES"],
    "OBJETO": ["VENTILADOR"],
    "MODO": ["OSCILADOR"]
}
#ACCION + OBJETO + LUGAR
def control_ventilador(entrada):
    accion = ""
    lugar = ""
    objeto = ""
    modo = ""
    nivel = ""

    for palabra in entrada:
        if not accion and palabra in diccionario["ACCION"]:
            accion = palabra
        elif not lugar and palabra in diccionario["LUGAR"]:
            lugar = palabra
        elif not objeto and palabra in diccionario["OBJETO"]:
            objeto = palabra
        elif not modo and palabra in diccionario["MODO"]:
            modo = palabra
        elif not nivel and palabra in diccionario["NIVEL"]:
            nivel = palabra

    accion_final = ""
    if objeto and lugar and not nivel and not modo:
        accion_final = f"{accion} {objeto} {lugar}"
        print(f"ACCION ENCONTRADA: {accion_final}")
    elif nivel and objeto and lugar and accion != "APAGA":
        accion_final = f"{objeto} {nivel} {lugar}"
        print(f"ACCION ENCONTRADA: {accion_final}")
    elif modo and lugar and accion:
        accion_final = f"{accion} {modo} {lugar}"
        print(f"ACCION ENCONTRADA: {accion_final}")
    else:
        print("ACCION NO RECONOCIDA")
        return None


    codigo = busqueda_de_accion(accion_final)
    return codigo

def busqueda_de_accion(accion):
    for key, valor in acciones.items():
        if accion == valor:
            print(f"codigo de activacion: {key}")
            return key
    print("codigo de activacion invalida")
    return None
