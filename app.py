import os
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

from downloaders.youtube_downloader import download_youtube
from downloaders.tiktok_downloader import download_tiktok


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')

app = Flask(__name__, static_folder='static', template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/downloads/<path:filename>')
def downloads(filename):
    # serve completed downloads as attachments
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


@socketio.on('download')
def handle_download(data):
    """Receive a download request from the client and start a background task."""
    url = data.get('url')
    source = data.get('source', 'youtube')
    if not url:
        socketio.emit('error', {'message': 'No URL provided'})
        return
    socketio.start_background_task(_download_task, url, source)


def _download_task(url, source):
    try:
        if source == 'tiktok':
            filepath = download_tiktok(url, output_dir=DOWNLOAD_DIR)
        else:
            filepath = download_youtube(url, output_dir=DOWNLOAD_DIR)
        filename = os.path.basename(filepath)
        file_url = f'/downloads/{filename}'
        socketio.emit('download_complete', {'filename': filename, 'url': file_url})
    except Exception as e:
        socketio.emit('error', {'message': str(e)})


if __name__ == '__main__':
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    # Use eventlet for async workers; ensure eventlet is installed
    socketio.run(app, host='0.0.0.0', port=5000)
