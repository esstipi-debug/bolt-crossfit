from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://qvcrpwfwqjmuaeaybycn.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_YbUSxwE3s9kLgI6he0JbGw_XtdBcIPo")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8329833479:AAEyoKFEpOspoo_NXlK_e7XKpUTO3lppgKA")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "BOLT API Online", "version": "1.0"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "bolt-crossfit"})

def send_telegram_message(chat_id, text):
    """Send a message to a Telegram chat"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        requests.post(url, json=data)
        print(f"✉️ Mensaje enviado a {chat_id}: {text}")
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")

@app.route("/webhook/telegram", methods=["GET", "POST"])
def telegram_webhook():
    if request.method == "GET":
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json()
        
        if "message" in data:
            message = data["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            
            print(f"📨 Mensaje recibido: {text} (Chat ID: {chat_id})")
            
            if text == "/start":
                response_text = "¡Hola! Bienvenido a BOLT CrossFit Performance."
            else:
                response_text = f"Recibido: {text}"

            send_telegram_message(chat_id, response_text)
        
        return jsonify({"ok": True})
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
