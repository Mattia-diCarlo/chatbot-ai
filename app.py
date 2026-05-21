from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

API_KEY = os.environ.get("API_KEY")
MODEL = "gemini-2.5-flash"


@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        persona = data.get("persona", "normale")

        # 🎭 PIRANDELLO MODE
        if persona == "pirandello":
            msg = user_message.lower()

            if any(x in msg for x in ["vita", "biografia", "chi sei"]):
                user_message = """
Sei Luigi Pirandello e racconta la tua vita:
- Agrigento 1867
- studi e formazione
- crisi familiare
- Nobel 1934
- maschere e identità
"""

            elif any(x in msg for x in ["opere", "mattia", "sei personaggi", "uno nessuno"]):
                user_message = """
Spiega le opere principali:
- Il fu Mattia Pascal
- Uno, nessuno e centomila
- Sei personaggi in cerca d’autore
Temi: identità, relativismo, maschere sociali
"""

            else:
                user_message = "Rispondi come Pirandello: " + user_message

        if not API_KEY:
            return jsonify({"reply": "API KEY mancante"}), 500

        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

        payload = {
            "contents": [
                {"parts": [{"text": user_message}]}
            ]
        }

        response = requests.post(url, json=payload, timeout=30)
        result = response.json()

        if "error" in result:
            return jsonify({"reply": "Errore AI: " + result["error"]["message"]})

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception as e:
        print(e)
        return jsonify({"reply": "Errore server"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)