from flask import Flask, jsonify, request
from flask_cors import CORS
from ..Generation.generator import Generator

# Flask Uygulaması
app = Flask(__name__)

# CORS Yapılandırması
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


# Preflight OPTIONS Yanıtı
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "https://arifabds.github.io/chatbot",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
        return ('', 200, headers)


# Generate Endpointi
@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        user_prompt = data.get("userPrompt")

        if not user_prompt or user_prompt.strip() == "":
            return jsonify({"status": "error", "message": "Prompt boş olamaz!"}), 400

        generator = Generator()
        result = generator.send_message(user_prompt)

        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500

        response = jsonify({"status": "success", "response": result["response"]})
        response.headers.add("Access-Control-Allow-Origin", "https://arifabds.github.io/chatbot")
        return response, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



# Uygulama oluşturma
def create_app():
    return app


