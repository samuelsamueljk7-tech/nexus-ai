import subprocess
import webbrowser
import time
import pyttsx3
import speech_recognition as sr

from ollama import chat


# ============================================================
# SPARK SETTINGS
# ============================================================

MODEL = "gemma3:1b"

program_running = True


# ============================================================
# TEXT TO SPEECH
# ============================================================

tts = pyttsx3.init()

tts.setProperty("rate", 175)
tts.setProperty("volume", 1.0)


def speak(text):

    print("SPARK:", text)

    try:
        tts.say(text)
        tts.runAndWait()

    except Exception as error:

        print("TTS ERROR:", error)


# ============================================================
# OLLAMA AI
# ============================================================

def ask_spark(command):

    try:

        response = chat(

            model=MODEL,

            messages=[

                {
                    "role": "system",

                    "content": """
You are Spark, a friendly local Windows AI assistant.

Keep your answers short and natural.

You are running locally through Ollama.
Do not claim that you performed a computer action
unless the Python program actually performed it.
"""
                },

                {
                    "role": "user",
                    "content": command
                }

            ]
        )

        return response.message.content

    except Exception as error:

        print("OLLAMA ERROR:", error)

        return "I'm having trouble connecting to my AI brain."


# ============================================================
# OPEN APPLICATION
# ============================================================

def open_application(name):

    name = name.lower().strip()

    applications = {

        "discord":
            r"C:\Users\Computer\AppData\Local\Discord\app-1.0.9254\Discord.exe",

        "chrome":
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        "notepad":
            "notepad.exe",

        "calculator":
            "calc.exe",

        "paint":
            "mspaint.exe",

        "explorer":
            "explorer.exe",

        "file explorer":
            "explorer.exe"

    }

    if name in applications:

        subprocess.Popen(
            applications[name]
        )

        speak("Opening " + name)

        return True

    return False


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_command(command):

    global program_running

    command = command.lower().strip()

    print("\nYOU:", command)


    # --------------------------------------------
    # REMOVE WAKE WORD
    # --------------------------------------------

    if command.startswith("hey spark"):

        command = command[9:].strip()

    elif command.startswith("spark"):

        command = command[5:].strip()


    # --------------------------------------------
    # STOP
    # --------------------------------------------

    if command in [
        "stop spark",
        "exit spark",
        "quit spark"
    ]:

        speak("Shutting down.")

        program_running = False

        return


    # --------------------------------------------
    # OPEN APPLICATION
    # --------------------------------------------

    if command.startswith("open "):

        target = command[5:].strip()

        if open_application(target):

            return


    # --------------------------------------------
    # WEBSITES
    # --------------------------------------------

    websites = {

        "youtube":
            "https://www.youtube.com",

        "google":
            "https://www.google.com",

        "instagram":
            "https://www.instagram.com",

        "chatgpt":
            "https://chatgpt.com"

    }


    if command.startswith("open "):

        target = command[5:].strip()

        if target in websites:

            webbrowser.open(
                websites[target]
            )

            speak("Opening " + target)

            return


    # --------------------------------------------
    # AI
    # --------------------------------------------

    speak(
        ask_spark(command)
    )


# ============================================================
# VOICE RECOGNITION
# ============================================================

def voice_loop():

    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300

    recognizer.dynamic_energy_threshold = True


    try:

        microphone = sr.Microphone()

    except Exception as error:

        print("MICROPHONE ERROR:", error)

        return


    with microphone as source:

        print()
        print("Calibrating microphone...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        print()
        print("====================================")
        print("       SPARK VOICE READY")
        print("====================================")
        print()
        print('Say "Hey Spark" followed by a command.')
        print()


    while program_running:

        try:

            with microphone as source:

                print("Listening...")

                audio = recognizer.listen(
                    source,
                    timeout=2,
                    phrase_time_limit=6
                )


            print("Recognizing...")

            command = recognizer.recognize_google(
                audio
            )


            process_command(command)


        except sr.WaitTimeoutError:

            continue


        except sr.UnknownValueError:

            print("Didn't understand.")


        except sr.RequestError:

            print("Speech recognition service unavailable.")

            time.sleep(2)


        except Exception as error:

            print(
                "VOICE ERROR:",
                error
            )

            time.sleep(1)


# ============================================================
# START
# ============================================================

print()
print("====================================")
print("          SPARK IS ONLINE")
print("====================================")
print()
print("AI:     Ollama / Gemma 3 1B")
print("VOICE:  Active")
print("PC:     Active")
print()
print('Say: "Hey Spark, open Discord"')
print()

voice_loop()

print()
print("Spark stopped.")