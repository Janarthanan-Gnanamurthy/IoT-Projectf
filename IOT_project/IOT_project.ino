#include "WifiCam.hpp"
#include <WiFi.h>
#include <PubSubClient.h>

static const char* WIFI_SSID = "Redmi";
static const char* WIFI_PASS = "star1234";
const char* mqtt_server = "broker.mqtt-dashboard.com";
int relay_1 = 12;
int relay_2 = 13;
int relay_3 = 14;
int relay_4 = 15;



WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;



esp32cam::Resolution initialResolution;

WebServer server(80);
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == 'r11') {
    digitalWrite(relay_1, HIGH);
        Serial.print("relay1 on");
   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else if((char)payload[0] == 'r10'){
    digitalWrite(relay_1, LOW);
        Serial.print("relay1 off");
  // Turn the LED off by making the voltage HIGH
  }
  else if((char)payload[0] == 'r21'){
    digitalWrite(relay_2, HIGH);  // Turn the LED off by making the voltage HIGH
    Serial.print("relay2 on");
  }
  else if((char)payload[0] == 'r20'){
    digitalWrite(relay_2, LOW);  // Turn the LED off by making the voltage HIGH
    Serial.print("relay2 off");

  }
  else if((char)payload[0] == 'r31'){
    digitalWrite(relay_3, HIGH);  // Turn the LED off by making the voltage HIGH
    Serial.print("relay3 on");

  }
  else if((char)payload[0] == 'r30'){
    digitalWrite(relay_3, LOW);  // Turn the LED off by making the voltage HIGH
    Serial.print("relay3 off");

  }
  else if((char)payload[0] == 'r41'){
    digitalWrite(relay_4, HIGH);  // Turn the LED off by making the voltage HIGH
    Serial.print("relay4 on");

  }
  else if((char)payload[0] == 'r40'){
    digitalWrite(relay_4, LOW);  // Turn the LED off by making the voltage HIGH
    Serial.print("relay4 off");

  }
  

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      // client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("TEMPERATURE");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}




void setup() {
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

pinMode(33, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}
void
loop() {
  
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