import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
import os
datos_30_dias = [1,2,0,0,1,1,1,2,2,2,0,1,2,0,1,0,1,2,2,2,1,2,1,2,0,2,0,1,2,0]
# Calcular la matriz estocástica de transición
matriz_transicion = np.zeros((3, 3))
for i in range(len(datos_30_dias) - 1):
    estado_actual = datos_30_dias[i]
    estado_siguiente = datos_30_dias[i + 1]
    matriz_transicion[estado_actual, estado_siguiente] += 1

# Normalizar la matriz para obtener probabilidades
matriz_transicion = matriz_transicion / matriz_transicion.sum(axis=1, keepdims=True)

# Generar más puntos de origen para aumentar la complejidad
np.random.seed(42)
points = np.random.rand(50, 2)

# Calcular el diagrama de Voronoi
vor = Voronoi(points)

# Obtener las regiones y sus límites
regions, vertices = vor.regions, vor.vertices

# Asignar colores específicos para cada estado climático
colors = {
    "Neutro": [0.5, 0.5, 0.5],  # Gris
    "Frío": [0.0, 0.0, 1.0],    # Azul
    "Cálido": [1.0, 1.0, 0.0]   # Amarillo
}

# Crear una lista de colores para cada región basada en los estados climáticos
region_colors_original = []
for region in regions:
    if -1 not in region and len(region) > 0:
        # Asignar color según el estado climático (Neutro, Frío o Cálido)
        rand_val = np.random.rand()
        if rand_val < 0.33:
            region_colors_original.append(colors["Frío"])
        elif rand_val < 0.66:
            region_colors_original.append(colors["Cálido"])
        else:
            region_colors_original.append(colors["Neutro"])
    else:
        # Si la región está vacía o tiene un punto en el infinito, asignar un color (por ejemplo, blanco)
        region_colors_original.append([1.0, 1.0, 0.0])

# Visualizar el fractal de Voronoi con colores específicos
fig, ax = plt.subplots(figsize=(8, 8))

# Dibujar manualmente las regiones con colores específicos
for region, color in zip(regions, region_colors_original):
    if -1 not in region and len(region) > 0:
        # Obtener las coordenadas del polígono de la región
        polygon = vertices[region]

        # Plotear el polígono con el color específico
        ax.fill(polygon[:, 0], polygon[:, 1], facecolor=color, edgecolor='k', linewidth=1, alpha=0.6)

ax.set_xlim([0, 1])
ax.set_ylim([0, 1])

ax.set_title('Fractal de Voronoi - Clima Actual')
if not os.path.exists("images"):
    os.makedirs("images")

# Guardar la imagen original en la carpeta "images"
plt.savefig('images/Clima_Actual.png')
plt.show()

# Obtener los estados actuales directamente del fractal original
estados_actuales = [list(colors.values()).index(color) for color in region_colors_original]

# Aplicar la cadena de Markov a cada región
estados_siguientes = [np.argmax(matriz_transicion[estado, :]) for estado in estados_actuales]

# Visualizar el nuevo fractal con colores específicos según la cadena de Markov
fig, ax = plt.subplots(figsize=(8, 8))

# Dibujar manualmente las regiones con colores específicos según la cadena de Markov
for region, estado in zip(regions, estados_siguientes):
    if -1 not in region and len(region) > 0:
        # Obtener las coordenadas del polígono de la región
        polygon = vertices[region]

        # Asignar color según el estado predicho
        color = {
            0: [0.5, 0.5, 0.5],  # Gris
            1: [0.0, 0.0, 1.0],  # Azul
            2: [1.0, 1.0, 0.0]   # Amarillo
        }[estado]

        # Plotear el polígono con el color específico
        ax.fill(polygon[:, 0], polygon[:, 1], facecolor=color, edgecolor='k', linewidth=1, alpha=0.6)

ax.set_xlim([0, 1])
ax.set_ylim([0, 1])

ax.set_title('Fractal de Voronoi con Estados Predichos por la Cadena de Markov')
if not os.path.exists("images"):
    os.makedirs("images")

# Guardar la imagen con la cadena de Markov aplicada en la carpeta "images"
plt.savefig('images/Dia_Siguiente.png')
plt.show()

