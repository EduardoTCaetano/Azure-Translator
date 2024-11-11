from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
TRANSLATOR_REGION = os.getenv("TRANSLATOR_REGION", "westus")  

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get("text")
    to_language = data.get("to_language", "en")

    if not text:
        return jsonify({"error": "Texto para tradução é obrigatório"}), 400

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": TRANSLATOR_REGION,
        "Content-Type": "application/json"
    }

    body = [{"text": text}]
    params = {"api-version": "3.0", "to": to_language}

    try:
        response = requests.post(
            f"{AZURE_TRANSLATOR_ENDPOINT}/translate",
            headers=headers,
            params=params,
            json=body
        )
        response.raise_for_status()
        translation = response.json()
        translated_text = translation[0]["translations"][0]["text"]

        return jsonify({"translated_text": translated_text})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
