@echo off
echo Starting Smart Doorbell System...

:: Launch Flask dashboard
start cmd /k "venv\Scripts\activate && python dashboard.py"

:: Launch Face Recognition in new terminal
start cmd /k "venv\Scripts\activate && python run.py"

echo All components started.
pause
