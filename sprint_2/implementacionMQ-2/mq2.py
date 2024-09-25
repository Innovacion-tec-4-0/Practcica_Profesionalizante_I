import paho.mqtt.client as mqtt
import json
from conexion import Conexion
from tabla import Sensores

usuario = "sala/temperatura"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado correctamente al broker MQTT")
        client.subscribe(usuario)
        print(f"conctado al topico {usuario}")
    else:
        print(f"Error al conectar al broker MQTT. Código: {rc}")

conectar = Conexion()
def onmessage(client, userdata, msj):
    print(f"Mensaje recibido: {msj.payload.decode()} del topico {usuario}")
    sensor = Sensores(0, 1, "humedad", msj)  
    conectar.insertarDatos(sensor)       

cliente = mqtt.Client()

cliente.on_connect = on_connect
cliente.on_message = onmessage

cliente.connect("test.mosquitto.org", 1883, 60)
cliente.subscribe(usuario)
cliente.loop_forever()
