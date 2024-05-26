import paho.mqtt.client as mqtt
import time
import cv2
import numpy as np
import requests
from person_detection import detect_person

mqttBroker = "broker.mqtt-dashboard.com"
relay = ["r1", "r2", "r3", "r4"]

# Initialize MQTT client
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

# URL for the image capture
image_url = "http://192.168.128.62/1280x720.jpg"

try:
    while True:
        # Fetch the image from the URL
        response = requests.get(image_url)
        image_data = np.frombuffer(response.content, np.uint8)
        frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        if frame is None:
            print("Failed to decode the image")
            continue

        # Detect persons in the frame and get the count
        person_count = detect_person(frame)
        print("Person count:", person_count)

        # Keep track of relays that should be on
        relay_on = set()
        
        # Turn on relays for detected persons
        for i in range(person_count):
            if i < len(relay):
                msg = relay[i] + '1'
                relay_on.add(relay[i])
                client.publish("PERSON_COUNT", str(msg))
                print(f"Just published {msg} to Topic PERSON_COUNT")

        # Turn off the remaining relays
        for r in relay:
            if r not in relay_on:
                msg = r + '0'
                client.publish("PERSON_COUNT", str(msg))
                print(f"Just published {msg} to Topic PERSON_COUNT")

        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Clean up
    client.disconnect()
    print("Cleaned up resources")
