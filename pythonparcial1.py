import time
import math

MAX_DATOS = 100

class Sensor:
    def __init__(self, timestamp, temperatura, humedad):
        self.timestamp = timestamp
        self.temperatura = temperatura
        self.humedad = humedad

def calcular_estadisticas(datos, contador, temp_limite_min, temp_limite_max, humd_limite_min, humd_limite_max):
    temp_max = float('-inf')
    temp_min = float('inf')
    humd_max = float('-inf')
    humd_min = float('inf')
    hora_temp_max = 0
    hora_temp_min = 0
    hora_humd_max = 0
    hora_humd_min = 0
    temp_suma = 0
    humd_suma = 0
    contador_validos = 0
    tiempo_total_fuera_limites = 0
    tiempo_inicio_fuera_limites = 0
    tiempo_fin_fuera_limites = 0

    for dato in datos:
        if temp_limite_min <= dato.temperatura <= temp_limite_max and humd_limite_min <= dato.humedad <= humd_limite_max:
            contador_validos += 1
            if dato.temperatura > temp_max:
                temp_max = dato.temperatura
                hora_temp_max = dato.timestamp
            if dato.temperatura < temp_min:
                temp_min = dato.temperatura
                hora_temp_min = dato.timestamp
            if dato.humedad > humd_max:
                humd_max = dato.humedad
                hora_humd_max = dato.timestamp
            if dato.humedad < humd_min:
                humd_min = dato.humedad
                hora_humd_min = dato.timestamp
            temp_suma += dato.temperatura
            humd_suma += dato.humedad
        else:
            if tiempo_inicio_fuera_limites == 0:
                tiempo_inicio_fuera_limites = dato.timestamp
            tiempo_fin_fuera_limites = dato.timestamp

    tiempo_inicio = datos[0].timestamp
    tiempo_fin = datos[contador - 1].timestamp
    tiempo_total_datos = tiempo_fin - tiempo_inicio

    if tiempo_inicio_fuera_limites != 0 and tiempo_fin_fuera_limites != 0:
        tiempo_total_fuera_limites = tiempo_fin_fuera_limites - tiempo_inicio_fuera_limites

    if contador_validos > 0:
        temp_promedio = temp_suma / contador_validos
        humd_promedio = humd_suma / contador_validos

        print("Cantidad de datos:", contador)
        print("Tiempo total de los datos:", tiempo_total_datos, "segundos")
        print("Temperatura máxima:", temp_max, ", Hora:", time.asctime(time.localtime(hora_temp_max)))
        print("Temperatura mínima:", temp_min, ", Hora:", time.asctime(time.localtime(hora_temp_min)))
        print("Humedad máxima:", humd_max, ", Hora:", time.asctime(time.localtime(hora_humd_max)))
        print("Humedad mínima:", humd_min, ", Hora:", time.asctime(time.localtime(hora_humd_min)))
        print("Promedio de temperatura:", temp_promedio)
        print("Promedio de humedad:", humd_promedio)
        print("Tiempo total fuera de los límites:", tiempo_total_fuera_limites, "segundos")

        punto_rocio = calcular_punto_rocio(temp_promedio, humd_promedio)
        print("Punto de rocío promedio:", punto_rocio)

        escribir_analisis(datos, contador, tiempo_total_datos, tiempo_total_fuera_limites, temp_max, temp_min, humd_max, humd_min, hora_temp_max, hora_temp_min, hora_humd_max, hora_humd_min)
    else:
        print("No hay datos válidos dentro de los límites especificados.")

def escribir_analisis(datos, contador, tiempo_total_datos, tiempo_total_fuera_limites, temp_max, temp_min, humd_max, humd_min, hora_temp_max, hora_temp_min, hora_humd_max, hora_humd_min):
    with open("analytics.csv", "w") as archivo:
        archivo.write("Variable,Valor\n")
        archivo.write(f"Cantidad de datos,{contador}\n")
        archivo.write(f"Tiempo total de los datos,{tiempo_total_datos} segundos\n")
        archivo.write(f"Tiempo total fuera de los límites,{tiempo_total_fuera_limites} segundos\n")
        archivo.write(f"Temperatura máxima,{temp_max}, Hora,{time.asctime(time.localtime(hora_temp_max))}\n")
        archivo.write(f"Temperatura mínima,{temp_min}, Hora,{time.asctime(time.localtime(hora_temp_min))}\n")
        archivo.write(f"Humedad máxima,{humd_max}, Hora,{time.asctime(time.localtime(hora_humd_max))}\n")
        archivo.write(f"Humedad mínima,{humd_min}, Hora,{time.asctime(time.localtime(hora_humd_min))}\n")

def calcular_punto_rocio(temperatura, humedad):
    b = 17.67
    c = 243.5
    punto_rocio = c * (math.log(humedad / 100.0) + ((b * temperatura) / (c + temperatura))) / (b - (math.log(humedad / 100.0) + ((b * temperatura) / (c + temperatura))))
    return punto_rocio

def main():
    datos = []
    contador = 0
    temp_limite_min, temp_limite_max, humd_limite_min, humd_limite_max = None, None, None, None
    respuesta = input("¿Desea establecer límites para la temperatura y la humedad? (s/n): ")

    with open("Datos_de_Sensor.txt", "r") as archivo:
        archivo.readline()  # Ignorar la primera línea (encabezado)
        for linea in archivo:
            timestamp, temperatura, humedad = map(float, linea.strip().split(","))
            datos.append(Sensor(int(timestamp), temperatura, humedad))
            contador += 1
            if contador >= MAX_DATOS:
                break

    if respuesta.lower() == 's':
        temp_limite_min = float(input("Ingrese el límite inferior de temperatura: "))
        temp_limite_max = float(input("Ingrese el límite superior de temperatura: "))
        humd_limite_min = float(input("Ingrese el límite inferior de humedad: "))
        humd_limite_max = float(input("Ingrese el límite superior de humedad: "))

    if temp_limite_min is not None and temp_limite_max is not None and humd_limite_min is not None and humd_limite_max is not None:
        calcular_estadisticas(datos, contador, temp_limite_min, temp_limite_max, humd_limite_min, humd_limite_max)
    else:
        calcular_estadisticas(datos, contador, float('-inf'), float('inf'), float('-inf'), float('inf'))

if __name__ == "__main__":
    main()

