# cristhian correa - luis santana. taller parcial 2

import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
import matplotlib.pyplot as plt

historial_df = None

# Función para mostrar el dato actual de la casilla seleccionada
def mostrar_dato_actual():
    dato_seleccionado = obtener_dato_seleccionado()
    if dato_seleccionado:
        # Enviar solicitud para obtener el dato actual
        enviar_solicitud()
        # Mostrar el dato actual
        messagebox.showinfo("Dato Actual", f"El dato actual de {dato_seleccionado} es: {dato_actual.get(dato_seleccionado, 'N/A')}")
    else:
        messagebox.showerror("Error", "Por favor, seleccione al menos una opción de datos a visualizar.")

# Función para mostrar el historial de datos
def mostrar_historial():
    global historial_df
    dato_seleccionado = obtener_dato_seleccionado()
    if dato_seleccionado:
        # Filtrar el DataFrame para mostrar solo el historial del dato seleccionado
        historial_seleccionado = historial_df[["Fecha y hora", dato_seleccionado]]
        messagebox.showinfo("Historial", historial_seleccionado.to_string(index=False))
    else:
        messagebox.showerror("Error", "Por favor, seleccione al menos una opción de datos a visualizar.")

# Función para obtener el dato seleccionado
def obtener_dato_seleccionado():
    for i, var in enumerate(checkbox_vars):
        if var.get():
            return data_options[i]
    return None

# Función para enviar la solicitud y procesar los datos
def enviar_solicitud():
    global historial_df, dato_actual
    ciudad = city_name.get("1.0", "end-1c")
    if not ciudad:
        messagebox.showerror("Error", "Por favor, ingrese el nombre de la ciudad.")
        return
    
    datos_seleccionados = [data_options[i] for i, var in enumerate(checkbox_vars) if var.get()]
    if not datos_seleccionados:
        messagebox.showerror("Error", "Por favor, marque al menos una opción de datos a visualizar.")
        return
    
    # Mapeo de opciones seleccionadas a claves en data_h
    opciones_a_claves = {
        "Temperatura": "temp",
        "Sensación térmica": "feels_like",
        "Presión atmosférica": "pressure",
        "Humedad": "humidity",
        "Velocidad del viento": "speed",
        "Clima": "description"
    }
    
    API_key_C = 'adbfe9f6eaffe4548f33628903375789'
    url_clima = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_key_C}&units=metric&lang=es'
    url_historial = f'http://history.openweathermap.org/data/2.5/history/city?q={ciudad},CO&type=hour&appid={API_key_C}&units=metric&lang=es'

    response = requests.get(url_clima)
    if response.status_code == 200:     
        data = response.json()
        #print("Datos actuales:")
        # Limpiar dato_actual
        dato_actual = {}
        for dato in datos_seleccionados:
            if dato == "Velocidad del viento":
                velocidad_viento = data['wind'].get('speed', None)
                dato_actual[dato] = velocidad_viento
                #print(f"{dato}: {velocidad_viento}")
            elif dato == "Clima":
                clima = data['weather'][0].get('description', None)
                dato_actual[dato] = clima
                #print(f"{dato}: {clima}")
            elif dato in opciones_a_claves:
                clave = opciones_a_claves[dato]
                valor = data['main'].get(clave, None)
                dato_actual[dato] = valor
                #print(f"{dato}: {valor}")                
    else: 
        messagebox.showerror("Error", "La ciudad no se encontró. Por favor, ingrese el nombre correcto.")
        return  # Salir de la función si hay un error en la solicitud de clima
        
    response_h = requests.get(url_historial)
    if response_h.status_code == 200:     
        data_h = response_h.json()
        #print("Historial:")
        # Crear un DataFrame vacío
        historial_df = pd.DataFrame()
        
        # Agregar siempre la columna 'Fecha y hora'
        historial_df['Fecha y hora'] = [pd.Timestamp.fromtimestamp(data['dt']) for data in data_h['list']]
        
        for dato in datos_seleccionados:
            if dato == "Velocidad del viento":
                historial_df[dato] = [data['wind'].get('speed', None) for data in data_h['list']]
            elif dato == "Clima":
                historial_df[dato] = [data['weather'][0].get('description', None) for data in data_h['list']]
            elif dato in opciones_a_claves:
                clave = opciones_a_claves[dato]
                historial_df[dato] = [data['main'].get(clave, None) for data in data_h['list']]
        #print(historial_df)  # Imprime el DataFrame
    else: 
        messagebox.showerror("Error", "Historial no encontrado")
        return  # Salir de la función si hay un error en la solicitud del historial

def cerrar_ventana():
    window.destroy()

def graficar_historial():
    # Obtener los datos seleccionados
    datos_seleccionados = [dato for dato, var in zip(data_options, checkbox_vars) if var.get()]
    
    # Filtrar el DataFrame para incluir solo las columnas seleccionadas
    datos_para_graficar = historial_df[["Fecha y hora"] + datos_seleccionados]
    
    # Establecer la columna 'Fecha y hora' como el índice
    datos_para_graficar.set_index("Fecha y hora", inplace=True)
    
    # Graficar los datos
    datos_para_graficar.plot(kind='line', figsize=(10, 6))
    plt.title('Datos Históricos del Clima')
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Valor')
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()

window = tk.Tk()
window.title("Verificación del Clima")

frame = tk.Frame(window)
frame.pack(padx=20, pady=20)

city_label = tk.Label(frame, text="Ingrese el nombre de la ciudad:")
city_label.grid(row=0, column=0, sticky="e")

city_name = tk.Text(frame, width=25, height=1)
city_name.grid(row=0, column=1, sticky="e")

data_label = tk.Label(frame, text="Selecciona los datos a visualizar:")
data_label.grid(row=1, column=0, columnspan=2, pady=10)

checkbox_vars = []
data_options = ["Temperatura", "Sensación térmica", "Presión atmosférica", "Humedad", "Velocidad del viento", "Clima"]
for i, option in enumerate(data_options):
    var = tk.BooleanVar()
    checkbox_vars.append(var)
    checkbox = tk.Checkbutton(frame, text=option, variable=var)
    checkbox.grid(row=i+2, column=0, columnspan=2, sticky="w")

mostrar_dato_button = tk.Button(frame, text="Mostrar Dato Actual", command=mostrar_dato_actual)
mostrar_dato_button.grid(row=len(data_options)+2, column=0, pady=10)

mostrar_historial_button = tk.Button(frame, text="Mostrar Historial", command=mostrar_historial)
mostrar_historial_button.grid(row=len(data_options)+2, column=1, pady=10)

cerrar_button = tk.Button(window, text="Cerrar", command=cerrar_ventana)
cerrar_button.pack(side="bottom", padx=10, pady=10, anchor="se")

# Variable para almacenar el dato actual
dato_actual = {}

# Agregar botón para graficar
graficar_button = tk.Button(frame, text="Graficar Historial", command=graficar_historial)
graficar_button.grid(row=len(data_options)+3, columnspan=2, pady=10)

window.mainloop() #este
