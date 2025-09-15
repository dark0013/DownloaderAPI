from fastapi import FastAPI
from routers import media_router

app = FastAPI(title="YouTube Downloader API")
app.include_router(media_router.router)
