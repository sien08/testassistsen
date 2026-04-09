from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8728995215:AAHqXJ0Jy1kAag8gTLuZHlxy0kgzhYq5HFs"
CLAUDE_API_KEY = "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"

def ask_ai(prompt):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-3-5-haiku-20241022",  # hemat dulu
        "max_tokens": 300,
        "messages": [{"role": "user", "content": prompt}]
    }

    res = requests.post(url, json=data, headers=headers)
    return res.json()["content"][0]["text"]

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.json

    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    reply = ask_ai(text)

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return "ok"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
