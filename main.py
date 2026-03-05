from flask import Flask, jsonify
import requests
import os
import time
import threading
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8329833479:AAEyoKFEpOspoo_NXlK_e7XKpUTO3lppgKA")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

last_update_id = 0

def send_message(chat_id, text):
    """Send a message to a Telegram chat"""
    try:
        response = requests.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def process_updates():
    """Poll for updates from Telegram"""
    global last_update_id

    while True:
        try:
            response = requests.get(
                f"{TELEGRAM_API_URL}/getUpdates",
                params={"offset": last_update_id + 1, "timeout": 30},
                timeout=35
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("ok") and data.get("result"):
                    for update in data["result"]:
                        last_update_id = update["update_id"]

                        if "message" in update:
                            message = update["message"]
                            chat_id = message["chat"]["id"]
                            text = message.get("text", "")

                            print(f"📨 Mensaje recibido: {text} (Chat ID: {chat_id})")

                            if text == "/start":
                                response_text = "¡Hola! Bienvenido a BOLT CrossFit Performance System. El sistema está online y listo."
                            else:
                                response_text = f"Recibido: {text}"

                            if send_message(chat_id, response_text):
                                print(f"✉️ Mensaje enviado exitosamente a {chat_id}")
                            else:
                                print(f"❌ Error enviando mensaje a {chat_id}")
        except Exception as e:
            print(f"Error in polling: {e}")

        time.sleep(1)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "BOLT API Online", "version": "2.0", "mode": "polling"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "bolt-crossfit", "mode": "polling"})

# Start polling in background thread
polling_thread = threading.Thread(target=process_updates, daemon=True)
polling_thread.start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
