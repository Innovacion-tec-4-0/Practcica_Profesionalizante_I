#data_recept.py
import paho.mqtt.client as mqttClient
import json
from test.conexion_db import Conexion


from datetime import datetime

client = mqttClient.Client()  # Última versión

def insertar_datos(conn, temperatura, humedad, lux, led, movimiento):
    if conn:
        try:
            with conn.conectar.cursor() as cursor:
                print("Insertando datos...")

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

def guardar_datos_json(temperatura, humedad, lux, led, movimiento):
    datos = {
        "temperatura": temperatura,
        "humedad": humedad,
        "lux": lux,
        "led": led,
        "movimiento": movimiento
    }

    with open("datosv.json", "a") as f:
        json.dump(datos, f)
        f.write("\n")  # Para separar cada entrada
    print("Datos almacenados en JSON.")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    print("Payload recibido:", payload)
    datos = payload.split(",")

    try:
        # Asumimos que el payload viene en este orden: temperatura, humedad, lux, led, movimiento
        temperatura = float(datos[0])
        humedad = float(datos[1])
        lux = int(datos[2])
        led = int(datos[3])
        movimiento = int(datos[4])

        with Conexion() as conn:
            insertar_datos(conn, temperatura, humedad, lux, led, movimiento)
            guardar_datos_json(temperatura, humedad, lux, led, movimiento)

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

# Función para obtener los datos ambientales
def obtener_datos_ambientales(conn):
    if conn:
        try:
            with conn.conectar.cursor() as cursor:
                cursor.execute("""
                    SELECT da.*, t.valor AS temp_valor, h.valor AS hum_valor, l.nivel AS lux_nivel, 
                           led.estado AS led_estado, m.estado AS mov_estado
                    FROM datos_ambientales da
                    JOIN temperatura t ON da.temperatura_id = t.id
                    JOIN humedad h ON da.humedad_id = h.id
                    JOIN lux l ON da.lux_id = l.id
                    JOIN led ON da.led_id = led.id
                    JOIN movimiento m ON da.movimiento_id = m.id
                """)
                resultados = cursor.fetchall()
                for fila in resultados:
                    print(f"ID: {fila[0]}, Temp: {fila['temp_valor']}, Humedad: {fila['hum_valor']}, Lux: {fila['lux_nivel']}, LED: {fila['led_estado']}, Movimiento: {fila['mov_estado']}")
        except Exception as e:
            print(f"Error al obtener los datos ambientales: {e}")

# Función para obtener el estado de los LEDs
def obtener_estado_led(conn):
    if conn:
        try:
            with conn.conectar.cursor() as cursor:
                cursor.execute("SELECT * FROM led")
                resultados = cursor.fetchall()
                for fila in resultados:
                    print(f"ID: {fila[0]}, Estado: {fila[1]}")
        except Exception as e:
            print(f"Error al obtener el estado de los LEDs: {e}")

if __name__ == "__main__":
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    # Suscripciones
    client.subscribe("sala/temperatura")
    client.subscribe("sala/humedad")
    client.subscribe("sala/luz")  
    client.subscribe("sala/movimiento")  
    client.subscribe("sala/led")  

    # Bucle para mantener la conexión
    client.loop_start()

    # Obtener datos iniciales de las tablas
    with Conexion() as conn:
        print("Obteniendo datos iniciales...")
        obtener_temperaturas(conn)
        obtener_datos_ambientales(conn)
        obtener_estado_led(conn)

    client.loop_forever()
