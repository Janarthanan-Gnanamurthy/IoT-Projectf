import paho.mqtt.client as mqtt
import time
import cv2
import numpy as np
import requests
from person_detection import detect_person

mqttBroker = "test.mosquitto.org"
relay = ["r1", "r2", "r3", "r4"]

# Initialize MQTT client
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)

# URL for the image capture
image_url = "http://192.168.250.62/1280x720.jpg"

try:
    while True:
        # Fetch the image from the URL
        response = requests.get(image_url)
        image_data = np.frombuffer(response.content, np.uint8)
        frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        if frame is None:
            print("Failed to decode the image")
            continue

        # Detect persons in the frame and get the count and the frame with detections
        person_count, frame_with_detections = detect_person(frame)
        print("Person count:", person_count)

        # Display the frame with detections
        cv2.imshow('Person Detection', frame_with_detections)

        # Publish the person count to the MQTT topic
        client.publish("COUNT", str(person_count))
        print(f"Just published {person_count} to Topic PERSON_COUNT")

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Clean up
    client.disconnect()
    cv2.destroyAllWindows()
    print("Cleaned up resources")
