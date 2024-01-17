import json
import os 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def cargar_datos(archivo_path):
    with open(os.path.join(extract_path, 'file.json'), 'r') as archivo:
        datos = json.load(archivo)
    return datos

extract_path = "extracted_files"
# Suponiendo que hay un archivo JSON llamado 'datos.json' en lugar del archivo ZIP
archivo_datos = os.path.join(extract_path, "file.json")

# Carga los datos desde el archivo JSON
datos = cargar_datos(archivo_datos)

#DISTANCIA MÁXIMA
#Calcula la distancia máxima (eje x) de las trayectorias
def calcular_distancia_maxima(lanzamiento):
    distancia_maxima = max(lanzamiento, key=lambda x: x[2])
    return distancia_maxima

def distancia_maxima_lanzamientos(lanzamientos):
    distancias_maximas = [calcular_distancia_maxima(lanzamiento) for lanzamiento in lanzamientos]
    return distancias_maximas

distancias_maximas = distancia_maxima_lanzamientos(datos)

print("Distancias máximas de cada lanzamiento:")
for i, distancia_maxima in enumerate(distancias_maximas, 1):
    print(f"Lanzamiento {i}: Tiempo={distancia_maxima[0]}, Altura={distancia_maxima[1]}, Distancia={distancia_maxima[2]}")

#ALTURA MÁXIMA
# Calcula la altura máxima que alcanzan las trayectorias (eje y)

def calcular_altura_maxima(lanzamiento):
    # Encuentra la altura máxima (valor máximo en el eje Y) para un lanzamiento
    altura_maxima = max(lanzamiento, key=lambda x: x[1])
    return altura_maxima

def altura_maxima_lanzamientos(lanzamientos):
    # Calcula la altura máxima para cada lanzamiento
    alturas_maximas = [calcular_altura_maxima(lanzamiento) for lanzamiento in lanzamientos]
    return alturas_maximas

alturas_maximas = altura_maxima_lanzamientos(datos)

# Muestra las alturas máximas para cada lanzamiento
print("Alturas máximas de cada lanzamiento:")
for i, altura_maxima in enumerate(alturas_maximas, 1):
    print(f"Lanzamiento {i}: Tiempo={altura_maxima[0]}, Altura={altura_maxima[1]}, Distancia={altura_maxima[2]}")

#TIEMPO DE VUELO EXCEDIDO
#Calcula si alguna de las trayectorias sigue en el aire después de un límite de tiempo
def lanzamiento_tiempo_excedido(lanzamientos, tiempo_limite):
    lanzamiento_excedido = None

    for lanzamiento in lanzamientos:
        tiempo_vuelo = lanzamiento[-1][0]
        if tiempo_vuelo > tiempo_limite:
            lanzamiento_excedido = lanzamiento
            break  # Detener la búsqueda después del primer lanzamiento que excede el tiempo límite

    return lanzamiento_excedido

tiempo_limite = float(input("Ingrese el tiempo límite para el lanzamiento (segundos): "))
lanzamiento_excedido = lanzamiento_tiempo_excedido(datos, tiempo_limite)

if lanzamiento_excedido:
    print(f"Lanzamiento con tiempo de vuelo excedido ({tiempo_limite} segundos):")
    print(f"Tiempo de vuelo: {lanzamiento_excedido[-1][0]} segundos")
    print(f"Altura máxima: {max(lanzamiento_excedido, key=lambda x: x[1])[1]} unidades de altura")
    print(f"Distancia total: {lanzamiento_excedido[-1][2]} unidades de distancia")
else:
    print(f"Ningún lanzamiento excedió el tiempo de vuelo de {tiempo_limite} segundos.")

#ANÁLISIS TRAYECTORIAS
def analisis_trayectorias(lanzamientos):
    duraciones = [lanzamiento[-1][0] for lanzamiento in lanzamientos]  # Tiempo del último punto para cada lanzamiento
    alturas_maximas = [max(lanzamiento, key=lambda x: x[1])[1] for lanzamiento in lanzamientos]
    distancias_totales = [lanzamiento[-1][2] for lanzamiento in lanzamientos]  # Distancia del último punto para cada lanzamiento

    duracion_promedio = sum(duraciones) / len(duraciones)
    altura_maxima_promedio = sum(alturas_maximas) / len(alturas_maximas)
    distancia_total_promedio = sum(distancias_totales)

    print(f"Duración promedio del vuelo: {duracion_promedio} segundos")
    print(f"Altura máxima promedio: {altura_maxima_promedio} unidades de altura")
    print(f"Distancia total promedio: {distancia_total_promedio} unidades de distancia")

analisis_trayectorias(datos)

#GRÁFICA A TIEMPO REAL
#Crea una gráica en 3D que simula las trayectorias
def update(frame):
    # Función de actualización para la animación
    plt.cla()  # Borra la gráfica anterior
    for lanzamiento in datos[:frame]:
        # Grafica cada lanzamiento hasta el frame actual
        tiempos = [punto[0] for punto in lanzamiento]
        alturas = [punto[1] for punto in lanzamiento]
        distancias = [punto[2] for punto in lanzamiento]
        plt.plot(tiempos, alturas, label='Altura')
        plt.plot(tiempos, distancias, label='Distancia')

    plt.xlabel('Tiempo')
    plt.ylabel('Altura / Distancia')
    plt.title('Gráfica en tiempo real')
    plt.legend()

# Carga los datos desde el archivo
datos = cargar_datos(archivo_datos)

# Configura la animación
num_frames = len(datos)
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update, frames=num_frames, repeat=False)

plt.show()