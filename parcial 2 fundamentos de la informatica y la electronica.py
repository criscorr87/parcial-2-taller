import tkinter as tk
from tkinter import messagebox
import requests

def enviar_solicitud():
    ciudad = city_name.get("1.0", "end-1c")
    if not ciudad:
        messagebox.showerror("Error", "Por favor, ingrese el nombre de la ciudad.")
        return
    
    datos_seleccionados = [data_options[i] for i, var in enumerate(checkbox_vars) if var.get()]
    if not datos_seleccionados:
        messagebox.showerror("Error", "Por favor, marque al menos una opción de datos a visualizar.")
        return
    
    API_key_C = 'adbfe9f6eaffe4548f33628903375789'
    url_clima = f'https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_key_C}&units=metric&lang=es'
    url_historial = f'http://history.openweathermap.org/data/2.5/history/city?q={ciudad},CO&type=hour&appid={API_key_C}&lang=es'

    response = requests.get(url_clima)
    if response.status_code == 200:     
        data = response.json()
        for dato in datos_seleccionados:
            if dato == "Clima":
                print('El clima es', data['weather'][0]['description'])
            elif dato == "Temperatura Actual":
                print('Temperatura Actual', data['main']['temp'])
            elif dato == "Temperatura Real":
                print('La temperatura actual se siente como', data['main']['feels_like'])
            elif dato == "Humedad":
                print('La humedad es', data['main']['humidity'])
    else: 
        messagebox.showerror("Error", "La ciudad no se encontró. Por favor, ingrese el nombre correcto.")
        
    response_h = requests.get(url_historial)
    if response_h.status_code == 200:     
        data_h = response_h.json()
        for dato in data_h['list']:  
            print("Fecha y hora (timestamp):", dato['dt'])
            print("Temperatura:", str(dato['main']['temp']))
            print("Sensación térmica:", str(dato['main']['feels_like']))
            print("Presión atmosférica:", str(dato['main']['pressure']))
            print("Humedad:", str(dato['main']['humidity']))
            print("Velocidad del viento:", str(dato['wind']['speed']))
            print("Descripción del clima:", str(dato['weather'][0]['description']))
            print("")

    else: 
        messagebox.showerror("Error", "Historial no encontrado")


def cerrar_ventana():
    window.destroy()

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
data_options = ["Clima", "Temperatura Actual", "Temperatura Real", "Humedad"]
for i, option in enumerate(data_options):
    var = tk.BooleanVar()
    checkbox_vars.append(var)
    checkbox = tk.Checkbutton(frame, text=option, variable=var)
    checkbox.grid(row=i+2, column=0, columnspan=2, sticky="w")

enviar_button = tk.Button(frame, text="Enviar Solicitud", command=enviar_solicitud)
enviar_button.grid(row=len(data_options)+2, columnspan=2, pady=10)

cerrar_button = tk.Button(window, text="Cerrar", command=cerrar_ventana)
cerrar_button.pack(side="bottom", padx=10, pady=10, anchor="se")

window.mainloop()