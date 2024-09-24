#jsondata.py se encarga de recibir datos de un broker MQTT y guardarlos en un archivo de texto.
from datetime import datetime
import json
import paho.mqtt.client as mqtt
import os

# Configuraciones de MQTT
broker = "test.mosquitto.org"
port = 1883
id= "SiMonAmMu"
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

# Ruta en tu computadora donde quieres guardar los datos (en el mismo directorio que el script)
ruta_guardado = os.path.join(os.getcwd(), "sensor_datav2.json")

# Inicializar el diccionario para almacenar datos
data_dict = {}

# Función que se llama cuando se recibe un mensaje
def on_message(client, userdata, message):
    # Obtener el tópico y el dato recibido
    topic = message.topic
    data = message.payload.decode("utf-8")
    
    # Agregar la información al diccionario
    if topic not in data_dict:
        data_dict[topic] = []
    
    # Guardar la información con un timestamp
    timestamp = datetime.now().isoformat()
    data_dict[topic].append({"timestamp": timestamp, "value": data})
    
    # Imprimir datos recibidos
    print(f"Datos recibidos de {topic}: {data}")

    # Guardar los datos en un archivo JSON
    with open(ruta_guardado, "w") as json_file:
        json.dump(data_dict, json_file, indent=4)


# Crear cliente MQTT
client = mqtt.Client()


# Asignar la función de callback para cuando llegue un mensaje
client.on_message = on_message

# Conectar al broker
client.connect(broker, port)

# Suscribirse a todos los tópicos
client.subscribe([(topico_aviso_humedad, 0), (topico_led, 0), (topico_luz, 0), 
                  (topico_movimiento, 0), (topico_pir, 0), (topico_potenciometro, 0), 
                  (topico_ventilacion, 0), (topico_temperatura, 0), (topico_humedad, 0)])


# Comenzar la escucha (bucle) de mensajes
client.loop_forever()
