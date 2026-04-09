from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "8728995215:AAHqXJ0Jy1kAag8gTLuZHlxy0kgzhYq5HFs"
CLAUDE_API_KEY = "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"

# =========================
# TEST ROUTE (cek server hidup)
# =========================
@app.route("/", methods=["GET"])
def home():
    return "Server is alive"


# =========================
# CLAUDE FUNCTION
# =========================
def ask_ai(prompt):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-3-5-haiku-20241022",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}]
    }

    res = requests.post(url, json=data, headers=headers)

    print("CLAUDE RAW:", res.text)  # DEBUG

    try:
        return res.json()["content"][0]["text"]
    except:
        return "Error dari Claude API"


# =========================
# TELEGRAM WEBHOOK
# =========================
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    print("INCOMING:", data)  # DEBUG

    # Safety biar ga crash
    if "message" not in data:
        return "ok"

    if "text" not in data["message"]:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    # TEST DUMMY (biar tau webhook jalan)
    if text.lower() == "ping":
        reply = "pong"
    else:
        reply = ask_ai(text)

    print("REPLY:", reply)  # DEBUG

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return "ok"


# =========================
# RUN SERVER (RAILWAY FIX)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
