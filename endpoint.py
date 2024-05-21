from flask import Flask, request

app = Flask(__name__)

@app.route('/print', methods=['POST'])
def print_request():
    data = request.get_json()
    print(data)
    return 'Data received and printed', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
