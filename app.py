import logging
from flask import Flask, jsonify, request

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Middleware para logar requisições
@app.before_request
def log_request_info():
    logger.info(f"Recebendo requisição: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    if request.method in ["POST", "PUT", "PATCH"]:
        logger.info(f"Payload: {request.get_json()}")

# Middleware para logar respostas
@app.after_request
def log_response_info(response):
    logger.info(f"Enviando resposta: {response.status}")
    logger.info(f"Headers: {dict(response.headers)}")
    logger.info(f"Body: {response.get_json()}")
    return response

@app.route('/notificacao', methods=['GET'])
def notificacao():
    print("NOTIFICAÇÃO PRINT")
    logger.info("Requisição recebida em /notificacao")
    return jsonify({"mensagem": "Notificação recebida"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
