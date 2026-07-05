@echo off
echo Starting Athena Universe...

set BASE_DIR=%~dp0

start "Athena Universe" wt.exe -w 0 nt --title "AI Engine" -d "%BASE_DIR%Ai Control Center" cmd /k "koboldcpp.exe --model GameBrain\unsloth.Q8_0.gguf --port 5002" ; new-tab --title "Python Backend" -d "%BASE_DIR%backend" cmd /k "uvicorn main:app --port 8282" ; new-tab --title "Vite Frontend" -d "%BASE_DIR%frontend" cmd /k "npm run dev"

echo All services launched!