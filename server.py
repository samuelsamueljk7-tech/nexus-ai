from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import spark_state
from spark_brain import ask_spark
from command_router import handle_command
import pc_control

ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=None)

@app.route("/")
def index():
    return send_from_directory(ROOT, "index.html")

@app.route("/<path:name>")
def assets(name):
    path = ROOT / name
    if path.is_file():
        return send_from_directory(ROOT, name)
    return jsonify({"error": "Not found"}), 404

@app.route("/health")
def health():
    return jsonify({"ok": True, "service": "nexus"})

@app.route("/state")
def state():
    return jsonify({
        "status": spark_state.status,
        "command": spark_state.last_command,
        "response": spark_state.last_response,
        "control": spark_state.control_status,
        "hand": spark_state.hand_status,
    })

@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}
    text = str(data.get("command", "")).strip()
    if not text:
        return jsonify({"success": False, "response": "No command received."}), 400

    try:
        spark_state.last_command = text
        spark_state.status = "THINKING"

        result = handle_command(text)
        if result is None:
            result = ask_spark(text)

        action = str(result.get("action", "NONE"))
        target = str(result.get("target", ""))
        reply = str(result.get("reply", ""))

        # Actually execute the action chosen by the AI/router.
        if action != "NONE":
            spark_state.control_status = "EXECUTING"
            execution_reply = pc_control.execute_action(action, target)
            if execution_reply:
                reply = execution_reply
            spark_state.control_status = "READY"

        spark_state.status = "ONLINE"
        spark_state.last_response = reply
        return jsonify({
            "success": True,
            "response": reply,
            "action": action,
            "target": target,
        })

    except Exception as exc:
        print("[NEXUS COMMAND ERROR]", exc)
        spark_state.status = "ERROR"
        spark_state.control_status = "ERROR"
        return jsonify({"success": False, "response": str(exc)}), 500

if __name__ == "__main__":
    print("\n==============================================")
    print("              ⚡ SPARK AI")
    print("==============================================\n")
    print("Open: http://127.0.0.1:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
