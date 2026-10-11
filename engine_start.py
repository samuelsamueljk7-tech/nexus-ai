
import speech_recognition as sr
import subprocess
import os

from voice import speak


# ============================================================
# SPARK ENGINE CONTROLLER
# ============================================================

SPARK_FOLDER = r"C:\Users\Computer\Desktop\pc controller"

SPARK_MAIN = os.path.join(
    SPARK_FOLDER,
    "spark_main.py"
)


# ============================================================
# ENGINE STATE
# ============================================================

engine_running = False
spark_process = None


# ============================================================
# VOICE RECOGNITION
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

microphone = sr.Microphone()


# ============================================================
# START ENGINE
# ============================================================

def start_engine():

    global engine_running
    global spark_process

    if engine_running:

        speak("Spark is already online.")

        return

    print()
    print("==========================================")
    print("          SPARK ENGINE IGNITION")
    print("==========================================")
    print()

    try:

        engine_running = True

        # --------------------------------------------
        # STARTUP VOICE
        # --------------------------------------------

        speak("Initializing systems.")

        # --------------------------------------------
        # START SPARK MAIN PROCESS
        # --------------------------------------------

        spark_process = subprocess.Popen(

            [
                "py",
                "-3.13",
                SPARK_MAIN
            ],

            cwd=SPARK_FOLDER

        )

        print("Spark engine started.")

    except Exception as error:

        engine_running = False
        spark_process = None

        print(
            "ENGINE START ERROR:",
            error
        )

        speak(
            "Engine startup failed."
        )


# ============================================================
# STOP ENGINE
# ============================================================

def stop_engine():

    global engine_running
    global spark_process

    if not engine_running:

        speak("Spark is already offline.")

        return

    print()
    print("==========================================")
    print("          SPARK ENGINE SHUTDOWN")
    print("==========================================")
    print()

    try:

        # --------------------------------------------
        # STOP SPARK PROCESS TREE
        # --------------------------------------------

        if spark_process is not None:

            print("Stopping Spark processes...")

            subprocess.run(

                [
                    "taskkill",
                    "/PID",
                    str(spark_process.pid),
                    "/T",
                    "/F"
                ],

                stdout=subprocess.DEVNULL,

                stderr=subprocess.DEVNULL

            )

            spark_process = None


        engine_running = False

        print("Spark engine stopped.")

        speak(
            "Spark engine offline."
        )

    except Exception as error:

        print(
            "ENGINE STOP ERROR:",
            error
        )

        engine_running = False
        spark_process = None


# ============================================================
# MICROPHONE CALIBRATION
# ============================================================

with microphone as source:

    print()
    print("==========================================")
    print("          SPARK STANDBY SYSTEM")
    print("==========================================")
    print()

    print(
        "Calibrating microphone..."
    )

    recognizer.adjust_for_ambient_noise(

        source,

        duration=1

    )

    print()
    print("==========================================")
    print("          ⚡ SPARK STANDBY")
    print("==========================================")
    print()

    print(
        'Say "START ENGINE"'
    )

    print(
        'Say "STOP ENGINE"'
    )

    print()


# ============================================================
# STANDBY LOOP
# ============================================================

while True:

    try:

        with microphone as source:

            audio = recognizer.listen(

                source,

                timeout=None,

                phrase_time_limit=4

            )


        # ====================================================
        # RECOGNIZE
        # ====================================================

        try:

            command = recognizer.recognize_google(

                audio

            )

            command = command.lower().strip()

            print(
                "HEARD:",
                command
            )

        except sr.UnknownValueError:

            continue

        except sr.RequestError as error:

            print(
                "VOICE ERROR:",
                error
            )

            continue


        # ====================================================
        # START ENGINE
        # ====================================================

        if (

            "start engine" in command

            or

            "engine start" in command

            or

            "activate spark" in command

        ):

            start_engine()

            continue


        # ====================================================
        # STOP ENGINE
        # ====================================================

        if (

            "stop engine" in command

            or

            "engine stop" in command

            or

            "shutdown spark" in command

        ):

            stop_engine()

            continue


    # ========================================================
    # CTRL+C
    # ========================================================

    except KeyboardInterrupt:

        print()
        print(
            "Spark standby stopped."
        )

        break


    # ========================================================
    # OTHER ERROR
    # ========================================================

    except Exception as error:

        print()
        print(
            "ERROR:",
            error
        )

        print()

