@echo off
setlocal enabledelayedexpansion

rem --[[ CONFIGURATION ]]]--
rem Set the full path to your koboldcpp.exe and your desired model file.
set KOBOLDCPP_PATH="D:\Extra storage\koboldcpp.exe"
set MODEL_PATH="F:\LLM\Qwen2.5-Coder-14B-Instruct-Q5_K_M.gguf" --port 5001 --contextsize 8192 --usecublas
rem --[[ END CONFIGURATION ]]]--

echo ===================================================
echo   SCANNING NETWORK STACK: ATHENA REPOSITORY CORE
echo ===================================================

set PORTS=8282 5002 5174

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
echo   LAUNCHING GAME INTERFACE PIPELINE
echo ===================================================

echo Starting KoboldCPP Engine (Port 5002)...
for %%i in (%KOBOLDCPP_PATH%) do set KOBOLD_DIR=%%~dpi
start "Athena AI Brain" /D "%KOBOLD_DIR%" %KOBOLDCPP_PATH% --model %MODEL_PATH% --context 8192 --port 5002

echo Waiting for AI server to initialize (10 seconds)...
timeout /t 10 /nobreak

echo Starting Python FastAPI Engine (Port 8282)...
wt -d backend cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8282"

echo Starting Vite Frontend Terminal...
wt -d frontend cmd /k "npm run dev"

echo Initialization loop complete.
