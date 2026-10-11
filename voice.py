
import pyttsx3
import threading


# ============================================================
# SPARK VOICE ENGINE
# ============================================================

engine = pyttsx3.init()


# ============================================================
# VOICE SETTINGS
# ============================================================

engine.setProperty(
    "rate",
    190
)

engine.setProperty(
    "volume",
    1.0
)


# ============================================================
# FIND FEMALE WINDOWS VOICE
# ============================================================

voices = engine.getProperty(
    "voices"
)


for voice in voices:

    name = voice.name.lower()

    if (
        "zira" in name
        or
        "female" in name
    ):

        engine.setProperty(
            "voice",
            voice.id
        )

        print(
            "🎙️ Spark voice:",
            voice.name
        )

        break


# ============================================================
# VOICE LOCK
# ============================================================

voice_lock = threading.Lock()


# ============================================================
# SPEAK
# ============================================================

def speak(text):

    if not text:
        return

    print(
        "🔊 SPARK:",
        text
    )

    try:

        with voice_lock:

            engine.say(
                text
            )

            engine.runAndWait()

    except Exception as error:

        print(
            "VOICE ERROR:",
            error
        )


# ============================================================
# STOP VOICE
# ============================================================

def stop_voice():

    try:

        with voice_lock:

            engine.stop()

    except Exception as error:

        print(
            "VOICE STOP ERROR:",
            error
        )

