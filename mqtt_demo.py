import paho.mqtt.client as mqtt
import random
import time
import cv2
from person_detection import detect_person

mqttBroker = "broker.mqtt-dashboard.com"
relay = ["r11", "r10", "r21", "r20", "r31", "r30", "r41", "r40"]
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

# 0 for default webcam, change accordingly if you have multiple cameras
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect persons in the frame and get the count
    person_count = detect_person(frame)
    print(person_count)
    # # Publish the person count to the MQTT broker
    # client.publish("PERSON_COUNT", str(person_count))
    # print(f"Just published {person_count} to Topic PERSON_COUNT")

    # # Publish a random relay value
    # relay1 = random.choice(relay)
    # client.publish("TEMPERATURE", relay1)
    # print(f"Just published {relay1} to Topic TEMPERATURE")

    time.sleep(1)

cap.release()
cv2.destroyAllWindows()
