import json
import os
import paho.mqtt.client as mqtt
from test.conexion_db import Conexion
from datetime import datetime

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

#  Crear el cliente MQTT
client = mqtt.Client()

# Obtener el directorio actual
directorio_actual = os.getcwd()

# Definir la ruta completa del archivo JSON
json_file_path = os.path.join(directorio_actual, "datos_SimMonAmMu.json")

print(f"Archivo JSON se guardará en: {json_file_path}")

def guardar_datos(temperatura, humedad, lux, led, movimiento, potenciometro=None, ventilacion=None, pir=None, aviso_humedad=None):
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
        "temperatura": temperatura,
        "humedad": humedad,
        "lux": lux,
        "led": led,
        "movimiento": movimiento,
        "potenciometro": potenciometro,
        "ventilacion": ventilacion,
        "pir": pir,
        "aviso_humedad": aviso_humedad,
        "fecha": datetime.now().isoformat()
    }
    datos_existentes.append(nuevos_datos)

    # Guarda los datos de nuevo en el archivo
    with open(json_file_path, 'w') as file:
        json.dump(datos_existentes, file, indent=4)

def insertar_datos(conn, temperatura, humedad, lux, led, movimiento, potenciometro=None, ventilacion=None, pir=None, aviso_humedad=None):
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

                # Guardar datos adicionales si están disponibles
                if potenciometro is not None:
                    cursor.execute("INSERT INTO potenciometro (valor) VALUES (%s)", (potenciometro,))
                if ventilacion is not None:
                    cursor.execute("INSERT INTO ventilacion (valor) VALUES (%s)", (ventilacion,))
                if pir is not None:
                    cursor.execute("INSERT INTO pir (estado) VALUES (%s)", (pir,))
                if aviso_humedad is not None:
                    cursor.execute("INSERT INTO aviso_humedad (estado) VALUES (%s)", (aviso_humedad,))

                cursor.execute("""INSERT INTO datos_ambientales 
                    (temperatura_id, humedad_id, lux_id, led_id, movimiento_id, fecha_hora) 
                    VALUES (%s, %s, %s, %s, %s, NOW())""",
                    (temperatura_id, humedad_id, lux_id, led_id, movimiento_id))

                conn.conectar.commit()
                print("Datos almacenados correctamente.")
        except Exception as e:
            print(f"Error al insertar datos: {e}")
            conn.conectar.rollback()

def on_message(client, userdata, message):
    payload = message.payload.decode()
    print("Payload recibido:", payload)
    datos = payload.split(",")
    
    # Inicializa las variables
    temperatura = humedad = lux = led = movimiento = None
    potenciometro = ventilacion = pir = aviso_humedad = None

    try:
        if message.topic == topico_temperatura:
            temperatura = float(datos[0])
        elif message.topic == topico_humedad:
            humedad = float(datos[0])
        elif message.topic == topico_luz:
            lux = int(datos[0])
        elif message.topic == topico_led:
            led = int(datos[0])
        elif message.topic == topico_movimiento:
            movimiento = int(datos[0])
        elif message.topic == topico_potenciometro:
            potenciometro = float(datos[0])
        elif message.topic == topico_ventilacion:
            ventilacion = float(datos[0])
        elif message.topic == topico_pir:
            pir = int(datos[0])
        elif message.topic == topico_aviso_humedad:
            aviso_humedad = int(datos[0])

        # Solo insertar datos si todas las variables están definidas
        if temperatura is not None and humedad is not None and lux is not None and led is not None and movimiento is not None:
            with Conexion() as conn:
                insertar_datos(conn, temperatura, humedad, lux, led, movimiento, potenciometro, ventilacion, pir, aviso_humedad)
                guardar_datos(temperatura, humedad, lux, led, movimiento, potenciometro, ventilacion, pir, aviso_humedad)
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
                      (topico_movimiento, 0),
                      (topico_potenciometro, 0),
                      (topico_ventilacion, 0),
                      (topico_pir, 0),
                      (topico_aviso_humedad, 0)])

    client.loop_start()

    # Obtener datos iniciales de las tablas
    with Conexion() as conn:
        print("Obteniendo datos iniciales...")
        obtener_temperaturas(conn)

    client.loop_forever()