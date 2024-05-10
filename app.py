from flask import Flask, render_template, request
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt://127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883  # Port of the MQTT broker
app.config['MQTT_REFRESH_TIME'] = 1.0  # Refresh time in seconds

mqtt = Mqtt(app)

# Function to handle messages received from MQTT
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f"Received message: Topic={topic}, Payload={payload}")

# Route to turn the device on
@app.route('/turn_on', methods=['POST'])
def turn_on():
    mqtt.publish('esp32/control', 'on')
    return 'Device turned on'

# Route to turn the device off
@app.route('/turn_off', methods=['POST'])
def turn_off():
    mqtt.publish('esp32/control', 'off')
    return 'Device turned off'

if __name__ == '__main__':
    app.run(debug=True)
