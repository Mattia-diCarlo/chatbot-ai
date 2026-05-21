from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


    try:
        data = request.json
        user_message = data.get("message", "")
        persona = data.get("persona", "normale")

        # 🎭 PIRANDELLO 2.0
        if persona == "pirandello":

            msg = user_message.lower()

            # 🧠 VITA
            if any(x in msg for x in ["vita", "chi sei", "parlami di te", "biografia"]):

                user_message = """
Sei Luigi Pirandello e racconta la tua vita in modo completo.

Includi:
- nascita ad Agrigento nel 1867
- studi e formazione
- crisi familiare e psicologica
- rapporto con la moglie malata
- Premio Nobel per la letteratura (1934)
- nascita del concetto di umorismo
- teoria delle maschere e identità

Racconta in prima persona.
"""

            # 📚 OPERE
            elif any(x in msg for x in ["opera", "opere", "sei personaggi", "fu mattia", "uno nessuno"]):

                user_message = """
Sei Luigi Pirandello e spiega le tue opere principali:

- Il fu Mattia Pascal
- Uno, nessuno e centomila
- Sei personaggi in cerca d’autore

Spiega i temi:
- identità
- maschera sociale
- relativismo della verità
- crisi dell’io
"""

            # 🎭 TEMI
            elif any(x in msg for x in ["maschera", "identità", "umorismo", "tema"]):

                user_message = """
Sei Luigi Pirandello e spiega i tuoi temi:

- maschere sociali
- identità multipla
- umorismo (sentimento del contrario)
- crisi dell’individuo

Tono filosofico e riflessivo.
"""

            # 🎭 DEFAULT
            else:

                user_message = (
                    "Rispondi come Luigi Pirandello in modo filosofico e teatrale. "
                    "Domanda: " + user_message
                )

        # 🌐 GEMINI API
        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": user_message}]
                }
            ]
        }

        response = requests.post(url, json=payload)
        result = response.json()

        if "error" in result:
            return jsonify({"reply": "⚠️ " + result["error"]["message"]})

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception as e:
        print(e)
        return jsonify({"reply": "Errore server o AI"})


if __name__ == "__main__":
    app.run(debug=True)