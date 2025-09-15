import os
import glob

BASE_DIR = "downloads"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
VIDEO_DIR = os.path.join(BASE_DIR, "video")

# Crear carpetas si no existen
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

def get_folder(download_type: str) -> str:
    return AUDIO_DIR if download_type == "audio" else VIDEO_DIR

def find_latest_file(folder: str) -> str:
    files = glob.glob(os.path.join(folder, "*"))
    if not files:
        return None
    return max(files, key=os.path.getctime)
