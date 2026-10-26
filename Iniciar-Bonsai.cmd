@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Falta el entorno Python del proyecto.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m mira.launch_model
pause
