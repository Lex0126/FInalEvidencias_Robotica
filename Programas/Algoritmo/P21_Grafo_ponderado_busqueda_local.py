import networkx as nx
import matplotlib.pyplot as plt
import math
import time

# 1. Definicion del Grafo Ponderado
grafo_ponderado = {
    'A': {'A': 0, 'B': 29, 'C': 20, 'D': 21},
    'B': {'A': 29, 'B': 0, 'C': 15, 'D': 35},
    'C': {'A': 20, 'B': 15, 'C': 0, 'D': 30},
    'D': {'A': 21, 'B': 35, 'C': 30, 'D': 0},
}

#2. Variables Globales para el Estado
# Necesitamos que la funcion recursiva actualice la mejor ruta
mejor_ruta_global = []
mejor_costo_global = math.inf


#3. Funcion de Ayuda para Calcular Costo
def calcular_costo_ruta(ruta, grafo):
    costo_total = 0
    for i in range(len(ruta) - 1):
        costo_total += grafo[ruta[i]][ruta[i + 1]]
    costo_total += grafo[ruta[-1]][ruta[0]]  # Regresar al inicio
    return costo_total


#4. Funcion de Dibujo (Actualiza la MISMA ventana)
def dibujar_estado_grafo(G, pos, ax, ruta_actual, titulo=""):
    """
    Limpia y redibuja el grafo en el 'ax' (eje) proporcionado.
    Muestra la ruta de exploracion (azul) y la mejor ruta (verde).
    """
    ax.clear()  # Limpia el dibujo anterior
    ax.set_title(titulo)

    # Convertir rutas (listas de nodos) a aristas
    aristas_actuales = list(zip(ruta_actual[:-1], ruta_actual[1:]))
    aristas_mejores = []
    if mejor_ruta_global:
        aristas_mejores = list(zip(mejor_ruta_global[:-1], mejor_ruta_global[1:]))
        # Anadir arista de cierre para la mejor ruta
        aristas_mejores.append((mejor_ruta_global[-1], mejor_ruta_global[0]))

    # Dibujar aristas base (grises)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=1, alpha=0.5)

    # Dibujar la MEJOR ruta (verde)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=aristas_mejores, edge_color='green', width=3)

    # Dibujar la ruta de exploracion ACTUAL (azul)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=aristas_actuales, edge_color='blue', width=2)

    # Dibujar nodos, etiquetas y pesos
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_color='darkgreen')

    plt.axis('off')
    plt.pause(0.5)  # Pausa breve para crear el efecto de animacion


# --- 5. Algoritmo de Busqueda (Backtracking / DFS) ---
def busqueda_dfs_visual(G, pos, ax, nodo_actual, nodo_inicio, visitados, ruta_actual):
    """
    Funcion recursiva que explora el grafo y actualiza el dibujo.
    """
    global mejor_ruta_global, mejor_costo_global

    # 1. Marcar nodo como visitado y anadir a la ruta
    visitados.add(nodo_actual)
    ruta_actual.append(nodo_actual)

    # 2. Visualizar este paso (AVANCE)
    titulo_str = f"Explorando: {'->'.join(ruta_actual)}"
    dibujar_estado_grafo(G, pos, ax, ruta_actual, titulo=titulo_str)

    # 3. Caso Base: Todos los nodos visitados
    if len(visitados) == len(G.nodes):
        costo_actual = calcular_costo_ruta(ruta_actual, G.graph['data'])
        print(f"Ruta completa: {'->'.join(ruta_actual)} | Costo: {costo_actual}")

        if costo_actual < mejor_costo_global:
            mejor_costo_global = costo_actual
            mejor_ruta_global = ruta_actual.copy()
            print(f"*** NUEVA MEJOR RUTA: {mejor_costo_global} ***")
            titulo_str = f"Mejor Ruta: {costo_actual}"
            dibujar_estado_grafo(G, pos, ax, ruta_actual, titulo=titulo_str)
            plt.pause(0.5)  # Pausa mas larga para ver la mejor ruta

    # 4. Paso Recursivo: Visitar vecinos no visitados
    else:
        for vecino in G.neighbors(nodo_actual):
            if vecino not in visitados:
                busqueda_dfs_visual(G, pos, ax, vecino, nodo_inicio, visitados, ruta_actual)

    # 5. Backtrack (Retroceso)
    # Quitar este nodo de la ruta para probar otros caminos
    visitados.remove(nodo_actual)
    ruta_actual.pop()

    # 6. Visualizar este paso (RETROCESO)
    titulo_str = f"Retrocediendo desde {nodo_actual}"
    dibujar_estado_grafo(G, pos, ax, ruta_actual, titulo=titulo_str)


#6. Ejecucion Principal
if __name__ == "__main__":

    # 1. Crear grafo de NetworkX
    G = nx.Graph()
    G.graph['data'] = grafo_ponderado  # Guardamos el dict original
    for nodo_origen, conexiones in grafo_ponderado.items():
        for nodo_destino, peso in conexiones.items():
            if nodo_origen != nodo_destino:
                G.add_edge(nodo_origen, nodo_destino, weight=peso)

    pos = nx.circular_layout(G)

    # 2. Configurar Matplotlib para modo interactivo
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 8))

    print("Iniciando Busqueda en tiempo real (DFS)...")

    # 3. Variables de estado inicial
    nodo_inicio = 'A'
    visitados = set()
    ruta_actual = []

    # 4. Iniciar la busqueda
    busqueda_dfs_visual(G, pos, ax, nodo_inicio, nodo_inicio, visitados, ruta_actual)

    # 5. Mantener la ventana final abierta
    plt.ioff()
    ax.clear()

    ruta_final_str = ' -> '.join(mejor_ruta_global) + f' -> {mejor_ruta_global[0]}'
    titulo_final = f"Ruta Optima Final (Costo: {mejor_costo_global})\n{ruta_final_str}"

    # Dibujar solo la mejor ruta al final
    aristas_mejores = list(zip(mejor_ruta_global[:-1], mejor_ruta_global[1:]))
    aristas_mejores.append((mejor_ruta_global[-1], mejor_ruta_global[0]))

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', node_size=1000)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=1, alpha=0.5)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=aristas_mejores, edge_color='green', width=4)
    ax.set_title(titulo_final)

    print("\n--- Resultado Final ---")
    print(f"Mejor ruta: {ruta_final_str}")
    print(f"Costo total: {mejor_costo_global}")

    plt.show()  # Mantiene la ventana final abierta