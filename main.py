from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import yt_dlp
import os
import uuid
import logging
import glob

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Carpeta principal y subcarpetas
BASE_DIR = "downloads"
AUDIO_DIR = f"{BASE_DIR}/audio"
VIDEO_DIR = f"{BASE_DIR}/video"

# Crear carpetas si no existen
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

def get_ydl_options(download_type: str, folder: str, unique_id: str) -> dict:
    """Devuelve la configuración de yt_dlp según el tipo de descarga."""
    if download_type == "audio":
        return {
            'format': 'bestaudio/best',
            'outtmpl': f"{folder}/{unique_id}.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
    else:
        return {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f"{folder}/{unique_id}.%(ext)s",
            'quiet': True,
            'no_warnings': True,
        }

@app.get("/download")
def download_media(
    url: str = Query(..., description="URL de YouTube"),
    type: str = Query("video", regex="^(video|audio)$", description="Tipo de descarga: 'video' o 'audio'")
):
    """Descarga un video o audio de YouTube y lo devuelve como respuesta."""
    unique_id = str(uuid.uuid4())
    folder = AUDIO_DIR if type == "audio" else VIDEO_DIR
    media_type = "audio/mpeg" if type == "audio" else "video/mp4"

    ydl_opts = get_ydl_options(type, folder, unique_id)

    try:
        logging.info(f"Iniciando descarga: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Buscar el archivo descargado real
        files = glob.glob(f"{folder}/{unique_id}.*")
        if files:
            filename = files[0]
            logging.info(f"Descarga completada: {filename}")
            return FileResponse(filename, media_type=media_type, filename=f"download.{filename.split('.')[-1]}")
        else:
            logging.error("Archivo descargado no encontrado")
            raise HTTPException(status_code=500, detail="Archivo descargado no encontrado")

    except Exception as e:
        logging.exception("Error al descargar el archivo")
        raise HTTPException(status_code=400, detail=str(e))
