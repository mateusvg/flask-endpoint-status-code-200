from flask import Flask, request, jsonify
import hmac
import hashlib
import base64

app = Flask(__name__)

# Configurações de segurança (substitua pela chave real compartilhada com AppDirect)
SHARED_SECRET = "seu_shared_secret"

def validate_signature(event_url, signature):
    """Valida a assinatura OAuth da requisição."""
    expected_signature = base64.b64encode(
        hmac.new(SHARED_SECRET.encode(), event_url.encode(), hashlib.sha256).digest()
    ).decode()
    return hmac.compare_digest(expected_signature, signature)

@app.route("/cancel", methods=["POST"])
def cancel_subscription():
    event_url = request.args.get("eventUrl")
    signature = request.headers.get("Authorization")
    
    if not event_url or not signature:
        return jsonify({"success": False, "errorCode": "MISSING_PARAMETERS", "message": "Parâmetros obrigatórios ausentes."}), 400
    
    if not validate_signature(event_url, signature):
        return jsonify({"success": False, "errorCode": "UNAUTHORIZED", "message": "Assinatura inválida."}), 401
    
    # Simula a recuperação das informações do evento (idealmente, você faria uma requisição para a API da AppDirect aqui)
    event_data = {
        "type": "SUBSCRIPTION_CANCEL",
        "account": {"accountIdentifier": "12345"},
        "creator": {"email": "admin@example.com"}
    }
    
    account_id = event_data.get("account", {}).get("accountIdentifier")
    if not account_id:
        return jsonify({"success": False, "errorCode": "ACCOUNT_NOT_FOUND", "message": "Conta não encontrada."}), 404
    
    # Processa o cancelamento da assinatura
    print(f"Cancelando assinatura para a conta {account_id}")
    
    return jsonify({"success": True, "message": "Assinatura cancelada com sucesso."})

if __name__ == "__main__":
    app.run(debug=True)
