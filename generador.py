import matplotlib.pyplot as plt
import numpy as np
import random

class GeneradorPoblacion:
    def __init__(self, numero_zonas, puntos_por_zona, media, desviacion_estandar, ancho, alto):
        self.numero_zonas = numero_zonas
        self.puntos_por_zona = puntos_por_zona
        self.media = media
        self.desviacion_estandar = desviacion_estandar
        self.ancho = ancho
        self.alto = alto
        self.pts = []

    def generar_puntos_distribucion_normal(self):
        x = np.random.normal(loc=self.media, scale=self.desviacion_estandar, size=self.puntos_por_zona)
        y = np.random.normal(loc=self.media, scale=self.desviacion_estandar, size=self.puntos_por_zona)

        # Asegurar que los puntos estén dentro del área rectangular
        x = np.clip(x, 0, self.ancho)
        y = np.clip(y, 0, self.alto)

        puntos = np.column_stack((x, y))
        return puntos

    def generar_puntos_aleatorios_en_area(self):
        x = np.random.uniform(0, self.ancho, size=self.puntos_por_zona)
        y = np.random.uniform(0, self.alto, size=self.puntos_por_zona)

        puntos = np.column_stack((x, y))
        return puntos

    def generar_zonas_poblacion(self):
        centros_zonas = np.random.rand(self.numero_zonas, 2) * np.array([self.ancho, self.alto])
        return centros_zonas

    def generar_y_visualizar_poblacion(self, s):
        centros_zonas = self.generar_zonas_poblacion()

        plt.figure(figsize=(8, 8))

        for centro in centros_zonas:
            puntos_generados = self.generar_puntos_distribucion_normal()
            puntos_generados[:, 0] += centro[0]
            puntos_generados[:, 1] += centro[1]

            # Guardar las coordenadas de los puntos en la lista
            self.pts.extend(puntos_generados.tolist())

            plt.scatter(puntos_generados[:, 0], puntos_generados[:, 1], s)

        puntos_aleatorios = self.generar_puntos_aleatorios_en_area()

        # Guardar las coordenadas de los puntos aleatorios en la lista
        self.pts.extend(puntos_aleatorios.tolist())

        # plt.title("Densidad de poblacion generada")
        # plt.xlabel("X")
        # plt.ylabel("Y")
        # plt.show()

    def obtener_puntos_generados(self):
        print(type(self.pts))
        return self.pts

# # Parámetros
# numero_zonas = 5
# puntos_por_zona = 100
# media_distribucion = 25
# desviacion_estandar_distribucion = 5
# ancho_area = 50
# alto_area = 50

# # Crear instancia de la clase y generar y visualizar población
# generador = GeneradorPoblacion(numero_zonas, puntos_por_zona, media_distribucion, desviacion_estandar_distribucion, ancho_area, alto_area)
# generador.generar_y_visualizar_poblacion()

# # Obtener puntos generados
# todos_los_puntos = generador.obtener_puntos_generados()

# print(todos_los_puntos)