# Snapsort — AI Photo & Video Organizer

Point Snapsort at a messy folder. It looks at every photo and video, understands what's
inside, and **sorts everything into folders automatically** — thousands of files at a time.

```
Before                          After
📸 IMG_0001.jpg                  Sorted/
📸 IMG_0002.jpg                  ├── People/
📸 VID_2024.mp4                  │   ├── IMG_0001.jpg
📸 screenshot.png                │   └── VID_2024.mp4
📸 receipt.jpg                   ├── Food & Drinks/
📸 sunset.jpg                    │   └── IMG_0002.jpg
📸 ...                           ├── Screenshots/
                                 ├── Documents/
                                 ├── Travel & Nature/
                                 └── ...
```

- **Understands content** — an on-device vision model (CLIP) recognizes people, food,
  travel, screenshots, documents, pets, vehicles, events and memes.
- **Handles thousands of files** — batched analysis, parallel decoding, live progress
  and a time estimate. Roughly 10–15 photos/second on a normal laptop CPU.
- **You stay in control** — review every file, fix categories with one click, then move.
- **100% local and private** — nothing is uploaded anywhere. No account, no cloud.

---

## Quick start

**Windows**

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/) — tick
   **“Add python.exe to PATH”** during installation.
2. Double-click **`setup.bat`** (installs dependencies and downloads the AI model once).
3. Double-click **`start.bat`** — Snapsort opens in its own window.

**macOS**

1. Install Python 3 from [python.org](https://www.python.org/downloads/) or
   `brew install python`.
2. Double-click **`setup.command`** (right-click → Open the first time).
3. Double-click **`start.command`**.

**Linux / manual**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python download_model.py      # optional, auto-downloads on first run
.venv/bin/python run.py
```

The first launch downloads the AI model (~155 MB) to `~/.cache/snapsort/`. Every launch
after that starts in a couple of seconds.

---

## How to use it

1. **Choose a folder** — use the *Browse* button (native folder picker) or paste a path
   like `C:\Users\you\Pictures` or `/Users/you/Pictures`.
2. **Scan** — Snapsort finds all photos and videos, including subfolders.
3. **Customize categories (optional)** — add anything in plain English: *Sunsets*,
   *Weddings*, *Receipts*, *Diwali*… Each becomes a folder.
4. **Start AI sorting** — watch live progress, the files it has classified, and a
   running count per category.
5. **Review** — browse the grid, filter by category, search by filename. Click any
   thumbnail to move it to a different category.
6. **Move files** — confirm the destination and Snapsort moves everything into
   `<your folder>/<Sorted>/<Category>/`.

### Notes on moving files

- Files are **moved**, not copied — that keeps your disk from filling up. Make sure you
  have a backup before your first big sort, as with any organizer.
- Nothing is ever deleted. If a file can't be read or moved, it stays where it is and is
  listed in the summary.
- A manifest of every move (`_snapsort_manifest.json`) is written inside the destination
  folder, so you can always trace what went where.
- Name collisions are handled automatically: `photo.jpg` becomes `photo (2).jpg`.

---

## Supported formats

| Type | Formats |
|---|---|
| Photos | JPG, JPEG, PNG, HEIC, HEIF, WebP, GIF, BMP, TIFF, AVIF, JXL |
| Camera RAW | DNG, CR2, CR3, NEF, ARW, ORF, RW2, PEF, RAF |
| Videos | MP4, MOV, AVI, MKV, WebM, M4V, 3GP, MTS, M2TS, WMV, FLV |

Videos are classified by sampling a few frames, so a clip of a birthday party lands in
*Events & Parties* just like the photos do.

## Default categories

`People` · `Food & Drinks` · `Travel & Nature` · `Events & Parties` · `Screenshots` ·
`Documents` · `Pets & Animals` · `Vehicles` · `Memes & Graphics` — plus `Others` for
anything the model isn't confident about.

Remove the ones you don't need or add your own before analyzing. Custom categories are
described in plain English, e.g. *“a photo of sunsets”*.

---

## How it works (under the hood)

- **Model:** OpenAI CLIP ViT-B/32, exported to ONNX and quantized to int8. It runs on
  the CPU via `onnxruntime` — no GPU, no Python ML stack, no internet needed after the
  first download.
- **Zero-shot classification:** each category is described by a handful of natural-language
  prompts. Snapsort embeds them once, then compares every image against those embeddings
  and takes a softmax. Confidence below 30% goes to *Others*.
- **Pipeline:** files are decoded in parallel (Pillow for images incl. HEIC/RAW, OpenCV
  for video frames), batched into the model, and results stream to the UI while analysis
  continues.
- **App:** FastAPI + a single-page UI. It binds to `127.0.0.1` only, so nothing on your
  network can reach it. Optionally runs in a native window via `pywebview`.

## Performance tips

- Keep the folder on an internal SSD for the fastest scanning.
- Very long 4K videos take a little longer (Snapsort samples frames rather than decoding
  the whole clip).
- If you have tens of thousands of files, the review grid loads in chunks — keep scrolling.
- Close other heavy apps during analysis on older machines.

## Optional: build a standalone desktop app

You can package Snapsort into a single `.exe` (Windows) or `.app` (macOS) so it runs
without Python installed:

```bash
pip install pyinstaller
pyinstaller --name Snapsort --noconfirm --windowed \
  --add-data "static;static" \
  --add-data "sample_photos;sample_photos" \
  --collect-all pillow_heif --collect-all rawpy \
  run.py
```

The binary appears in `dist/`. The AI model is still downloaded to the user's cache on
first run (add `--include-model` logic yourself if you want it bundled).

## Troubleshooting

| Problem | Fix |
|---|---|
| “AI model is downloading…” takes a while | Normal on first run (~155 MB). It resumes/retries automatically. |
| `pick-folder` does nothing | Your Python build lacks Tk. Paste the folder path instead, or install `python3-tk`. |
| HEIC photos show as unreadable | Reinstall `pillow-heif` (`pip install -U pillow-heif`). |
| Port 8765 already in use | Run `python run.py --port 9000`. |
| Antivirus warns on first run | It's a local server binding to 127.0.0.1 — allow it, or run from source. |
| macOS says the app is damaged | `xattr -dr com.apple.quarantine Snapsort.app` |

## Privacy

Snapsort runs entirely on your machine. The only network access is the one-time model
download from Hugging Face. Your file paths, names and photos never leave the device.

## License

MIT — use it, change it, share it.
