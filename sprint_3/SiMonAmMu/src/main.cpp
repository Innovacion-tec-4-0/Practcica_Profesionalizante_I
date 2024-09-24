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
float lux; // Variable para luminosidad

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
    pinMode(ventilacionPin, OUTPUT); // Pin 26 como salida (ventilación)
    pinMode(controlHumedadPin, OUTPUT); // Pin 27 como salida (control de humedad)
    pinMode(luzPin, INPUT); // Configura el pin del sensor de luz como entrada
    pinMode(pirPin, INPUT); // Configura el pin PIR como entrada
    pinMode(ledPin, OUTPUT); // Configura el pin LED como salida
    pinMode(potPin, INPUT); // Configura el pin del potenciómetro como entrada
    pinMode(14, OUTPUT); // Pin para persianas

    sensordht22.begin(); // Inicia la comunicación con el sensor DHT22
}

// Función para leer los sensores y publicar los datos
void leerSensoresYPublicar() {
    
    // Leer el sensor de luz
    int analogValue = analogRead(luzPin);
    float voltage = analogValue * (5.0 / 4095.0);
    float resistance = (RL10 * (5.0 - voltage)) / voltage;
    lux = pow(RL10 * 1000 * pow(10, GAMMA) / resistance, (1 / GAMMA));
    lux = constrain(lux, 0, 100000);

    // Leer el estado del sensor PIR
    int movimientoDetectado = digitalRead(pirPin);

    // Leer el DHT22
    temperatura = sensordht22.readTemperature();
    humedadambiente = sensordht22.readHumidity();
    if (isnan(temperatura) || isnan(humedadambiente)) {
        Serial.println("Error leyendo del DHT!");
        return;
    }

    // Publicar potenciómetro
    int potValue = analogRead(potPin);
    char potStr[8];
    dtostrf(potValue, 1, 0, potStr);
    client.publish(pot_topic, potStr);

    // Publicar luminosidad
    char luxStr[8];
    dtostrf(lux, 1, 2, luxStr);
    client.publish(luz_topic, luxStr);

    // Publicar datos de temperatura y humedad
    char humStr[8], tempStr[8];
    dtostrf(humedadambiente, 1, 2, humStr);
    dtostrf(temperatura, 1, 2, tempStr);
    client.publish(humedad_topic, humStr);
    client.publish(temperatura_topic, tempStr);

    // Publicar movimiento
    client.publish(mov_topic, movimientoDetectado ? "1" : "0");

    // Publicar el estado de la ventilación y control de humedad
    if (humedadambiente >= 40 || temperatura >= 28) {
        digitalWrite(ventilacionPin, HIGH);
        client.publish(aviso_humedad_topic, "Humedad alta detectada");
    } else {
        digitalWrite(ventilacionPin, LOW);
    }

    // Control de persianas basado en luminosidad
    digitalWrite(14, lux >= 50000 ? HIGH : LOW);

    // Control de ventilación basado en temperatura
    digitalWrite(ventilacionPin, (temperatura >= 28) ? HIGH : LOW);

    // Imprimir datos en el monitor serie
    Serial.print("Temperatura: ");
    Serial.println(temperatura);
    Serial.print("Humedad: ");
    Serial.println(humedadambiente);
    Serial.print("Luminosidad: ");
    Serial.println(lux);
    Serial.print("Movimiento detectado: ");
    Serial.println(movimientoDetectado ? "Sí" : "No");
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    leerSensoresYPublicar();
    delay(2000); // Espera 2 segundos entre lecturas
}
