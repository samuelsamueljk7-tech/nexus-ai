@echo off
cd /d "C:\Users\Computer\Desktop\pc controller"

start "SPARK HUD" cmd /k "py -3.13 server.py"

timeout /t 2 /nobreak >nul

start "SPARK HAND" cmd /k "py -3.13 hand_tracker.py"

timeout /t 2 /nobreak >nul

start "SPARK VOICE" cmd /k "py -3.13 spark_voice.py"

timeout /t 3 /nobreak >nul

start "" "http://127.0.0.1:5000"

exit