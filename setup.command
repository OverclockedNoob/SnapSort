#!/bin/bash
cd "$(dirname "$0")"

echo
echo "  Snapsort - first-time setup"
echo "  --------------------------"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "  [!] Python 3 not found. Install it from https://www.python.org/downloads/"
  read -r -p "  Press Enter to close..."
  exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
  echo "  Creating a virtual environment..."
  python3 -m venv .venv || { read -r -p "  Press Enter to close..."; exit 1; }
fi

echo "  Installing dependencies (this happens once)..."
.venv/bin/python -m pip install --upgrade pip >/dev/null
.venv/bin/python -m pip install -r requirements.txt || { read -r -p "  Press Enter to close..."; exit 1; }

echo "  Installing the optional native window..."
.venv/bin/python -m pip install pywebview >/dev/null 2>&1 || echo "  (Native window unavailable - Snapsort will open in your browser instead.)"

echo
echo "  Downloading the AI model (about 155 MB, one time)..."
.venv/bin/python download_model.py || echo "  [!] Model download failed - Snapsort will retry on first run."

echo
echo "  Setup complete! Double-click start.command to launch Snapsort."
read -r -p "  Press Enter to close..."
