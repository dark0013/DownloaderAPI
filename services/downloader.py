import yt_dlp
import logging
import threading

logging.basicConfig(level=logging.INFO)

def get_ydl_options(download_type: str, folder: str) -> dict:
    """Configura yt_dlp según el tipo de descarga usando título del video como nombre de archivo."""
    outtmpl = f"{folder}/%(title)s-%(id)s.%(ext)s"

    if download_type == "audio":
        return {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        }
    else:
        return {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': outtmpl,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        }

def download_file(url: str, ydl_opts: dict):
    """Ejecuta la descarga con yt_dlp en un hilo."""
    logging.info(f"Iniciando descarga: {url}")
    thread = threading.Thread(target=lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
    thread.start()
    thread.join()
    logging.info("Descarga completada")
