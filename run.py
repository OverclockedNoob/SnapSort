"""Snapsort launcher — starts the local server and opens the app window.

Usage:
    python run.py                     # desktop window (falls back to browser)
    python run.py --no-browser        # just serve (for headless/remote use)
    python run.py --host 0.0.0.0 --port 8765
"""
from __future__ import annotations

import argparse
import os
import socket
import sys
import threading
import time
import webbrowser

import uvicorn

from backend import config  # noqa: F401  (ensures paths are initialised)
from backend.main import app


def _port_free(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1" if host in ("0.0.0.0", "::", "") else host, port)) != 0


def _find_port(host: str, start: int) -> int:
    for port in range(start, start + 50):
        if _port_free(host, port):
            return port
    return start


def main() -> None:
    ap = argparse.ArgumentParser(description="Snapsort — AI photo & video organizer")
    ap.add_argument("--host", default=os.environ.get("SNAPSORT_HOST", "127.0.0.1"))
    ap.add_argument("--port", type=int, default=int(os.environ.get("SNAPSORT_PORT", "8765")))
    ap.add_argument("--no-browser", action="store_true",
                    default=os.environ.get("SNAPSORT_NO_BROWSER") == "1")
    args = ap.parse_args()

    port = _find_port(args.host, args.port)
    display_host = "127.0.0.1" if args.host in ("0.0.0.0", "::", "") else args.host
    url = f"http://{display_host}:{port}"

    server = uvicorn.Server(uvicorn.Config(
        app, host=args.host, port=port, log_level="warning", access_log=False,
    ))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    for _ in range(150):
        if server.started:
            break
        time.sleep(0.1)

    print(f"\n  ✨ Snapsort is running at {url}\n  Press Ctrl+C to stop.\n")

    if not args.no_browser:
        opened = False
        try:
            import webview  # pywebview: optional native desktop window
            webview.create_window(
                "Snapsort — AI Photo & Video Organizer", url,
                width=1280, height=860, min_size=(980, 640),
                background_color="#0b0d14",
            )
            webview.start()
            opened = True
            server.should_exit = True
        except Exception:
            pass
        if not opened:
            try:
                webbrowser.open(url)
            except Exception:
                pass
        try:
            thread.join()
        except KeyboardInterrupt:
            server.should_exit = True
    else:
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            server.should_exit = True


if __name__ == "__main__":
    main()
