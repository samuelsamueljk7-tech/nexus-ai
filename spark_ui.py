from flask import Flask, send_from_directory, jsonify
from pathlib import Path
import threading
import webbrowser

BASE = Path(__file__).resolve().parent

app = Flask(__name__)


# ==============================
# MAIN PAGE
# ==============================

@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")


# ==============================
# CSS
# ==============================

@app.route("/style.css")
def style():
    return send_from_directory(BASE, "style.css")


# ==============================
# JAVASCRIPT
# ==============================

@app.route("/script.js")
def javascript():
    return send_from_directory(BASE, "script.js")


# ==============================
# CHARACTER IMAGE
# ==============================

@app.route("/spark_character.png")
def character():
    return send_from_directory(BASE, "spark_character.png")


# ==============================
# STATUS
# ==============================

@app.route("/status")
def status():

    return jsonify({
        "status": "online",
        "assistant": "Spark"
    })


# ==============================
# START
# ==============================

if __name__ == "__main__":

    print()
    print("==============================")
    print("          SPARK")
    print("==============================")
    print()
    print("Starting Spark interface...")
    print()

    threading.Timer(
        1.0,
        lambda: webbrowser.open(
            "http://127.0.0.1:5000"
        )
    ).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )