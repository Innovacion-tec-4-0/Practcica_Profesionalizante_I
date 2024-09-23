#jsondata.py se encarga de recibir datos de un broker MQTT y guardarlos en un archivo de texto.
import paho.mqtt.client as mqtt
import os

# Configuraciones de MQTT
broker = "test.mosquitto.org"
port = 1883
id= "SiMonAmMu"
topic = "sala/temperatura" 
topic2 = "sala/humedad"
topic3 = "sala/luz"
topic4 = "sala/movimiento"
topic5 = "sala/led"

# Ruta en tu computadora donde quieres guardar los datos (en el mismo directorio que el script)
ruta_guardado = os.path.join(os.getcwd(), "sensor_data.txt")

# Función que se llama cuando se recibe un mensaje
def on_message(client, userdata, message):
    data = message.payload.decode("utf-8")
    print(f"Datos recibidos: {data}")

    # Guardar los datos en un archivo en la ruta especificada
    with open(ruta_guardado, "a") as file:
        file.write(data + "\n")

# Crear cliente MQTT
client = mqtt.Client()

# Asignar la función de callback para cuando llegue un mensaje
client.on_message = on_message

# Conectar al broker
client.connect(broker, port)

# Suscribirse al tópico donde el ESP32 está publicando
client.subscribe(topic)

# Comenzar la escucha (bucle) de mensajes
client.loop_forever()
