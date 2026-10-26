@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Falta el entorno. Ejecuta primero Instalar-MIRA.ps1.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m mira.cli preparar
if errorlevel 1 (
  pause
  exit /b 1
)
echo.
echo Abre http://127.0.0.1:8000
echo Usuario: U-01. Clave local de demostracion: mira-demo
echo Para conversar inicia tambien Bonsai con Iniciar-Bonsai.cmd.
echo.
".venv\Scripts\python.exe" -m mira.cli servir
pause
