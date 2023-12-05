import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from shapely.geometry import Point, Polygon
from celda import Celda
from generador import GeneradorPoblacion
import random

# Función para verificar si un punto está dentro de un hexágono densidad de poblacion
def punto_dentro_hexagono(punto, vertices_hexagono):
    #print(f'punto{punto}')
    hexagono = Polygon(vertices_hexagono)
    punto_shapely = Point(punto)
    return punto_shapely.within(hexagono)

def puntos_dentro(pts, vertices):
    pts_dentro = [p for p in pts if punto_dentro_hexagono(p, vertices)]
    return pts_dentro

def fitnes(pts, cells, num_particulas):
    fitnes_vector = []
    numero2 = num_particulas-1
    for i in range(len(cells)):
        suma_puntos = 0  # Inicializa la suma para cada partícula
        for j in range(len(cells)):
            # Suma la cantidad de puntos dentro del hexágono
            suma_puntos += len(puntos_dentro(pts, cells[i][j].get_vertices()))
        fitnes_vector.append(suma_puntos)
    return fitnes_vector

# Define the Rastrigin function
# def function(x, n):
#     #x = arreglo de exagonos
#     #n = numero de puntos para calcular porcentaje de cobertura en funcion de la poblacion
#     #for i in range(n):
        
#     return num=0

def grey_wolf_optimization(num_zonas, list_pts, cost_func, num_particles=5, max_iter=1, alpha=2.0, beta=1.5, delta=0.3):
    # Initialize wolves' positions
    wolves_positions = []

    for _ in range(num_zonas):
        wolves_position = []
        for _ in range(num_particles):
            wolves_position.append(Celda((random.randint(10, 100), random.randint(10, 100)), 20))
        wolves_positions.append(wolves_position)
    # Fitness of the first iteration
    fitnes_vals = fitnes(list_pts, wolves_positions, num_particles)

    # Initialize the best positions and fitness values
    best_positions = np.copy(wolves_positions)
    best_fitness = max(fitnes_vals)
    swarm_best_position = fitnes_vals.index(max(fitnes_vals))
    swarm_best_fitness = max(fitnes_vals)

    # Iterate through the specified number of iterations
    for iteration in range(max_iter):
        print(f'iteracion: {iteration}')
        for i in range(num_zonas):
            for j in range(num_particles):  # Fix here
                # Update the position of each wolf using the GWO formula
                a = 2 * (iteration / max_iter) - 1
                A1 = 2 * alpha * np.random.rand() - alpha
                C1 = 2 * np.random.rand()
                D_alpha = np.abs(C1 * np.multiply(np.array(best_positions[i][j].get_vertices()), -np.array(wolves_positions[i][j].get_vertices())))
                X1 = best_positions[i][j].get_vertices() - A1 * D_alpha

                B = 2 * (iteration / max_iter) - 1
                A2 = 2 * beta * np.random.rand() - beta
                C2 = 2 * np.random.rand()
                D_beta = np.abs(C2 * np.multiply(np.array(best_positions[i][j].get_vertices()), -np.array(wolves_positions[i][j].get_vertices())))
                X2 = best_positions[i][j].get_vertices() - A2 * D_beta

                C = 2 * (iteration / max_iter) - 1
                A3 = 2 * delta * np.random.rand() - delta
                C3 = 2 * np.random.rand()
                D_delta = np.abs(C3 * np.multiply(np.array(best_positions[i][j].get_vertices()), -np.array(wolves_positions[i][j].get_vertices())))
                X3 = best_positions[i][j].get_vertices() - A3 * D_delta

                # Update the position of the wolf
                wolves_positions[i][j].set_vertices((X1 + X2 + X3) / 3.0)

        # Evaluate fitness of each wolf
        fitness_values = fitnes(list_pts, wolves_positions, num_particles)

        maxfit = max(fitness_values)

        # Update best positions and fitness values
        maxfit = max(fitness_values)
        improved_index = np.argmin(fitness_values)  # Cambiar a np.argmin

        if maxfit < best_fitness:
            best_positions[improved_index] = wolves_positions[improved_index]
            best_fitness = maxfit

        swarm_best_position = np.argmax(fitness_values)  # Cambiar a np.argmax
        swarm_best_fitness = max(fitness_values)

    # Return the best solution found by the GWO algorithm
    return swarm_best_position, swarm_best_fitness, best_positions


##cuerpo principal de la funcion:
# Parámetros
numero_zonas = 5#mapa de densidad de poblacion
puntos_por_zona = 100
media_distribucion = 25
desviacion_estandar_distribucion = 5
ancho_area = 50
alto_area = 50
lista_celdas = []

# Crear instancia de la clase y generar y visualizar población
generador = GeneradorPoblacion(numero_zonas, puntos_por_zona, media_distribucion, desviacion_estandar_distribucion, ancho_area, alto_area)
generador.generar_y_visualizar_poblacion(numero_zonas)

# Obtener puntos generados
pts_poblacion = generador.obtener_puntos_generados()

# Convertir la lista de puntos a un array bidimensional
pts_poblacion_array = np.array(pts_poblacion)

#print(pts_poblacion)


# print(type(lista_celdas))

# print(type(lista_celdas[1]))

# Ejecutar el algoritmo GWO
best_solution, best_fitness, best_positions = grey_wolf_optimization(numero_zonas, pts_poblacion, fitnes, num_particles=30, max_iter=10)
print("Mejor solución encontrada:", best_solution)
print("Mejor fitness encontrado:", best_fitness)

# Obtener las coordenadas de los hexágonos que dan la mejor solución
best_hexagons_coords = [cell.get_vertices() for cell in best_positions[best_solution]]

# Calcular fitness de cada hexágono
fitness_hexagons = fitnes(pts_poblacion, best_positions, 30)

# Ordenar hexágonos por rendimiento
sorted_hexagons = [x for _, x in sorted(zip(fitness_hexagons, best_hexagons_coords), reverse=True)]

# Tomar los 5 mejores hexágonos
top_5_hexagons = sorted_hexagons[:5]

# Visualizar la población, los hexágonos que dan la mejor solución y los puntos utilizados
generador.generar_y_visualizar_poblacion(numero_zonas)

# Dibujar los mejores hexágonos
for hexagon_coords in top_5_hexagons:
    hexagon = plt.Polygon(hexagon_coords, fill=None, edgecolor='red')
    plt.gca().add_patch(hexagon)

# Dibujar puntos
plt.scatter(*zip(*pts_poblacion), marker='.', color='blue')

plt.show()