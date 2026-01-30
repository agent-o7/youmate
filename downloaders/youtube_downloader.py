import os
from yt_dlp import YoutubeDL


def download_youtube(url, output_dir='downloads'):
    """Download a YouTube (or generic) URL using yt-dlp.

    Returns the full path to the downloaded file.
    """
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # prepare_filename builds the actual output filename from the info
        filename = ydl.prepare_filename(info)
    return filename
