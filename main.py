from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import yt_dlp
import os
import uuid
import glob
import threading
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Carpeta principal y subcarpetas
BASE_DIR = "downloads"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
VIDEO_DIR = os.path.join(BASE_DIR, "video")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

def get_ydl_options(download_type: str, folder: str, unique_id: str) -> dict:
    """Configura yt_dlp según el tipo de descarga."""
    if download_type == "audio":
        return {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(folder, f"{unique_id}.%(ext)s"),
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
            'format': 'bestvideo+bestaudio/best',  # fusiona video+audio
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(folder, f"{unique_id}.%(ext)s"),
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        }

def download_file(url: str, ydl_opts: dict):
    """Ejecuta la descarga con yt_dlp."""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.get("/download")
def download_media(
    url: str = Query(..., description="URL de YouTube"),
    type: str = Query("video", regex="^(video|audio)$", description="Tipo de descarga: 'video' o 'audio'")
):
    unique_id = str(uuid.uuid4())
    folder = AUDIO_DIR if type == "audio" else VIDEO_DIR
    media_type = "audio/mpeg" if type == "audio" else "video/mp4"

    ydl_opts = get_ydl_options(type, folder, unique_id)

    try:
        logging.info(f"Iniciando descarga: {url}")

        # Descargar en hilo separado para no bloquear la API
        thread = threading.Thread(target=download_file, args=(url, ydl_opts))
        thread.start()
        thread.join()

        # Buscar el archivo descargado
        files = glob.glob(os.path.join(folder, f"{unique_id}.*"))
        if not files:
            raise HTTPException(status_code=500, detail="Archivo descargado no encontrado")

        filename = files[0]

        # StreamingResponse para enviar archivo grande al cliente
        def iterfile():
            with open(filename, "rb") as f:
                while chunk := f.read(1024*1024):  # 1 MB por bloque
                    yield chunk

        logging.info(f"Descarga completada: {filename}")
        return StreamingResponse(iterfile(), media_type=media_type, headers={
            "Content-Disposition": f"attachment; filename=download.{filename.split('.')[-1]}"
        })

    except Exception as e:
        logging.exception("Error al descargar el archivo")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/files")
def list_files():
    """Devuelve todos los archivos descargados (audio y video)."""
    audio_files = [f for f in os.listdir(AUDIO_DIR) if os.path.isfile(os.path.join(AUDIO_DIR, f))]
    video_files = [f for f in os.listdir(VIDEO_DIR) if os.path.isfile(os.path.join(VIDEO_DIR, f))]

    return JSONResponse({
        "audio": audio_files,
        "video": video_files
    })
