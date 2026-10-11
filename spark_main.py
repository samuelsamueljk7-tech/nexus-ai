import subprocess
import time
import webbrowser
import os
import ctypes
import socket


# ============================================================
# SPARK AI SYSTEM
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HUD_URL = "http://127.0.0.1:5000"

STARTUP_SOUND = os.path.join(
    BASE_DIR,
    "jarvis_on.mp3"
)

SOUND_ALIAS = "spark_startup"


# ============================================================
# CHECK IF SPARK HUD IS ALREADY RUNNING
# ============================================================

def server_is_running():

    try:

        connection = socket.create_connection(
            ("127.0.0.1", 5000),
            timeout=0.2
        )

        connection.close()

        return True

    except OSError:

        return False


# ============================================================
# PLAY STARTUP SOUND
# ============================================================

def play_startup_sound():

    if not os.path.exists(STARTUP_SOUND):

        print()
        print("WARNING: jarvis_on.mp3 was not found.")
        print()
        print("Expected location:")
        print(STARTUP_SOUND)
        print()

        return

    try:

        winmm = ctypes.windll.winmm

        command = (
            f'open "{STARTUP_SOUND}" '
            f'type mpegvideo '
            f'alias {SOUND_ALIAS}'
        )

        winmm.mciSendStringW(
            command,
            None,
            0,
            None
        )

        winmm.mciSendStringW(
            f"play {SOUND_ALIAS}",
            None,
            0,
            None
        )

        print("🔊 Spark startup sound playing...")

    except Exception as error:

        print()
        print("STARTUP SOUND ERROR:", error)
        print()


# ============================================================
# STOP STARTUP SOUND
# ============================================================

def stop_startup_sound():

    try:

        ctypes.windll.winmm.mciSendStringW(
            f"close {SOUND_ALIAS}",
            None,
            0,
            None
        )

    except Exception:

        pass


# ============================================================
# START SPARK
# ============================================================

print()
print("==============================================")
print("              ⚡ SPARK AI SYSTEM")
print("==============================================")
print()

print("⚡ Initializing Spark...")
print()


# ============================================================
# DUPLICATE PROTECTION
# ============================================================

if server_is_running():

    print("==============================================")
    print("        ⚠️ SPARK IS ALREADY RUNNING")
    print("==============================================")
    print()
    print("HUD already detected on port 5000.")
    print("No new browser tab will be opened.")
    print("No duplicate Spark instance will be started.")
    print()

    raise SystemExit


# ============================================================
# STARTUP SOUND
# ============================================================

play_startup_sound()


# ============================================================
# START HUD SERVER
# ============================================================

print("🖥️ Starting Spark HUD...")

server = subprocess.Popen(

    ["py", "-3.13", "server.py"],

    cwd=BASE_DIR

)


# ============================================================
# WAIT FOR HUD SERVER
# ============================================================

print("⏳ Waiting for Spark HUD...")

hud_ready = False

for attempt in range(30):

    if server_is_running():

        hud_ready = True

        break

    time.sleep(0.2)


# ============================================================
# OPEN HUD
# ============================================================

if hud_ready:

    print("🌐 Opening Spark HUD...")

    webbrowser.open(
        HUD_URL
    )

else:

    print()
    print("⚠️ Spark HUD did not start correctly.")
    print()


# ============================================================
# START HAND CONTROLLER
# ============================================================

print("🖐️ Starting hand control...")

hand = subprocess.Popen(

    ["py", "-3.13", "hand_tracker.py"],

    cwd=BASE_DIR

)


# ============================================================
# START VOICE CONTROLLER
# ============================================================

print("🎙️ Starting voice control...")

voice = subprocess.Popen(

    ["py", "-3.13", "spark_voice.py"],

    cwd=BASE_DIR

)


# ============================================================
# SPARK ONLINE
# ============================================================

print()
print("==============================================")
print("             ⚡ SPARK IS ONLINE ⚡")
print("==============================================")
print()

print("HUD        : ACTIVE")
print("Voice      : ACTIVE")
print("Hand       : ACTIVE")
print("AI Brain   : OPENAI")
print("PC Control : ACTIVE")

print()
print("Startup sound : jarvis_on.mp3")
print()
print("Talk naturally to Spark.")
print()
print("Press CTRL+C to shut down Spark.")
print()

print("==============================================")
print()


# ============================================================
# KEEP SPARK RUNNING
# ============================================================

try:

    while True:

        time.sleep(1)


# ============================================================
# SHUTDOWN
# ============================================================

except KeyboardInterrupt:

    print()
    print("==============================================")
    print("          ⚡ SHUTTING DOWN SPARK")
    print("==============================================")
    print()

    # Stop startup sound
    stop_startup_sound()


    # Stop voice controller
    try:

        voice.terminate()

    except Exception:

        pass


    # Stop hand controller
    try:

        hand.terminate()

    except Exception:

        pass


    # Stop HUD server
    try:

        server.terminate()

    except Exception:

        pass


    # Give processes a moment to close
    time.sleep(0.5)


    print()
    print("✅ Voice control stopped.")
    print("✅ Hand control stopped.")
    print("✅ HUD server stopped.")
    print()
    print("⚡ SPARK OFFLINE")
    print()