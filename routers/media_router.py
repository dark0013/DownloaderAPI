from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from services.downloader import get_ydl_options, download_file
from utils.file_manager import get_folder, find_latest_file
import os

router = APIRouter()

@router.get("/download")
def download_media(
    url: str = Query(..., description="URL de YouTube"),
    type: str = Query("video", regex="^(video|audio)$", description="Tipo de descarga")
):
    folder = get_folder(type)
    media_type = "audio/mpeg" if type == "audio" else "video/mp4"

    ydl_opts = get_ydl_options(type, folder)
    
    try:
        download_file(url, ydl_opts)

        filename = find_latest_file(folder)
        if not filename:
            raise HTTPException(status_code=500, detail="Archivo descargado no encontrado")

        def iterfile():
            with open(filename, "rb") as f:
                while chunk := f.read(1024*1024):
                    yield chunk

        return StreamingResponse(
            iterfile(), media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={os.path.basename(filename)}"}
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/files")
def list_files():
    from utils.file_manager import AUDIO_DIR, VIDEO_DIR
    audio_files = [f for f in os.listdir(AUDIO_DIR) if os.path.isfile(os.path.join(AUDIO_DIR, f))]
    video_files = [f for f in os.listdir(VIDEO_DIR) if os.path.isfile(os.path.join(VIDEO_DIR, f))]

    return JSONResponse({"audio": audio_files, "video": video_files})
