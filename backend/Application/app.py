from flask import Flask, jsonify, request
from flask_cors import CORS
from ..Generation.generator import Generator

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# CORS Yapılandırması
CORS(app, resources={r"/*": {"origins": "*"}}, intercept_exceptions=True)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Sağlık kontrolü
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "çalışır durumda"}), 200

# Generate Endpoint
@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    if request.method == "OPTIONS":
        # CORS preflight için response
        response = jsonify()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        return response
    
    mesajApandisi = "bu sistemin nereye kadar çalıştığını gösteriyor\n"

    try:
        mesajApandisi += "try bloğuna girdi\n"
        data = request.get_json()
        mesajApandisi += f"data request.getjson ile alındı data şu {data}\n"
        user_prompt = data.get("userPrompt")
        mesajApandisi += f"userPrompt alındı o da şu {user_prompt}\n"

        if not user_prompt:
            return jsonify({"status": "error", "message": "Prompt boş olamaz!"}), 400

        generator = Generator()
        mesajApandisi += f"generator objesı oluştu\n"
        result = generator.send_message(user_prompt)

        mesajApandisi += f"result oluştu: {result}\n"

        if "error" in result:
            return jsonify({"status": "tüh ya error", "message": result["error"]}), 500

        return jsonify({"status": "success", "response": result["response"]}), 200

    except Exception as e:
        return jsonify({"status": f"{mesajApandisi}", "message": str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Beklenmeyen hata: {str(e)}")
    return jsonify({"error": str(e)}), 500


# Uygulama oluşturma
def create_app():
    return app
