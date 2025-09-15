from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import yt_dlp
import os
import uuid

app = FastAPI()

@app.get("/download")
def download_media(
    url: str = Query(..., description="URL de YouTube"),
    type: str = Query("video", regex="^(video|audio)$", description="Tipo de descarga: 'video' o 'audio'")
):
    unique_id = str(uuid.uuid4())
    output_template = f"{unique_id}.%(ext)s"

    if type == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        expected_ext = "mp3"
        media_type = "audio/mpeg"
        filename = f"{unique_id}.mp3"

    else:  # video
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }
        expected_ext = "mp4"
        media_type = "video/mp4"
        filename = f"{unique_id}.mp4"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(filename):
            return FileResponse(filename, media_type=media_type, filename=f"download.{expected_ext}")
        else:
            raise HTTPException(status_code=500, detail="Archivo descargado no encontrado")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 