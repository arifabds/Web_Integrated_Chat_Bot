from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from ..Generation.generator import Generator

app = Flask(__name__)

CORS(app, origins=["https://arifabds.github.io/chatbot/"], methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight başarılı"})
        response.headers.add("Access-Control-Allow-Origin", "https://arifabds.github.io/chatbot/")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200


@app.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    return jsonify({"status": "çalışır durumda"}), 200

@app.route('/generate', methods=['POST', 'OPTIONS'])
@cross_origin()
def generate():
    # Preflight OPTIONS isteği
    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight başarılı"}), 200
    
    try:
        data = request.get_json()
        prompt_from_frontend = data.get("userPrompt")

        #print("\nFrontend'den gelen mesaj şu şekilde:", prompt_from_frontend, "\n")

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