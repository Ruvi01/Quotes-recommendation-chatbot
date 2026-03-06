from flask import Flask, jsonify, render_template, request
import requests

RASA_REST_URL = "http://localhost:5005/webhooks/rest/webhook"

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()
    sender = (payload.get("sender") or "web_user").strip()

    if not message:
        return jsonify({"reply": "Please type a message."}), 400

    try:
        response = requests.post(
            RASA_REST_URL,
            json={"sender": sender, "message": message},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        return jsonify(
            {
                "reply": (
                    "I could not reach the Rasa server. "
                    "Start it with: rasa run --enable-api --cors \"*\""
                )
            }
        ), 503

    data = response.json()
    if not data:
        return jsonify({"reply": "I did not generate a response. Try another prompt."})

    texts = [item.get("text", "") for item in data if item.get("text")]
    reply = "\n".join(texts).strip() or "I did not understand that."
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
