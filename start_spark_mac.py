#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".spark-venv"
PYTHON = VENV / "bin" / "python"


def run(cmd):
    print("[RUN]", " ".join(map(str, cmd)))
    return subprocess.run(cmd, cwd=ROOT)


def ensure_venv():
    if not PYTHON.exists():
        print("[SETUP] Creating Spark environment...")
        r = subprocess.run([sys.executable, "-m", "venv", str(VENV)], cwd=ROOT)
        if r.returncode:
            raise SystemExit("Could not create the Spark virtual environment.")

    print("[SETUP] Installing/checking dependencies...")
    r = run([str(PYTHON), "-m", "pip", "install", "--upgrade", "pip"])
    if r.returncode:
        raise SystemExit("Could not update pip.")
    r = run([str(PYTHON), "-m", "pip", "install", "-r", "requirements.txt"])
    if r.returncode:
        raise SystemExit("Spark dependencies failed to install.")


def main():
    print("\n==============================================")
    print("              ⚡ SPARK AI")
    print("==============================================\n")

    print("[INFO] Spark uses Ollama locally; no paid API key is required.")
    print("[INFO] Make sure the Ollama app is running and model qwen3:4b is installed.")

    ensure_venv()

    env = os.environ.copy()
    env.setdefault("SPARK_MODEL", "qwen3:4b")
    env["PYTHONUNBUFFERED"] = "1"
    print("[START] Web UI + AI API")
    server = subprocess.Popen([str(PYTHON), "server.py"], cwd=ROOT, env=env)

    try:
        for _ in range(80):
            if server.poll() is not None:
                raise SystemExit("[ERROR] Spark web server stopped during startup.")
            try:
                with urllib.request.urlopen("http://127.0.0.1:5000/health", timeout=0.5) as response:
                    if response.status == 200:
                        break
            except Exception:
                time.sleep(0.25)
        else:
            raise SystemExit("[ERROR] Spark web server did not become ready.")

        print("[READY] Spark is running at http://127.0.0.1:5000")
        webbrowser.open("http://127.0.0.1:5000")
        print("[READY] Spark UI opened. Press Ctrl+C here to stop Spark.")
        server.wait()
    except KeyboardInterrupt:
        print("\n[STOP] Shutting down Spark...")
    finally:
        if server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=3)
            except subprocess.TimeoutExpired:
                server.kill()


if __name__ == "__main__":
    main()
