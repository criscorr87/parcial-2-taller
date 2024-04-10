//Cristian Correa Leon      1130613337
//Luis Santana              1144105923

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define MAX_DATOS 100

// Definición de la estructura Sensor
typedef struct {
    time_t timestamp;
    float temperatura;
    float humedad;
} Sensor;

// Prototipos de funciones
void calcular_estadisticas(Sensor datos[], int contador, float temp_limite_min, float temp_limite_max, float humd_limite_min, float humd_limite_max);
void escribir_analisis(Sensor datos[], int contador, int tiempo_total_datos, int tiempo_total_fuera_limites, float temp_max, float temp_min, float humd_max, float humd_min, time_t hora_temp_max, time_t hora_temp_min, time_t hora_humd_max, time_t hora_humd_min);
float calcular_punto_rocio(float temperatura, float humedad);

int main() {
    FILE *archivo;
    char linea[100]; 
    Sensor datos[MAX_DATOS];
    int contador = 0;
    float temp_limite_min, temp_limite_max, humd_limite_min, humd_limite_max;
    char respuesta;

    archivo = fopen("Datos_de_Sensor.txt", "r");

    if (archivo == NULL) {
        perror("Error al abrir el archivo");
        return 1;
    }

    // Ignorar la primera línea (encabezado)
    fgets(linea, 100, archivo); 

    while (fgets(linea, 100, archivo) != NULL && contador < MAX_DATOS) { 
        sscanf(linea, "%ld,%f,%f", &datos[contador].timestamp, &datos[contador].temperatura, &datos[contador].humedad);
        contador++;
    }

    fclose(archivo);

    printf("¿Desea establecer límites para la temperatura y la humedad? (s/n): ");
    scanf(" %c", &respuesta);

    if (respuesta == 's' || respuesta == 'S') {
        printf("Ingrese el límite inferior de temperatura: ");
        scanf("%f", &temp_limite_min);
        printf("Ingrese el límite superior de temperatura: ");
        scanf("%f", &temp_limite_max);
        printf("Ingrese el límite inferior de humedad: ");
        scanf("%f", &humd_limite_min);
        printf("Ingrese el límite superior de humedad: ");
        scanf("%f", &humd_limite_max);

        // Calcular estadísticas con límites
        calcular_estadisticas(datos, contador, temp_limite_min, temp_limite_max, humd_limite_min, humd_limite_max);
    } else {
        // Calcular estadísticas sin límites
        calcular_estadisticas(datos, contador, -INFINITY, INFINITY, -INFINITY, INFINITY);
    }

    return 0;
}

