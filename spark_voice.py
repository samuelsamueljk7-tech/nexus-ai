import speech_recognition as sr
import pyttsx3
import time

from spark_brain import ask_spark
from pc_control import execute_action


# ============================================================
# SPARK VOICE SYSTEM
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

speaker = pyttsx3.init()

speaker.setProperty(
    "rate",
    175
)

speaker.setProperty(
    "volume",
    1.0
)


# ============================================================
# SPEAK
# ============================================================

def speak(text):

    if not text:
        return

    print()
    print("🔊 SPARK:", text)

    speaker.say(text)
    speaker.runAndWait()


# ============================================================
# LISTEN
# ============================================================

def listen():

    try:

        with sr.Microphone() as source:

            print()
            print("🎤 Listening...")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        print("🧠 Recognizing...")

        text = recognizer.recognize_google(
            audio
        )

        print()
        print("YOU:", text)

        return text

    except sr.WaitTimeoutError:

        return None

    except sr.UnknownValueError:

        print("Couldn't understand that.")

        return None

    except sr.RequestError as error:

        print("Speech recognition error:")
        print(error)

        return None

    except Exception as error:

        print("Voice error:")
        print(error)

        return None


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_command(text):

    if not text:
        return

    result = ask_spark(text)

    action = result.get(
        "action",
        "NONE"
    )

    target = result.get(
        "target",
        ""
    )

    reply = result.get(
        "reply",
        ""
    )

    print()
    print("ACTION:", action)
    print("TARGET:", target)
    print("REPLY :", reply)

    # --------------------------------------------------------
    # NORMAL CONVERSATION
    # --------------------------------------------------------

    if action == "NONE":

        speak(reply)

        return

    # --------------------------------------------------------
    # PC ACTION
    # --------------------------------------------------------

    execution_result = execute_action(
        action,
        target
    )

    # Spark's AI-generated reply is spoken
    if reply:

        speak(reply)

    elif execution_result:

        speak(execution_result)


# ============================================================
# START
# ============================================================

def start_voice():

    print()
    print("======================================")
    print("          SPARK VOICE SYSTEM")
    print("======================================")
    print()

    print("🎤 Calibrating microphone...")

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

    print()
    print("🎤 Microphone ready.")
    print()

    speak(
        "Spark is online."
    )

    while True:

        try:

            command = listen()

            if command:

                lowered = command.lower().strip()

                if lowered in [
                    "stop spark",
                    "exit spark",
                    "quit spark",
                    "shutdown spark"
                ]:

                    speak(
                        "Shutting down."
                    )

                    break

                process_command(
                    command
                )

            time.sleep(0.1)

        except KeyboardInterrupt:

            print()
            print("Spark stopped.")

            break

        except Exception as error:

            print()
            print("Spark voice system stopped.")
            print(error)
            print()

            break


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    start_voice()