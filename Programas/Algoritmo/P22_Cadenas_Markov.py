import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# --- 1. Definicion de la Cadena de Markov ---
# (Matriz de transicion con NUEVAS probabilidades)
# La unica regla es que la suma de cada fila sea 1.0

transiciones = {
    # Logica: Despues de comer, tienes energia para estudiar
    'Comer': {'Comer': 0.1, 'Jugar': 0.2, 'Estudiar': 0.7},

    # Logica: Despues de jugar, da hambre
    'Jugar': {'Comer': 0.6, 'Jugar': 0.2, 'Estudiar': 0.2},

    # Logica: Despues de estudiar, quieres un descanso
    'Estudiar': {'Comer': 0.4, 'Jugar': 0.5, 'Estudiar': 0.1}
}
# Verificacion de sumas:
# Comer:    0.1 + 0.2 + 0.7 = 1.0
# Jugar:    0.6 + 0.2 + 0.2 = 1.0
# Estudiar: 0.4 + 0.5 + 0.1 = 1.0

# --- 2. Configuracion de la Simulacion ---
NUM_PASOS = 300
ESTADO_INICIAL = 'Comer'  # Empezamos comiendo


# --- 3. Funcion para el siguiente paso ---
def siguiente_estado(estado_actual, matriz_transicion):
    """Elige el proximo estado basado en probabilidades."""

    destinos = list(matriz_transicion[estado_actual].keys())
    probabilidades = list(matriz_transicion[estado_actual].values())

    # Elige uno aleatoriamente, ponderado por las probabilidades
    return random.choices(destinos, weights=probabilidades, k=1)[0]


# --- 4. Funcion Principal de Visualizacion ---
def simular_cadena_markov():
    # 1. Crear Grafo Dirigido
    G = nx.DiGraph()
    for origen, destinos in transiciones.items():
        for destino, prob in destinos.items():
            if prob > 0:
                G.add_edge(origen, destino, weight=round(prob, 2))

    pos = nx.circular_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # 2. Configurar Ventana Interactiva
    plt.ion()  # Modo interactivo
    fig, (ax_grafo, ax_barras) = plt.subplots(1, 2, figsize=(16, 7))

    # 3. Variables de Estado
    estado_actual = ESTADO_INICIAL
    conteo_estados = {estado: 0 for estado in G.nodes()}

    print("Iniciando simulacion...")
    print(f"Paso 0: Empezando en {estado_actual}")

    # 4. Bucle de Simulacion
    for i in range(NUM_PASOS):
        conteo_estados[estado_actual] += 1

        # --- DIBUJAR GRAFO (Izquierda) ---
        ax_grafo.clear()

        nx.draw_networkx_edges(G, pos, ax=ax_grafo,
                               connectionstyle='arc3,rad=0.1',
                               arrowstyle='->', arrowsize=15,
                               edge_color='gray', node_size=2000)
        nx.draw_networkx_edge_labels(G, pos, ax=ax_grafo,
                                     edge_labels=edge_labels,
                                     label_pos=0.3, font_size=9)

        nx.draw_networkx_nodes(G, pos, ax=ax_grafo, node_color='lightblue', node_size=2000)
        nx.draw_networkx_nodes(G, pos, ax=ax_grafo, nodelist=[estado_actual],
                               node_color='red', node_size=2000)
        nx.draw_networkx_labels(G, pos, ax=ax_grafo, font_size=12, font_weight='bold')

        ax_grafo.set_title("Simulador de Paseo Aleatorio")
        plt.axis('off')

        # --- DIBUJAR GRAFICO DE BARRAS (Derecha) ---
        ax_barras.clear()

        total_pasos = i + 1
        probabilidades = {estado: conteo / total_pasos for estado, conteo in conteo_estados.items()}

        nombres_estados = list(transiciones.keys())
        valores_prob = [probabilidades[estado] for estado in nombres_estados]

        ax_barras.bar(nombres_estados, valores_prob, color=['lightgreen', 'skyblue', 'salmon'])
        ax_barras.set_ylim(0, 1.0)
        ax_barras.set_title("Tiempo en cada estado")
        ax_barras.set_ylabel("Probabilidad")

        for j, prob in enumerate(valores_prob):
            ax_barras.text(j, prob + 0.02, f"{prob:.2%}", ha='center')

        # --- Actualizar y pausar ---
        fig.suptitle(f"Paso {i + 1} / {NUM_PASOS} | Estado Actual: {estado_actual}", fontsize=16)
        plt.pause(0.1)  # Pausa para animacion

        # --- Calcular Siguiente Paso ---
        estado_actual = siguiente_estado(estado_actual, transiciones)

    # 5. Finalizar
    plt.ioff()
    print("Simulacion finalizada.")
    print("Distribucion final:", probabilidades)
    ax_grafo.set_title(f"Simulacion Finalizada")
    plt.show()


# --- 5. Ejecucion Principal ---
if __name__ == "__main__":
    simular_cadena_markov()