// Función para calcular y mostrar las estadísticas de temperatura y humedad
void calcular_estadisticas(Sensor datos[], int contador, float temp_limite_min, float temp_limite_max, float humd_limite_min, float humd_limite_max) {
    float temp_max = -INFINITY;
    float temp_min = INFINITY;
    float humd_max = -INFINITY;
    float humd_min = INFINITY;
    time_t hora_temp_max = 0;
    time_t hora_temp_min = 0;
    time_t hora_humd_max = 0;
    time_t hora_humd_min = 0;
    float temp_suma = 0;
    float humd_suma = 0;
    int contador_validos = 0;
    int tiempo_total_fuera_limites = 0;
    time_t tiempo_inicio_fuera_limites = 0;
    time_t tiempo_fin_fuera_limites = 0;

    for (int i = 0; i < contador; i++) {
        if (datos[i].temperatura >= temp_limite_min && datos[i].temperatura <= temp_limite_max &&
            datos[i].humedad >= humd_limite_min && datos[i].humedad <= humd_limite_max) {
            contador_validos++;
            if (datos[i].temperatura > temp_max) {
                temp_max = datos[i].temperatura;
                hora_temp_max = datos[i].timestamp;
            }
            if (datos[i].temperatura < temp_min) {
                temp_min = datos[i].temperatura;
                hora_temp_min = datos[i].timestamp;
            }
            if (datos[i].humedad > humd_max) {
                humd_max = datos[i].humedad;
                hora_humd_max = datos[i].timestamp;
            }
            if (datos[i].humedad < humd_min) {
                humd_min = datos[i].humedad;
                hora_humd_min = datos[i].timestamp;
            }
            temp_suma += datos[i].temperatura;
            humd_suma += datos[i].humedad;
        } else {
            // Incrementar tiempo fuera de los límites
            if (tiempo_inicio_fuera_limites == 0) {
                tiempo_inicio_fuera_limites = datos[i].timestamp;
            }
            tiempo_fin_fuera_limites = datos[i].timestamp;
        }
    }

    // Calcular tiempo total de los datos
    time_t tiempo_inicio = datos[0].timestamp;
    time_t tiempo_fin = datos[contador - 1].timestamp;
    int tiempo_total_datos = difftime(tiempo_fin, tiempo_inicio);

    // Calcular tiempo total fuera de los límites
    if (tiempo_inicio_fuera_limites != 0 && tiempo_fin_fuera_limites != 0) {
        tiempo_total_fuera_limites = difftime(tiempo_fin_fuera_limites, tiempo_inicio_fuera_limites);
    }

    // Verificar si hay datos válidos antes de calcular el promedio
    if (contador_validos > 0) {
        float temp_promedio = temp_suma / contador_validos;
        float humd_promedio = humd_suma / contador_validos;

        printf("Cantidad de datos: %d\n", contador);
        printf("Tiempo total de los datos: %d segundos\n", tiempo_total_datos);
        printf("Temperatura máxima: %.2f, Hora: %s", temp_max, asctime(localtime(&hora_temp_max)));
        printf("Temperatura mínima: %.2f, Hora: %s", temp_min, asctime(localtime(&hora_temp_min)));
        printf("Humedad máxima: %.2f, Hora: %s", humd_max, asctime(localtime(&hora_humd_max)));
        printf("Humedad mínima: %.2f, Hora: %s", humd_min, asctime(localtime(&hora_humd_min)));
        printf("Promedio de temperatura: %.2f\n", temp_promedio);
        printf("Promedio de humedad: %.2f\n", humd_promedio);
        printf("Tiempo total fuera de los límites: %d segundos\n", tiempo_total_fuera_limites);

        float punto_rocio = calcular_punto_rocio(temp_promedio, humd_promedio);
        printf("Punto de rocío promedio: %.2f\n", punto_rocio);

        // Escribir análisis en un archivo CSV
        escribir_analisis(datos, contador, tiempo_total_datos, tiempo_total_fuera_limites, temp_max, temp_min, humd_max, humd_min, hora_temp_max, hora_temp_min, hora_humd_max, hora_humd_min);
    } else {
        printf("No hay datos válidos dentro de los límites especificados.\n");
    }
}

// Función para escribir los resultados del análisis en un archivo CSV
void escribir_analisis(Sensor datos[], int contador, int tiempo_total_datos, int tiempo_total_fuera_limites, float temp_max, float temp_min, float humd_max, float humd_min, time_t hora_temp_max, time_t hora_temp_min, time_t hora_humd_max, time_t hora_humd_min) {
    FILE *archivo;
    archivo = fopen("analytics.csv", "w");

    if (archivo == NULL) {
        perror("Error al abrir el archivo analytics.csv");
        exit(EXIT_FAILURE);
    }

    fprintf(archivo, "Variable,Valor\n");
    fprintf(archivo, "Cantidad de datos,%d\n", contador);
    fprintf(archivo, "Tiempo total de los datos,%d segundos\n", tiempo_total_datos);
    fprintf(archivo, "Tiempo total fuera de los límites,%d segundos\n", tiempo_total_fuera_limites);
    fprintf(archivo, "Temperatura máxima,%.2f, Hora,%s", temp_max, asctime(localtime(&hora_temp_max)));
    fprintf(archivo, "Temperatura mínima,%.2f, Hora,%s", temp_min, asctime(localtime(&hora_temp_min)));
    fprintf(archivo, "Humedad máxima,%.2f, Hora,%s", humd_max, asctime(localtime(&hora_humd_max)));
    fprintf(archivo, "Humedad mínima,%.2f, Hora,%s", humd_min, asctime(localtime(&hora_humd_min)));

    fclose(archivo);
}

// Función para calcular el punto de rocío
float calcular_punto_rocio(float temperatura, float humedad) {
    const float b = 17.67;
    const float c = 243.5;
    float punto_rocio = c * (log(humedad / 100.0) + ((b * temperatura) / (c + temperatura))) / (b - (log(humedad / 100.0) + ((b * temperatura) / (c + temperatura))));
    return punto_rocio;
}
