 //main.cpp Local

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h> // Librería para manejar el sensor DHT22



#define pinDHT 15
#define tipDHT DHT22 // Define el tipo de sensor como DHT22
DHT sensordht22(pinDHT, DHT22); // Crea un objeto sensordht22 para interactuar con el sensor DHT22 conectado al pin 15.

// Configuración de la red WiFi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Configuración del servidor MQTT
const char* mqtt_server = "test.mosquitto.org"; // broker público
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_password = "";

// ID único del cliente MQTT
const char* client_id = "SiMonAmMu";

// Tópicos MQTT
const char* temperatura_topic = "sala/temperatura";
const char* humedad_topic = "sala/humedad";
const char* led_topic = "sala/led";
const char* luz_topic = "sala/luz";
const char* mov_topic = "sala/movimiento";
const char* pot_topic = "sala/potenciometro";
const char* ventilacion_topic = "sala/ventilacion";
const char* pir_topic = "sala/pir";
const char* aviso_humedad_topic = "sala/aviso_humedad";

// Pines
const int pirPin = 13; // Pin para el sensor PIR
const int ledPin = 23; // Pin para el LED
const int potPin = 34; // Pin para el potenciómetro
const int ventilacionPin = 26; // Pin para la ventilación
const int controlHumedadPin = 27; // Pin para el control de humedad
const int luzPin = 32; // Pin para el sensor de luz


// Variables Globales
float temperatura; // Almacena la lectura de la temperatura del sensor DHT22
float humedadambiente; // Almacena la lectura de la humedad ambiente del sensor DHT22
const float GAMMA = 0.7; // Valor constante usado en el cálculo de la luminosidad (lux)
const float RL10 = 50; // Constante usada en el cálculo de la luminosidad
float lux; //

/// Inicialización de cliente MQTT
WiFiClient espClient;
PubSubClient client(espClient);

// Declaración de la función callback
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Mensaje recibido en el tópico: ");
    Serial.println(topic);

    String msg = "";
    for (int i = 0; i < length; i++) {
        msg += (char)payload[i];
    }


    // Control de LED
    if (msg.substring(0, 3) == "on1") {
        Serial.print("LAMPARA1 ON  ");
        digitalWrite(ledPin, HIGH);
    }
    if (msg.substring(0, 3) == "of1") {
        Serial.print("LAMPARA1 Off  ");
        digitalWrite(ledPin, LOW);
    }
    Serial.print(msg.substring(0, 3));
    Serial.print("-----------------------");
    Serial.print(msg.length());
}

void testDHT() {
    float temp = sensordht22.readTemperature();
    float hum = sensordht22.readHumidity();
    Serial.print("Temperatura: ");
    Serial.println(temp);
    Serial.print("Humedad: ");
    Serial.println(hum);
}

void setup_wifi() {
    delay(10);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Conectado a WiFi");
}
// Conexión MQTT
void reconnect() {
    while (!client.connected()) {
        Serial.println("Intentando conexión MQTT...");
        if (client.connect(client_id, mqtt_user, mqtt_password)) {
            Serial.println("Conectado al servidor MQTT");
            client.subscribe(led_topic);
            client.subscribe(mov_topic);
        } else {
            Serial.print("Error de conexión, rc=");
            Serial.print(client.state());
            Serial.println(" Intentando de nuevo en 5 segundos");
            delay(5000);
        }
    }
}
void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);

// Configuración de pines
 
  
  pinMode(26, OUTPUT); // Pin 26 como salida (ventilación)
  pinMode(27, OUTPUT); // Pin 27 como salida (control de humedad)
  pinMode(luzPin, INPUT); // Configura el pin del sensor de luz como entrada
  pinMode(ventilacionPin, OUTPUT); // Pin para ventilación
  pinMode(controlHumedadPin, OUTPUT); // Pin para control de humedad
  pinMode(pirPin, INPUT); // Configura el pin PIR como entrada
  pinMode(ledPin, OUTPUT); // Configura el pin LED como salida
  pinMode(potPin, INPUT); // Configura el pin del potenciómetro como entrada
  pinMode(14, OUTPUT); // 
    
  sensordht22.begin(); // Inicia la comunicación con el sensor DHT22
}


