import json
import os
import paho.mqtt.client as mqtt
from conexion_db import Conexion
from datetime import datetime

# Tópicos
topico_temperatura = "sala/temperatura"
topico_humedad = "sala/humedad"
topico_led = "sala/led"
topico_luz = "sala/luz"
topico_movimiento = "sala/movimiento"

# ID del sistema
id = "SiMonAmMu"

# Crear el cliente MQTT
client = mqtt.Client()
conexion = Conexion()

# Definir el archivo JSON
json_file_path = "datos_sensores.json"

def guardar_datos(sensor):
    # Verifica si el archivo existe
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as file:
            json.dump([], file)

    # Lee los datos existentes
    with open(json_file_path, 'r') as file:
        datos_existentes = json.load(file)

    # Agrega los nuevos datos
    nuevos_datos = {
        "id": id,
        "sensor": sensor.getsensor(),
        "nombre": sensor.getnombre(),
        "descripcion": sensor.getdescripcion(),
        "fecha": sensor.getfecha().isoformat()
    }
    datos_existentes.append(nuevos_datos)

    # Guarda los datos de nuevo en el archivo
    with open(json_file_path, 'w') as file:
        json.dump(datos_existentes, file, indent=4)

def insertar_datos(conn, temperatura, humedad, lux, led, movimiento):
    if conn:
        try:
            with conn.conectar.cursor() as cursor:
                print("Insertando datos...")
                # Inserciones en las tablas
                cursor.execute("INSERT INTO lux (nivel) VALUES (%s)", (lux,))
                lux_id = cursor.lastrowid

                cursor.execute("INSERT INTO led (estado) VALUES (%s)", (led,))
                led_id = cursor.lastrowid

                cursor.execute("INSERT INTO temperatura (valor) VALUES (%s)", (temperatura,))
                temperatura_id = cursor.lastrowid

                cursor.execute("INSERT INTO humedad (valor) VALUES (%s)", (humedad,))
                humedad_id = cursor.lastrowid

                cursor.execute("INSERT INTO movimiento (estado) VALUES (%s)", (movimiento,))
                movimiento_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO datos_ambientales 
                    (temperatura_id, humedad_id, lux_id, led_id, movimiento_id, fecha_hora) 
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """, (temperatura_id, humedad_id, lux_id, led_id, movimiento_id))

                conn.conectar.commit()
                print("Datos almacenados correctamente.")
        except Exception as e:
            print(f"Error al insertar datos: {e}")
            conn.conectar.rollback()

def on_message(client, userdata, message):
    payload = message.payload.decode()
    print("Payload recibido:", payload)
    datos = payload.split(",")

    try:
        temperatura = float(datos[0])
        humedad = float(datos[1])
        lux = int(datos[2])
        led = int(datos[3])
        movimiento = int(datos[4])

        with Conexion() as conn:
            insertar_datos(conn, temperatura, humedad, lux, led, movimiento)
            guardar_datos(sensor)  # Aquí deberías definir cómo crear el objeto 'sensor'
            
    except ValueError as e:
        print(f"Error al procesar los datos: {e}")

# Función para obtener temperaturas desde la base de datos
def obtener_temperaturas(conn):
    if conn:
        try:
            with conn.conectar.cursor() as cursor:
                cursor.execute("SELECT * FROM temperatura")
                resultados = cursor.fetchall()
                for fila in resultados:
                    print(f"ID: {fila[0]}, Valor: {fila[1]}, Timestamp: {fila[2]}")
        except Exception as e:
            print(f"Error al obtener las temperaturas: {e}")

if __name__ == "__main__":
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    # Suscripciones
    client.subscribe([(topico_temperatura, 0),
                      (topico_humedad, 0),
                      (topico_led, 0),
                      (topico_luz, 0),
                      (topico_movimiento, 0)])

    client.loop_start()

    # Obtener datos iniciales de las tablas
    with Conexion() as conn:
        print("Obteniendo datos iniciales...")
        obtener_temperaturas(conn)

    client.loop_forever()
