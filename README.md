# Simple YouTube & TikTok downloader (Flask + Socket.IO)

This project provides two small downloader wrappers around `yt-dlp` and a Flask app that uses Socket.IO to trigger downloads and notify the browser when the file is ready.

Requirements

- Python 3.9+
- See `requirements.txt`

Install

```bash
python -m pip install -r requirements.txt
```

Run

```bash
python app.py
```

Open http://localhost:5000 in your browser.

How it works

- Client emits a `download` event with `{url, source}`.
- Server runs yt-dlp to download into `downloads/`.
- Server emits `download_complete` with `{filename, url}` when done.
- Client receives the event and shows a link (auto-downloads).

Notes

- `yt-dlp` supports many sites. TikTok and YouTube should work in most cases, but some videos (DRM, private) may not download.
- For production usage, add authentication, input validation, and disk quota controls.
