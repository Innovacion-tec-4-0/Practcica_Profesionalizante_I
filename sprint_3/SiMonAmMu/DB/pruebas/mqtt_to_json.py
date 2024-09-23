#mqtt_to_json.py: e encarga de recibir datos de varios tópicos MQTT y guardarlos en archivos JSON, tanto en la ubicación del script como en una ruta específica de respaldo
import time
import paho.mqtt.client as mqtt
import json
import os

# Ruta para que se guarde el archivo JSON en la misma carpeta que el script
json_file_path = os.path.join(os.path.dirname(__file__), "sensor_data.json")

# Ruta para guardar una copia en la carpeta específica
json_backup_path = r"D:\2024-segunda etapa\Practica_Profesionalizante_I\sprint_3\SiMonAmMu\DB\json\sensor_data.json"

# Verificar si la carpeta existe, si no, la crea
os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
os.makedirs(os.path.dirname(json_backup_path), exist_ok=True)

id = "SiMonAmMu"
humedad_topic = f"{id}/sala/humedad"
temperatura_topic = f"{id}/sala/temperatura"
luz_topic = f"{id}/sala/luz"
mov_topic = f"{id}/sala/movimiento"
led_topic = f"{id}/sala/led"
pir_topic = f"{id}/sala/pir"
pot_topic = f"{id}/sala/potenciometro"
ventilacion_topic = f"{id}/sala/ventilacion"
aviso_humedad_topic = f"{id}/sala/aviso_humedad"

# Callback when a message is received
def on_message(client, userdata, message):
    print(f"Mensaje recibido en el tópico: {message.topic}")
    payload = message.payload.decode()
    print(f"Contenido: {payload}")

    try:
        # Intentar decodificar el payload a JSON
        data = json.loads(payload)

        # Guardar los datos en un archivo JSON
        data_to_save = {
            "topic": message.topic,
            "value": data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Guardar en el archivo JSON principal
        with open(json_file_path, 'a') as json_file:
            json.dump(data_to_save, json_file)
            json_file.write('\n')

        # Guardar en el archivo JSON de copia
        with open(json_backup_path, 'a') as json_backup_file:
            json.dump(data_to_save, json_backup_file)
            json_backup_file.write('\n')

        print("Datos guardados exitosamente.")

    except json.JSONDecodeError:
        print(f"Error al decodificar el mensaje: {payload}")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

print(f"Datos se guardarán en: {json_file_path} y {json_backup_path}")

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    print("Conectado con resultado de código: " + str(rc))
    client.subscribe(humedad_topic)
    client.subscribe(temperatura_topic)
    client.subscribe(luz_topic)
    client.subscribe(mov_topic)
    client.subscribe(led_topic)
    client.subscribe(pir_topic)
    client.subscribe(pot_topic)
    client.subscribe(ventilacion_topic)
    client.subscribe(aviso_humedad_topic)

# Crear la conexión cliente
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Conectar al broker
mqtt_client.connect("test.mosquitto.org", 1883, 60)
mqtt_client.loop_start()

# Bucle principal
try:
    while True:
        time.sleep(1)  # Esperar para permitir la recepción de mensajes

except KeyboardInterrupt:
    print("Interrupción del programa")

finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
