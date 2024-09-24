import paho.mqtt.client as mqtt
import json
import time
import os

# Configuraciones de MQTT
broker = "test.mosquitto.org"
port = 1883
client_id = "SiMonAmMu"  # Changed variable name to client_id for clarity

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

# Archivo JSON donde se guardarán los datos
ruta_json = os.path.join(os.getcwd(), "datos_sensores.json")

# Cargar datos previos si el archivo existe
if os.path.exists(ruta_json):
    with open(ruta_json, 'r') as f:
        datos = json.load(f)
else:
    datos = []  # Lista vacía si el archivo no existe

# Callback - Conexión establecida con el broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
        # Suscribirse a los tópicos
        client.subscribe(topico_temperatura)
        client.subscribe(topico_humedad)
        client.subscribe(topico_led)
        client.subscribe(topico_luz)
        client.subscribe(topico_movimiento)
        client.subscribe(topico_potenciometro)
        client.subscribe(topico_ventilacion)
        client.subscribe(topico_pir)
        client.subscribe(topico_aviso_humedad)
    else:
        print(f"Conexión fallida. Código de error: {rc}")

# Callback - Mensaje recibido
def on_message(client, userdata, msg):
    mensaje = msg.payload.decode()
    topico = msg.topic

    # Mostrar el mensaje recibido en consola
    print(f"Tópico: {topico} | Mensaje: {mensaje}")

    # Crear un diccionario con los datos
    dato = {
        "timestamp": time.ctime(),
        "topico": topico,
        "mensaje": mensaje
    }

    # Añadir el nuevo dato a la lista de datos
    datos.append(dato)

    # Guardar los datos en formato JSON
    with open(ruta_json, 'w') as f:
        json.dump(datos, f, indent=4)

# Crear cliente MQTT
client = mqtt.Client(client_id=client_id)  # Specify client_id here

# Asignar las funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
print(f"Conectando al broker {broker}...")
client.connect(broker, port)

# Mantener el cliente conectado
client.loop_start()

try:
    while True:
        time.sleep(1)  # Mantener el script corriendo
except KeyboardInterrupt:
    print("Desconectando...")
    client.loop_stop()
    client.disconnect()
