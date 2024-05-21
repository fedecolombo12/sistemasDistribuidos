from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    print("Received Alert Data:", data)
    # Puedes añadir aquí más lógica para procesar los datos de la alerta
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
