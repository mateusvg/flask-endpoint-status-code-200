import logging
from flask import Flask, jsonify

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/notificacao', methods=['GET'])
def notificacao():
    logger.info("Requisição recebida em /notificacao")
    return jsonify({"mensagem": "Notificação recebida"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
