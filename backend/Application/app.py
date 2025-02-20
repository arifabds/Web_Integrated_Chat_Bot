from flask import Flask, jsonify, request
from flask_cors import CORS
from ..Generation.generator import Generator

# Flask Uygulaması
app = Flask(__name__)

# CORS Yapılandırması (Her route için geçerli)
CORS(
    app,
    origins=["https://arifabds.github.io", "https://arifabds.github.io/chatbot"],  
    methods=["GET", "POST", "OPTIONS"],       
    allow_headers=["Content-Type", "Authorization"],  
    supports_credentials=True
)

# Sağlık kontrolü
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "çalışır durumda"}), 200


# Generate Endpointi (CORS başlığı otomatik eklenecek)
@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    if request.method == "OPTIONS":
        return '', 200  # Preflight için basit yanıt

    try:
        # Kullanıcıdan gelen promptu al
        data = request.get_json()
        user_prompt = data.get("userPrompt")

        if not user_prompt or user_prompt.strip() == "":
            return jsonify({"status": "error", "message": "Prompt boş olamaz!"}), 400

        # Generator ile mesaj işleme
        generator = Generator()
        result = generator.send_message(user_prompt)

        # Hata kontrolü
        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500

        # Başarılı yanıt
        return jsonify({"status": "success", "response": result["response"]}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Uygulama oluşturma
def create_app():
    return app


