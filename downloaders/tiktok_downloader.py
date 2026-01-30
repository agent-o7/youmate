import os
from yt_dlp import YoutubeDL


def download_tiktok(url, output_dir='downloads'):
    """Download a TikTok URL (or generic short-video URL) using yt-dlp.

    Returns the full path to the downloaded file.
    """
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename
