import random
import json
from datetime import datetime, timedelta

# Función para generar los datos de los sensores
def generar_datos_sensores(num_datos):
    sensor_data = []  # Lista para almacenar los datos generados
    base_time = datetime.now()  # Obtener el tiempo actual como referencia

    # Generar una cantidad de datos basada en el número especificado
    for i in range(num_datos):
        id_sensor = f"sensor_{i}"  # Asignar un ID único a cada sensor
        humedadambiente = random.uniform(30.0, 60.0)  # Generar un valor aleatorio de humedad entre 30 y 60
        temperatura = random.uniform(20.0, 35.0)  # Generar un valor aleatorio de temperatura entre 20 y 35
        lightLevel = random.uniform(10, 100)  # Generar un nivel de luz entre 10 y 100
        movimiento = random.choice([0, 1])  # Generar un valor aleatorio para el sensor PIR (0: no hay movimiento, 1: hay movimiento)
        potenciometro = random.uniform(0, 1023)  # Generar un valor aleatorio para el potenciómetro (0 a 1023)
        
        # Controlar la ventilación basado en la humedad o temperatura
        ventilacion = 1 if (humedadambiente >= 40 or temperatura >= 28) else 0  
        
        # Controlar las luces basándose en el nivel de luz
        led = 1 if lightLevel < 50 else 0  
        
        # Generar un mensaje de aviso si la humedad es alta
 # Generar un mensaje de aviso si la humedad es alta
        aviso_humedad = "Humedad alta detectada" if humedadambiente >= 40 else ""  # Si la humedad es >= 40, si no, dejar vacío
        aviso_humedad = "Humedad alta detectada" if humedadambiente >= 40 else ""

        # Generar una marca de tiempo para cada dato
        timestamp = (base_time - timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')

        # Agregar los datos generados a la lista de sensor_data
        sensor_data.append({
            "id": id_sensor,
            "timestamp": timestamp,
            "humedad": round(humedadambiente, 2),
            "temperatura": round(temperatura, 2),
            "luz": round(lightLevel, 2),
            "movimiento": movimiento,
            "potenciometro": round(potenciometro, 2),
            "ventilacion": ventilacion,
            "led": led,
            "aviso_humedad": aviso_humedad,
            "topics": {
                "humedad_topic": f"{id_sensor}/sala/humedad",
                "temperatura_topic": f"{id_sensor}/sala/temperatura",
                "luz_topic": f"{id_sensor}/sala/luz",
                "mov_topic": f"{id_sensor}/sala/movimiento",
                "led_topic": f"{id_sensor}/sala/led",
                "pir_topic": f"{id_sensor}/sala/pir",
                "pot_topic": f"{id_sensor}/sala/potenciometro",
                "ventilacion_topic": f"{id_sensor}/sala/ventilacion",
                "aviso_humedad_topic": f"{id_sensor}/sala/aviso_humedad"
            }
        })

    return sensor_data

# Función para guardar los datos generados en un archivo JSON
def guardar_datos_json(sensor_data, file_name="sensor_data.json"):
    with open(file_name, "w") as f:
        json.dump(sensor_data, f, indent=4)  # Guardar los datos en formato JSON con indentación
    print(f"Datos guardados en {file_name}")  # Confirmar que los datos se guardaron correctamente

# Punto de entrada principal del script
if __name__ == "__main__":
    num_datos = 100  # Definir el número de datos a generar
    datos_sensores = generar_datos_sensores(num_datos)  # Llamar a la función para generar los datos
    guardar_datos_json(datos_sensores)  # Guardar los datos en un archivo JSON
