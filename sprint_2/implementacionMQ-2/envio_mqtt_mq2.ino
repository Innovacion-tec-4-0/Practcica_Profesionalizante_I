#include <WiFi.h>
#include <PubSubClient.h>


const char* ssid = "***";
const char* password = "***";
const char* mqtt_server = "test.mosquitto.org";  // Broker MQTT

const char* topico = "pentadevs/mq2";

WiFiClient espClient;
PubSubClient client(espClient); //declaramos la variable client

#define MQ2PIN 34 
  

void setup() {
  Serial.begin(115200);
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void setup_wifi() {
  delay(10);
  Serial.print("Conectando a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi conectado");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conectar a MQTT...");
    if (client.connect("ESP32Client_001")) {
      Serial.println("Conectado");
    } else {
      Serial.print("Fallado, rc=");
      Serial.print(client.state());
      Serial.println(" intentando de nuevo en 5 segundos");
      delay(5000);
    }
  }
}

void loop() {
  delay(2000);
  
  int mq = analogRead(MQ2PIN);

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  String mensaje = "valor: " + String(mq);
  client.publish(topico, mensaje.c_str());
  Serial.println("Se enviaron los datos: " + String(mensaje));

  delay(3000);
}
