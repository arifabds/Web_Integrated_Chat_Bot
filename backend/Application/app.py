from flask import Flask, jsonify, request
from flask_cors import CORS
from Generation.generator import Generator

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "çalışır durumda"}), 200

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        context = data.get("context")
        
        if not context or context.strip() == "":
            context = "Kullanıcı komutu boş veya eksik!"

        generator = Generator()

        result = generator.send_message(context)

        #print("\nModelden gelen yanıt:", result["response"], "\n")

        if "error" in result:
            return jsonify({"status": "error", "message": result["error"]}), 500

        return jsonify({"status": "success", "response": result["response"]}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def create_app():
    return app