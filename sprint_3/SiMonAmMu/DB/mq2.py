import paho.mqtt.client as mqtt
import json
from DB.conexion_db import Conexion
from tabla import Sensores

usuario = "sala/temperatura"
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
    payload = msg.payload.decode()
    print(f"Mensaje recibido: {payload} del tópico {msg.topic}")

    # Verificar el tópico y procesar según su tipo
    if msg.topic == "sala/aviso_humedad":
        print("Acción a tomar para aviso de humedad:", payload)
    elif msg.topic == "sala/potenciometro":
        # Suponiendo que este es un valor numérico
        try:
            valor = float(payload)
            print(f"Valor recibido de potenciometro: {valor}")
            # Aquí puedes insertar el dato en la base de datos o procesarlo
        except ValueError:
            print("Error al convertir el valor de potenciometro a float.")
    elif msg.topic == "sala/luz":
        # Suponiendo que este es un valor numérico
        try:
            valor = float(payload)
            print(f"Valor recibido de luz: {valor}")
            # Aquí puedes insertar el dato en la base de datos o procesarlo
        except ValueError:
            print("Error al convertir el valor de luz a float.")
    elif msg.topic == "sala/humedad":
        try:
            valor = float(payload)
            print(f"Valor recibido de humedad: {valor}")
            # Aquí puedes insertar el dato en la base de datos o procesarlo
        except ValueError:
            print("Error al convertir el valor de humedad a float.")
    elif msg.topic == "sala/temperatura":
        try:
            valor = float(payload)
            print(f"Valor recibido de temperatura: {valor}")
            # Aquí puedes insertar el dato en la base de datos o procesarlo
        except ValueError:
            print("Error al convertir el valor de temperatura a float.")
    elif msg.topic == "sala/movimiento":
        print(f"Estado de movimiento: {payload}")
    else:
        print("Mensaje no procesado:", payload)

# Crear un cliente MQTT
cliente = mqtt.Client()

# Asignar las funciones de callback para conexión y mensajes
cliente.on_connect = on_connect
cliente.on_message = on_message

# Conectar al broker test.mosquitto.org en el puerto 1883
cliente.connect("test.mosquitto.org", 1883, 60)

# Mantener el cliente en ejecución para escuchar mensajes
cliente.loop_forever()