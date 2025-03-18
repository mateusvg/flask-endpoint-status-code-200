from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/notificacao', methods=['GET'])
def notificacao():
    return jsonify({"mensagem": "Notificação recebida"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
