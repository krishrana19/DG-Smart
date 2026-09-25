#include <WiFi.h>
#include <PubSubClient.h>

#define ONBOARD_LED 2 

// --- Permanent Network & MQTT Configuration ---
const char* ssid = "LAPTOP-NU5176TH 1361";
const char* password = "707i97L]";
const char* mqtt_server = "192.168.137.1"; 

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;

void setup_wifi() {
  delay(10);
  Serial.print("Connecting to WiFi network: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected successfully.");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("Command received on [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(message);
  
  if (String(topic) == "smartdg/relay/command") {
    if (message == "DISCONNECT") {
      digitalWrite(ONBOARD_LED, LOW); 
      Serial.println("Action: Relay OFF");
    } else if (message == "RESTORE") {
      digitalWrite(ONBOARD_LED, HIGH); 
      Serial.println("Action: Relay ON");
    }
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection to ");
    Serial.print(mqtt_server);
    Serial.print("...");
    
    String clientId = "ESP32Client-";
    clientId += String(random(0, 0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.subscribe("smartdg/relay/command"); 
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(ONBOARD_LED, OUTPUT);
  digitalWrite(ONBOARD_LED, HIGH); 
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop(); 

  unsigned long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
    
    float dummyVoltage = random(2200, 2400) / 10.0; 
    float dummyPower = random(900, 1100) / 10.0;    
    bool dummyGridStatus = random(0, 2);            
    
    String payload = "{";
    payload += "\"voltage\":" + String(dummyVoltage) + ",";
    payload += "\"power\":" + String(dummyPower) + ",";
    payload += "\"grid_present\":" + String(dummyGridStatus ? "true" : "false"); 
    payload += "}";

    Serial.print("Publishing telemetry: ");
    Serial.println(payload);
    client.publish("smartdg/telemetry", payload.c_str());
  }
}