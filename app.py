from flask import Flask, request, jsonify
import logging
import requests
from requests_oauthlib import OAuth1

app = Flask(__name__)

# Configuração de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

oauth_consumer_key = "F9hXCJElZF"
oauth_consumer_secret = "VRWXj1gARHpyNbhPwanM"

def validate_oauth_signature(headers):
    """Valida a assinatura OAuth recebida na requisição."""
    if 'Authorization' not in headers:
        logging.error("Cabeçalho de autorização ausente.")
        return False
    # Aqui pode-se adicionar lógica para validar a assinatura OAuth corretamente.
    return True

@app.route('/cancel', methods=['GET'])
def cancel_subscription():
    event_url = request.args.get('eventUrl')
    if not event_url:
        logging.error("Parâmetro eventUrl ausente na solicitação.")
        return jsonify({"success": False, "error": "Missing eventUrl parameter"}), 400
    
    logging.info(f"Recebida solicitação de cancelamento: {event_url}")
    
    # Valida assinatura OAuth
    if not validate_oauth_signature(request.headers):
        return jsonify({"success": False, "error": "Invalid OAuth signature"}), 403
    
    # Obtém detalhes do evento
    auth = OAuth1(oauth_consumer_key, oauth_consumer_secret)
    response = requests.get(event_url, auth=auth)
    
    if response.status_code != 200:
        logging.error(f"Falha ao obter detalhes do evento: {response.text}")
        return jsonify({"success": False, "error": "Failed to fetch event details"}), 500
    
    event_data = response.json()
    logging.info(f"Detalhes do evento recebidos: {event_data}")
    
    # Processa o evento de cancelamento
    if event_data.get('type') == 'SUBSCRIPTION_CANCEL':
        account_id = event_data.get('payload', {}).get('account', {}).get('accountIdentifier')
        if account_id:
            logging.info(f"Cancelando assinatura para conta {account_id}")
            return jsonify({"success": True, "message": "Subscription canceled successfully"}), 200
        else:
            logging.error("Identificador da conta ausente no evento.")
            return jsonify({"success": False, "error": "Account identifier missing"}), 400
    
    logging.warning("Tipo de evento inesperado recebido.")
    return jsonify({"success": False, "error": "Invalid event type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
