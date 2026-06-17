@echo off
setlocal enabledelayedexpansion

rem --[[ INSTRUCTIONS ]]]--
rem 1. Place your koboldcpp.exe file in the "AI_SERVER" folder.
rem 2. Place your GGUF model file (e.g., "model.gguf") in the "AI_SERVER\models" folder.
rem --[[ END INSTRUCTIONS ]]]--

echo ===================================================
echo   SCANNING NETWORK STACK: ATHENA REPOSITORY CORE
echo ===================================================

set PORTS=8282 5002 5173

for %%P in (%PORTS%) do (
    echo Checking port %%P...
    for /f "tokens=5" %%A in ('netstat -aon ^| findstr /r /c:":%%P "') do (
        set PID=%%A
        if not "!PID!"=="" (
            echo Conflict detected on port %%P (PID: !PID!). Resetting port...
            taskkill /F /PID !PID! >nul 2>&1
        )
    )
)

echo.
echo ===================================================
echo   LAUNCHING ATHENA UNIVERSE RPG
echo ===================================================

set AI_SERVER_DIR=%~dp0AI_SERVER

rem Find the first .exe file in the AI_SERVER directory
for %%F in ("%AI_SERVER_DIR%\*.exe") do (
    set KOBOLDCPP_PATH=%%F
    goto found_exe
)

echo [ERROR] No koboldcpp.exe found in the AI_SERVER directory.
goto end

:found_exe
rem Find the first .gguf file in the models subdirectory
for %%F in ("%AI_SERVER_DIR%\models\*.gguf") do (
    set MODEL_PATH=%%F
    goto found_model
)

echo [ERROR] No .gguf model file found in the AI_SERVER\models directory.
goto end

:found_model
echo Starting KoboldCPP Engine (Port 5002)...
start "Athena AI Brain" /D "%AI_SERVER_DIR%" "%KOBOLDCPP_PATH%" --model "%MODEL_PATH%" --context 8192 --port 5002 --quiet

echo Waiting for AI server to initialize (10 seconds)...
timeout /t 10 /nobreak

echo Starting Python FastAPI Engine (Port 8282)...
start "Athena Backend" cmd /k "cd "%~dp0backend" && uvicorn main:app --reload --host 0.0.0.0 --port 8282"

echo Starting Vite Frontend Terminal...
start "Athena Frontend" cmd /k "cd "%~dp0frontend" && npm run dev"

echo Initialization loop complete.

:end
pause