void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    // Leer el sensor de luz
    int analogValue = analogRead(luzPin); // Lee un valor analógico del pin del sensor de luz
    float voltage = analogValue * (5.0 / 4095.0); // Convierte el valor a voltaje
    float resistance = (RL10 * (5.0 - voltage)) / voltage; // Cálculo de resistencia
    lux = pow(RL10 * 1000 * pow(10, GAMMA) / resistance, (1 / GAMMA)); // Cálculo de lux
    lux = constrain(lux, 0, 100000); // Ensure lux is within valid range

    if (lux < 0) lux = 0; // Asegura que no sea negativo
    if (lux > 100000) lux = 100000; // Limita el valor máximo si es necesario


    // Leer el estado del sensor PIR
    int movimientoDetectado = digitalRead(pirPin);
    Serial.print("Estado del PIR: ");
    Serial.println(movimientoDetectado);
    
    
    //Leer el DHT22
    temperatura = sensordht22.readTemperature();
    humedadambiente = sensordht22.readHumidity();
    if (isnan(temperatura) || isnan(humedadambiente)) {
        Serial.println("Error leyendo del DHT!");
        return; // Salir si hay un error
    } else {
        Serial.print("Temperatura: ");
        Serial.println(temperatura);
        Serial.print("Humedad: ");
        Serial.println(humedadambiente);
}

  // Enviar datos del sensor cada 10 segundos
    static unsigned long lastSendTime = 0;
    if (millis() - lastSendTime > 10000) {
    
        // Publicar datos de temperatura y humedad
        char humStr[8];
        dtostrf(humedadambiente, 1, 2, humStr);
        client.publish(humedad_topic, humStr);

        char tempStr[8];
        dtostrf(temperatura, 1, 2, tempStr);
        client.publish(temperatura_topic, tempStr);

        client.publish(mov_topic, movimientoDetectado ? "1" : "0");  

        Serial.print("Temperatura: ");
        Serial.println(temperatura);
        
        Serial.print("Luminosidad: ");
        Serial.println(lux);
        
        Serial.print("Movimiento: ");
        Serial.println(movimientoDetectado);


        // Leer el valor del potenciómetro
        int potenciometro = analogRead(potPin);
        Serial.print("Potenciometro: ");
        Serial.println(potenciometro);

              
        Serial.print("Ventilacion: ");
        Serial.println(digitalRead(ventilacionPin));
        
        Serial.print("Humedad Ambiente: ");
        Serial.println(humedadambiente);

        
        Serial.print("Led: ");
        Serial.println(digitalRead(ledPin));
        
        Serial.print("Pir: ");
        Serial.println(movimientoDetectado);    


       // Control de LED según movimiento
        digitalWrite(ledPin, movimientoDetectado == HIGH ? HIGH : LOW);

        // Control de ventilación y aviso de humedad
        if (humedadambiente >= 40 || temperatura >= 28) {
            digitalWrite(ventilacionPin, HIGH); // Encender ventilación
            if (humedadambiente >= 40) {
                client.publish(aviso_humedad_topic, "Humedad alta detectada");
            }
        } else {
            digitalWrite(ventilacionPin, LOW); // Apagar ventilación
        }


       // Control de persianas basado en luminosidad
        digitalWrite(14, lux >= 50000 ? HIGH : LOW); // Activa o desactiva persianas
 
      
      
        // Control de ventilación basado en temperatura
        if (temperatura >= 28) {
            digitalWrite(ventilacionPin, HIGH); // Activa la salida para la ventilación
        } else if (temperatura <= 24) {
            digitalWrite(ventilacionPin, LOW); // Desactiva la salida de ventilación
        }

       lastSendTime = millis();

    
// Detección de movimiento y control de luz
    int movimientoDetectado = digitalRead(pirPin);
    Serial.print("Estado del PIR: ");
    Serial.println(movimientoDetectado);

if (movimientoDetectado == HIGH) {
    Serial.println("Movimiento detectado.");
    int lightValue = analogRead(potPin); // Leer el valor del potenciómetro
    float lightLevel = map(lightValue, 0, 4095, 0, 100); // Convertir a un rango de 0 a 100

    if (lightLevel < 50) { // Ajusta este valor según tus necesidades
        digitalWrite(ledPin, HIGH); // Encender la luz
        Serial.println("Luces encendidas.");
    } else {
        digitalWrite(ledPin, LOW); // Mantener apagada la luz
        Serial.println("Suficiente luz, luces apagadas.");
    }
} else {
    digitalWrite(ledPin, LOW); // Apagar la luz si no hay movimiento
}

delay(100); // Esperar  antes de volver a comprobar
    }
}
    
