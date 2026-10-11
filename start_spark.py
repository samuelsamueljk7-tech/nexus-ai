import subprocess
import time
import webbrowser
import sys


# ============================================================
# SPARK ONE-CLICK STARTUP
# ============================================================

BASE_DIR = r"C:\Users\Computer\Desktop\pc controller"

PYTHON = sys.executable


print()
print("==============================================")
print("              SPARK AI SYSTEM")
print("==============================================")
print()
print("Starting Spark...")
print()


# ============================================================
# START FLASK HUD
# ============================================================

print("[1/3] Starting Spark HUD...")

server = subprocess.Popen(
    [PYTHON, "server.py"],
    cwd=BASE_DIR
)

time.sleep(3)


# ============================================================
# OPEN HUD
# ============================================================

print("[2/3] Opening Spark HUD...")

webbrowser.open(
    "http://127.0.0.1:5000"
)

time.sleep(1)


# ============================================================
# START HAND CONTROL
# ============================================================

print("[3/3] Starting hand control...")

hand = subprocess.Popen(
    [PYTHON, "hand_tracker.py"],
    cwd=BASE_DIR
)


# ============================================================
# START VOICE CONTROL
# ============================================================

print()
print("Starting voice control...")

voice = subprocess.Popen(
    [PYTHON, "spark_voice.py"],
    cwd=BASE_DIR
)


# ============================================================
# ONLINE
# ============================================================

time.sleep(3)

print()
print("==============================================")
print("              SPARK IS ONLINE")
print("==============================================")
print()
print("HUD        : ONLINE")
print("HAND       : ONLINE")
print("VOICE      : ONLINE")
print("OLLAMA     : READY")
print("PC CONTROL : READY")
print()
print("Talk naturally to Spark.")
print()
print("==============================================")
print()


# ============================================================
# KEEP SPARK RUNNING
# ============================================================

try:

    while True:

        time.sleep(1)


except KeyboardInterrupt:

    print()
    print("Stopping Spark...")


    # Stop all components

    server.terminate()

    hand.terminate()

    voice.terminate()


    print("Spark stopped.")