from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "bolt-crossfit", "version": "2.0"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
