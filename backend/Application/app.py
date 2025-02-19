from flask import Flask, jsonify, request
from flask_cors import CORS
from ..Generation.generator import Generator

app = Flask(__name__)

# CORS Yapılandırması (Tüm route'lar için geçerli)
CORS(
    app,
    origins=["https://arifabds.github.io"],  # Frontend origin
    methods=["GET", "POST", "OPTIONS"],       # İzin verilen metodlar
    allow_headers=["Content-Type", "Authorization"],  # İzin verilen başlıklar
    supports_credentials=True                # Cookie veya auth header'lar için
)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "çalışır durumda"}), 200

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    try:
        # Preflight OPTIONS isteği için otomatik yanıt (flask_cors halleder)
        if request.method == "OPTIONS":
            return jsonify({"message": "Preflight başarılı"}), 200
        
        # Ana POST işlemi
        data = request.get_json()
        prompt_from_frontend = data.get("userPrompt")

        if not prompt_from_frontend or prompt_from_frontend.strip() == "":
            prompt_from_frontend = "Kullanıcı komutu boş veya eksik!"

        generator = Generator()
        result = generator.send_message(prompt_from_frontend)

        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500

        return jsonify({"status": "success", "response": result["response"]}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def create_app():
    return app