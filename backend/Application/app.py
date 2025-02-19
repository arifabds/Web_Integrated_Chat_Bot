from flask import Flask, jsonify, request
from flask_cors import CORS
from ..Generation.generator import Generator

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "çalışır durumda"}), 200

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt_from_frontend = data.get("userPrompt")

        print("\nFrontend'den gelen mesaj şu şekilde:", prompt_from_frontend, "\n")
        
        if not prompt_from_frontend or prompt_from_frontend.strip() == "":
            prompt_from_frontend  = "Kullanıcı komutu boş veya eksik!"

        generator = Generator()

        result = generator.send_message(prompt_from_frontend)

        #print("\nModelden gelen yanıt:", result["response"], "\n")

        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500

        return jsonify({"status": "success", "response": result["response"]}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def create_app():
    return app