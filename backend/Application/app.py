from flask import Flask, jsonify, request
from flask_cors import CORS
from ..Generation.generator import Generator

app = Flask(__name__)

# CORS Yapılandırması (Tüm route'lar için geçerli)
CORS(
    app,
    origins=["https://arifabds.github.io"],  # Frontend origin
    methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],  # Tüm metodları kapsa
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],  # Gerekli başlıklar
    supports_credentials=True,               # Kimlik doğrulama için
    expose_headers=["Authorization"]         # Frontend'in görmesi gereken başlıklar
)

@app.route('/health', methods=['GET'])
def health_check():
    response = jsonify({"status": "çalışır durumda"})
    response.headers.add("Access-Control-Allow-Origin", "https://arifabds.github.io")
    return response, 200

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    if request.method == "OPTIONS":
        # Preflight için özel yanıt
        response = jsonify({"message": "Preflight başarılı"})
        response.headers.add("Access-Control-Allow-Origin", "https://arifabds.github.io")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200
    
    try:
        data = request.get_json()
        prompt_from_frontend = data.get("userPrompt")

        if not prompt_from_frontend or prompt_from_frontend.strip() == "":
            prompt_from_frontend = "Kullanıcı komutu boş veya eksik!"

        generator = Generator()
        result = generator.send_message(prompt_from_frontend)

        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500

        response = jsonify({"status": "success", "response": result["response"]})
        response.headers.add("Access-Control-Allow-Origin", "https://arifabds.github.io")
        return response, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def create_app():
    return app