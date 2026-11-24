@echo off
setlocal
cd /d "%~dp0"

echo.
echo   Snapsort - first-time setup
echo   --------------------------
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo   [!] Python not found. Install it from https://www.python.org/downloads/
  echo       and tick "Add python.exe to PATH" during setup.
  echo.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo   Creating a virtual environment...
  python -m venv .venv
)

echo   Installing dependencies (this happens once)...
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo   [!] Installation failed. Check your internet connection and try again.
  pause
  exit /b 1
)

echo   Installing the optional native window...
".venv\Scripts\python.exe" -m pip install pywebview >nul 2>nul
if errorlevel 1 echo   (Native window unavailable - Snapsort will open in your browser instead.)

echo.
echo   Downloading the AI model (about 155 MB, one time)...
".venv\Scripts\python.exe" download_model.py
if errorlevel 1 (
  echo.
  echo   [!] Model download failed. Snapsort will retry automatically on first run.
)

echo.
echo   Setup complete! Double-click start.bat to launch Snapsort.
echo.
pause
