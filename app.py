from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_mqtt import Mqtt  # Import Flask-MQTT

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session management

socketio = SocketIO(app)

# Create an instance of the Mqtt class and initialize it with your Flask app
mqtt = Mqtt(app)

@app.route('/')
def index():
    return render_template('index.html')  # Render your HTML page

@socketio.on('connect')
def handle_connect():
    print('Client connected')  # Handle client connection

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')  # Handle client disconnection

@socketio.on('send_command')
def handle_send_command(command):
    print(f'Received command: {command}')
    # Publish command to MQTT topic to control ESP32 devices

# Handle MQTT messages and emit updates to clients
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    print(f"Received message: Topic={topic}, Payload={payload}")
    # Emit message payload to clients
    socketio.emit('mqtt_message', {'topic': topic, 'payload': payload})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
