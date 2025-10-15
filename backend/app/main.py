from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .routers.search import router as search_router
from .routers.stream import router as stream_router
from .routers.cleanup import router as cleanup_router
from .routers.upload import router as upload_router
from .background import start_cleanup_loop

app = FastAPI(title="Telegram Movie Streamer", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_allow_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# Routers
app.include_router(search_router)
app.include_router(stream_router)
app.include_router(cleanup_router)
app.include_router(upload_router)


# Static serving for HLS content (read-only)
media_root = f"{settings.temp_dir}/{settings.hls_dirname}"
app.mount("/media", StaticFiles(directory=media_root), name="media")


@app.on_event("startup")
async def _startup() -> None:
    # Start background cleanup task
    import asyncio
    asyncio.create_task(start_cleanup_loop())


