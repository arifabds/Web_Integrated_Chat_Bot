from flask import Flask, jsonify, request
from flask_cors import CORS
from ..Generation.generator import Generator

app = Flask(__name__)

CORS(
    app,
    origins=["https://arifabds.github.io", "https://arifabds.github.io/chatbot"],  
    methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"], 
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"], 
    supports_credentials=True,            
    expose_headers=["Authorization"]      
)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "çalışır durumda"}), 200


@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():

    if request.method == "OPTIONS":
        return '', 200  

    try:
        data = request.get_json()
        prompt_from_frontend = data.get("userPrompt")

        if not prompt_from_frontend or prompt_from_frontend.strip() == "":
            prompt_from_frontend = "Kullanıcı komutu boş veya eksik!"

     
        generator = Generator()
        result = generator.send_message(prompt_from_frontend)


        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500

        # Başarılı yanıt
        return jsonify({"status": "success", "response": result["response"]}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Uygulama oluşturma
def create_app():
    return app


