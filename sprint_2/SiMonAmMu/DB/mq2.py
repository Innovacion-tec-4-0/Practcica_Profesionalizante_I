import paho.mqtt.client as mqtt
import json
from conexion_db import Conexion
from tabla import Sensores

# Tópicos MQTT
temperatura_topic = "sala/temperatura"
humedad_topic = "sala/humedad"
led_topic = "sala/led"
luz_topic = "sala/luz"
mov_topic = "sala/movimiento"
pot_topic = "sala/potenciometro"
ventilacion_topic = "sala/ventilacion"
pir_topic = "sala/pir"
aviso_humedad_topic = "sala/aviso_humedad"

# Función que se ejecuta cuando te conectas al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado correctamente al broker MQTT")
        # Suscribirse a los tópicos después de conectarse
        client.subscribe([
            (temperatura_topic, 0),
            (humedad_topic, 0),
            (led_topic, 0),
            (luz_topic, 0),
            (mov_topic, 0),
            (pot_topic, 0),
            (ventilacion_topic, 0),
            (pir_topic, 0),
            (aviso_humedad_topic, 0),
        ])
        print(f"Conectado a los tópicos MQTT")
    else:
        print(f"Error al conectar al broker MQTT. Código: {rc}")

# Función que se ejecuta cuando se recibe un mensaje del broker
def on_message(client, userdata, msg):
    print(f"Mensaje recibido: {msg.payload.decode()} del tópico {msg.topic}")
    
    try:
        # Suponiendo que el mensaje es un JSON
        mensaje = json.loads(msg.payload.decode())
        # Procesa el mensaje aquí, por ejemplo, inserta en la base de datos
        # sensor = Sensores(0, 1, "humedad", mensaje)  # Ejemplo
        # conectar.insertarDatos(sensor)               # Inserta el dato en la base
    except json.JSONDecodeError:
        print("Error al decodificar el mensaje JSON")

# Crear un cliente MQTT
cliente = mqtt.Client()

# Asignar las funciones de callback para conexión y mensajes
cliente.on_connect = on_connect
cliente.on_message = on_message

# Conectar al broker test.mosquitto.org en el puerto 1883
cliente.connect("test.mosquitto.org", 1883, 60)

# Mantener el cliente en ejecución para escuchar mensajes
cliente.loop_forever()
