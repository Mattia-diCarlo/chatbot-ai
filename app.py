from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# 🔑 ENV VAR
API_KEY = os.environ.get("API_KEY")
MODEL = "gemini-2.5-flash"


# 🌐 FRONTEND
@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


# 🔍 TEST ROUTE (IMPORTANTISSIMO PER DEBUG)
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})


# 💬 CHAT ROUTE
@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"reply": "Errore: JSON non valido"}), 400

        user_message = data.get("message", "")
        persona = data.get("persona", "normale")

        # 🎭 PIRANDELLO MODE
        if persona == "pirandello":

            msg = user_message.lower()

            if any(x in msg for x in ["vita", "chi sei", "biografia"]):
                user_message = """
Sei Luigi Pirandello e racconta la tua vita in modo completo:
- nascita ad Agrigento nel 1867
- formazione e studi
- crisi familiare
- Premio Nobel 1934
- teoria dell’umorismo
- maschere e identità
"""

            elif any(x in msg for x in ["opere", "sei personaggi", "mattia", "uno nessuno"]):
                user_message = """
Spiega:
- Il fu Mattia Pascal
- Uno, nessuno e centomila
- Sei personaggi in cerca d’autore
Temi: identità, maschere, relativismo
"""

            else:
                user_message = f"Rispondi come Pirandello: {user_message}"

        # 🚨 CHECK API KEY
        if not API_KEY:
            return jsonify({"reply": "Errore: API KEY mancante su Render"}), 500

        # 🌐 GEMINI CALL
        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": user_message}]
                }
            ]
        }

        response = requests.post(url, json=payload, timeout=30)

        result = response.json()

        # ❌ API ERROR HANDLING
        if "error" in result:
            return jsonify({"reply": "⚠️ " + result["error"]["message"]})

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": "Errore server o AI"}), 500


# 🚀 RENDER START
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)