#include "WifiCam.hpp"
#include <WiFi.h>
#include <PubSubClient.h>

static const char* WIFI_SSID = "Redmi";
static const char* WIFI_PASS = "star1234";
const char* mqtt_server = "broker.hivemq.com";

const int relay_1 = 13;
const int relay_2 = 2;
const int relay_3 = 14;
const int relay_4 = 15;

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

esp32cam::Resolution initialResolution;
WebServer server(80);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  String message = "";
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    message += (char)payload[i];
  }
  Serial.println();

  // Turn on relays based on the received message
  if (message == "1") {
    digitalWrite(relay_1, LOW);  // Active low
    digitalWrite(relay_2, HIGH);
    digitalWrite(relay_3, HIGH);
    digitalWrite(relay_4, HIGH);
    Serial.println("Relay 1 ON");
  } else if (message == "2") {
    digitalWrite(relay_1, LOW);  // Active low
    digitalWrite(relay_2, LOW);  // Active low
    digitalWrite(relay_3, HIGH);
    digitalWrite(relay_4, HIGH);
    Serial.println("Relay 1, 2 ON");
  } else if (message == "3") {
    digitalWrite(relay_1, LOW);  // Active low
    digitalWrite(relay_2, LOW);  // Active low
    digitalWrite(relay_3, LOW);  // Active low
    digitalWrite(relay_4, HIGH);
    Serial.println("Relay 1, 2, 3 ON");
  } else if (message == "4") {
    digitalWrite(relay_1, LOW);  // Active low
    digitalWrite(relay_2, LOW);  // Active low
    digitalWrite(relay_3, LOW);  // Active low
    digitalWrite(relay_4, LOW);  // Active low
    Serial.println("Relay 1, 2, 3, 4 ON");
  } else {
    digitalWrite(relay_1, HIGH);  // Active low
    digitalWrite(relay_2, HIGH);  // Active low
    digitalWrite(relay_3, HIGH);  // Active low
    digitalWrite(relay_4, HIGH);  // Active low
    Serial.println("All Relays OFF");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.subscribe("COUNT");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(relay_1, OUTPUT);
  pinMode(relay_2, OUTPUT);
  pinMode(relay_3, OUTPUT);
  pinMode(relay_4, OUTPUT);
  
  // Set initial state to HIGH (off for active low relays)
  digitalWrite(relay_1, HIGH);  // Active low
  digitalWrite(relay_2, HIGH);  // Active low
  digitalWrite(relay_3, HIGH);  // Active low
  digitalWrite(relay_4, HIGH);  // Active low

  Serial.begin(115200);
  Serial.println();
  delay(2000);

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.printf("WiFi failure %d\n", WiFi.status());
    delay(5000);
    ESP.restart();
  }
  Serial.println("WiFi connected");

  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("camera initialize failure");
      delay(5000);
      ESP.restart();
    }
    Serial.println("camera initialize success");
  }

  Serial.println("camera starting");
  Serial.print("http://");
  Serial.println(WiFi.localIP());

  addRequestHandlers();
  server.begin();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  server.handleClient();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    ++value;
  }
}
