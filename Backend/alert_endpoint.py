from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/alert', methods=['POST'])
def alert():
    alert_data = request.json
    try:
        alerts = alert_data.get('alerts', [])
        for alert in alerts:
            sensor_id = alert['labels'].get('sensor_id')
            values = alert.get('values', {})
            value = next(iter(values.values()), None)  # Get the first value in the dictionary

            # Emitir la alerta a todos los clientes conectados
            socketio.emit('new_alert', {'sensor_id': sensor_id, 'value': value})
        
        return jsonify({"status": "success", "message": "Alert received and notification sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    socketio.run(app, port=5000)
