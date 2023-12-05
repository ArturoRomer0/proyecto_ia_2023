import matplotlib.pyplot as plt
import numpy as np
#sirve para manejar las celdas los puntos de la poblacion y los hexagonos se van actualizando con lobo gris
class Celda:
    def __init__(self, centro, radio):
        self.centro = centro
        self.radio = radio
        self.calcular_coordenadas()

    def calcular_coordenadas(self):
        angulos = np.linspace(0, 2 * np.pi, 7)
        self.coordenadas_x = self.centro[0] + self.radio * np.cos(angulos)
        self.coordenadas_y = self.centro[1] + self.radio * np.sin(angulos)

        # Cerrar el hexágono agregando el primer vértice al final
        self.coordenadas_x = np.append(self.coordenadas_x, self.coordenadas_x[0])
        self.coordenadas_y = np.append(self.coordenadas_y, self.coordenadas_y[0])

    def get_vertices(self):
        return list(zip(self.coordenadas_x, self.coordenadas_y))
    
    def getCentro(self):
        return self.centro
    
    def set_vertices(self, vertices):
        self.vertices = vertices

# # Ejemplo de uso
# centro_celda = (50, 50)
# radio_celda = 30

# # Crear instancia de la clase
# celda = Celda(centro_celda, radio_celda)

# # Acceder a los vértices desde fuera de la clase
# vertices_celda = celda.vertices
# print("Vértices de la celda:", vertices_celda)

# # Graficar la celda
# plt.figure(figsize=(6, 6))
# celda.graficar_celda()
# plt.title("Hexágono Generado por la Clase Celda")
# plt.xlabel("X")
# plt.ylabel("Y")
# plt.show()