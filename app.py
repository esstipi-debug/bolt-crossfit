from flask import Flask, request, jsonify
import os
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

@app.route("/webhook/telegram", methods=["POST"])
def telegram_webhook():
    try:
        data = request.get_json()
        
        if "message" in data:
            message = data["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            
            print(f"📨 Mensaje recibido: {text} (Chat ID: {chat_id})")
            
            if text == "/start":
                response_text = "¡Hola! Bienvenido a BOLT CrossFit Performance."
                print(f"✅ Respondiendo: {response_text}")
            else:
                response_text = f"Recibido: {text}"
                print(f"✅ Respondiendo: {response_text}")
        
        return jsonify({"ok": True})
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
