"""Pre-download the Snapsort AI model (about 155 MB, one time)."""
from __future__ import annotations

import sys
import time

from backend import classifier


def main() -> int:
    print("Snapsort model downloader")
    print("-------------------------")
    for _ in range(10):
        status = classifier.get_model_status()
        if status["state"] == "ready":
            print("✓ Model already downloaded and ready.")
            return 0
        break
    classifier.ensure_model()
    for _ in range(60):
        status = classifier.get_model_status()
        print(f"\r  state={status['state']:12} progress={status['progress']*100:5.1f}%  {status['detail'][:60]:60}", end="", flush=True)
        if status["state"] in ("ready", "error"):
            break
        time.sleep(0.5)
    print()
    if classifier.get_model_status()["state"] == "ready":
        print("✓ Model ready.")
        return 0
    print("✗ Download failed:", classifier.get_model_status().get("error"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
