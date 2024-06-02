import time
import requests
from flask import Flask
from flask_socketio import SocketIO
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Permitir todos los orígenes

PROMETHEUS_URL = 'http://prometheus:9090/api/v1/query'
CHECK_INTERVAL = 10

# Set your alert thresholds here
THRESHOLDS = {
    'soil_moisture': (10, 60),  # Min and max thresholds
    'air_temperature': (15, 30)  # Min and max thresholds
}

def fetch_sensor_data(sensor_id):
    soil_moisture_query = f'soil_moisture{{sensor_id="{sensor_id}"}}'
    air_temperature_query = f'air_temperature{{sensor_id="{sensor_id}"}}'

    soil_moisture_response = requests.get(PROMETHEUS_URL, params={'query': soil_moisture_query})
    air_temperature_response = requests.get(PROMETHEUS_URL, params={'query': air_temperature_query})

    if soil_moisture_response.status_code == 200 and air_temperature_response.status_code == 200:
        soil_moisture_result = soil_moisture_response.json()['data']['result']
        air_temperature_result = air_temperature_response.json()['data']['result']

        if soil_moisture_result and air_temperature_result:
            soil_moisture = float(soil_moisture_result[0]['value'][1])
            air_temperature = float(air_temperature_result[0]['value'][1])
            return {
                'sensor_id': sensor_id,
                'soil_moisture': soil_moisture,
                'air_temperature': air_temperature
            }
    return None

def check_sensors():
    while True:
        sensor_id = "1"  # Assuming a single sensor for simplicity
        data = fetch_sensor_data(sensor_id)
        if data:
            if not (THRESHOLDS['soil_moisture'][0] <= data['soil_moisture'] <= THRESHOLDS['soil_moisture'][1]):
                socketio.emit('new_alert', {'sensor_id': sensor_id, 'type': 'soil_moisture', 'value': data['soil_moisture']})
            if not (THRESHOLDS['air_temperature'][0] <= data['air_temperature'] <= THRESHOLDS['air_temperature'][1]):
                socketio.emit('new_alert', {'sensor_id': sensor_id, 'type': 'air_temperature', 'value': data['air_temperature']})
        time.sleep(CHECK_INTERVAL)

@app.route('/')
def index():
    return "Alert Service Running"

if __name__ == '__main__':
    thread = Thread(target=check_sensors)
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
