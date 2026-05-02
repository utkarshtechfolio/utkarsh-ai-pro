from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# 🔐 PUT YOUR GROQ API KEY HERE
import os

# 🔐 API KEY (safe way)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-instant"

SYSTEM_PROMPT = """
You are Utkarsh AI Pro 🇮🇳
A smart, short and helpful AI assistant.
Answer clearly in simple language.
"""


@app.route("/")
def home():
    return render_template("index.html")


# 🤖 SAFE AI FUNCTION (NO CRASH)
def get_ai_reply(msg):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": msg}
            ]
        }

        res = requests.post(GROQ_URL, headers=headers, json=data, timeout=20)

        result = res.json()

        # ✅ SUCCESS RESPONSE
        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        # ❌ ERROR FROM GROQ (SHOW IT SAFE)
        return "⚠️ API Error: " + str(result)

    except Exception as e:
        return "⚠️ Connection Error"


@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").strip()

    if not msg:
        return jsonify({"reply": "⚠️ Please type something"})

    # 👋 FIRST GREETING ONLY ONCE
    if msg.lower() in ["hi", "hello", "hey"]:
        if not session.get("intro"):
            session["intro"] = True
            return jsonify({
                "reply": "👋 Hey there! I am 🇮🇳 Utkarsh AI Pro\nBuilt by Utkarsh Tech Folio, powered by Utkarsh Mishra.\n\n✨ Ask me anything — I’m here to help you today."
            })

    reply = get_ai_reply(msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    print("🚀 UTKARSH AI PRO RUNNING (GROQ MODE)")
    app.run(debug=True)