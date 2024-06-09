from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import tensorflow as tf
import requests
import time
from person_detection import detect_person
import paho.mqtt.client as mqtt

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load the model
model = tf.saved_model.load('./efficientdet_d0_coco17_tpu-32/saved_model')

# Initialize MQTT client
mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Temperature_Inside")
client.connect(mqttBroker)
# State
auto_mode = False
relay_status = {"r1": False, "r2": False, "r3": False, "r4": False}

# Detect persons in the image


@app.route('/detect', methods=['GET'])
def detect():
    global auto_mode, relay_status

    image_url = "http://192.168.200.62/1280x720.jpg"
    response = requests.get(image_url)
    image_data = np.frombuffer(response.content, np.uint8)
    frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Failed to decode the image"}), 500

    person_count = detect_person(frame)
    socketio.emit('person_count', {'count': person_count})

    if auto_mode:
        # Logic to control relays based on person count
        if person_count > 0:
            for relay in relay_status:
                relay_status[relay] = True
        else:
            for relay in relay_status:
                relay_status[relay] = False

    return jsonify({"person_count": person_count, "relay_status": relay_status})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    try:
        sample_image = cv2.imread('sample_image.jpg')
        person_count = detect_person(sample_image)
        socketio.emit('person_count', {'count': person_count})
        # socketio.start_background_task(send_person_count)
        send_person_count()
    except Exception as e:
        print(f'Error in handle_connect: {e}')


def send_person_count():
    while True:
        try:
            image_url = "http://192.168.200.62/1280x720.jpg"
            response = requests.get(image_url)
            image_data = np.frombuffer(response.content, np.uint8)
            frame = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            if frame is not None:
                person_count = detect_person(frame)
                socketio.emit('person_count', {'count': person_count})
            else:
                print('Failed to decode the image')
            time.sleep(2)  # Send person count every 2 seconds
        except Exception as e:
            print(f'Error in send_person_count: {e}')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
