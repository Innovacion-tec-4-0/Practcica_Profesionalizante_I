#script.py Se encarga de recibir datos de sensores a través de MQTT y almacenarlos en un archivo JSON, así como en una base de datos
import json
import os
import paho.mqtt.client as mqtt
from datetime import datetime
from conexion_db import Conexion
import conexion_db
import DB.pruebas.data_recept as data_recept
# Asegúrate de que este módulo aún sea necesario

# Tópicos
topico_temperatura = "sala/temperatura"
topico_humedad = "sala/humedad"
topico_led = "sala/led"
topico_luz = "sala/luz"
topico_movimiento = "sala/movimiento"
topico_potenciometro = "sala/potenciometro"
topico_ventilacion = "sala/ventilacion"
topico_pir = "sala/pir"
topico_aviso_humedad = "sala/aviso_humedad"

# ID del sistema
id = "SiMonAmMu"

# Crear el cliente MQTT
suscriptor = mqtt.Client()
conexion = Conexion()

# Define el archivo JSON
json_file_path = "datos_sensores.json"

def guardar_datos(sensor):
    # Verifica si el archivo existe
    if not os.path.exists(json_file_path):
        # Si no existe, crea uno nuevo
        with open(json_file_path, 'w') as file:
            json.dump([], file)

    # Lee los datos existentes
    with open(json_file_path, 'r') as file:
        datos_existentes = json.load(file)

    # Agrega los nuevos datos
    nuevos_datos = {
        "id": id,  # Agrega el ID aquí
        "sensor": sensor.getsensor(),
        "nombre": sensor.getnombre(),
        "descripcion": sensor.getdescripcion(),
        "fecha": sensor.getfecha().isoformat()  # Convierte a string
    }
    datos_existentes.append(nuevos_datos)

    # Guarda los datos de nuevo en el archivo
    with open(json_file_path, 'w') as file:
        json.dump(datos_existentes, file, indent=4)

# Función para manejar mensajes MQTT
def mensaje(cliente, informacion, msj):
    print(f"recibiendo el mensaje: {msj.payload.decode()}")
    # Aquí puedes ajustar el tipo de sensor según el tópico
    if informacion.topic == topico_humedad:
        sensor = Sensores(0, 1, "humedad", str(msj.payload.decode()))
    elif informacion.topic == topico_temperatura:
        sensor = Sensores(0, 1, "temperatura", str(msj.payload.decode()))
    # Agrega más condiciones para otros tópicos según sea necesario

    # Guarda los datos en la base de datos
    conexion.insertarDatos(sensor)  # Inserta en la base de datos
    guardar_datos(sensor)  # Guarda en el archivo JSON

# Asignar la función de callback
suscriptor.on_message = mensaje

# Conectar al broker y suscribirse a todos los tópicos
suscriptor.connect("test.mosquitto.org", 1883, 60)
suscriptor.subscribe([(topico_temperatura, 0),
                      (topico_humedad, 0),
                      (topico_led, 0),
                      (topico_luz, 0),
                      (topico_movimiento, 0),
                      (topico_potenciometro, 0),
                      (topico_ventilacion, 0),
                      (topico_pir, 0),
                      (topico_aviso_humedad, 0)])

# Escuchar siempre
suscriptor.loop_forever()
