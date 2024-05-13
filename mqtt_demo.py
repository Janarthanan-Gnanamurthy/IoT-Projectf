import paho.mqtt.client as mqtt
import random 
import time

mqttBroker = "broker.mqtt-dashboard.com"
relay = ["r11","r10","r21","r20","r31","r30","r41","r40"]
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

while True:
    relay1 = random.choice(relay)            
    client.publish("TEMPERATURE", relay1)
    print("Just published " + str(relay1) + " to Topic TEMPERATURE")
    time.sleep(1)