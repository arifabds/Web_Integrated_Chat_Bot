from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from ..Generation.generator import Generator

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# CORS Yapılandırması
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Sağlık kontrolü
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "çalışır durumda"}), 200


# Proxy Endpoint
@app.route('/proxy', methods=['POST'])
def proxy_request():
    try:
        data = request.json
        target_url = data.get('url')
        user_prompt = data.get('userPrompt')

        if not target_url or not user_prompt:
            return jsonify({"error": "Hedef URL ve userPrompt gerekli"}), 400

        # Render API istek kısmı
        response = requests.post(target_url, json={"userPrompt": user_prompt})

        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Generate Endpoint
@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    if request.method == "OPTIONS":
        return '', 200

    try:
        data = request.get_json()
        user_prompt = data.get("userPrompt")

        if not user_prompt:
            return jsonify({"status": "error", "message": "Prompt boş olamaz!"}), 400

        generator = Generator()
        result = generator.send_message(user_prompt)

        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500

        return jsonify({"status": "success", "response": result["response"]}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Beklenmeyen hata: {str(e)}")
    return jsonify({"error": str(e)}), 500


# Uygulama oluşturma
def create_app():
    return app
