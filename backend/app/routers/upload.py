import os
import tempfile
from fastapi import APIRouter, UploadFile, File
from fastapi import HTTPException

from ..services.hls import convert_to_hls, generate_movie_id

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("")
async def upload_video(file: UploadFile = File(...)) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    suffix = os.path.splitext(file.filename)[1]
    # Write to a temporary file first
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        data = await file.read()
        tmp.write(data)
        tmp_path = tmp.name

    movie_id = generate_movie_id()
    try:
        output_dir = convert_to_hls(tmp_path, movie_id)
    finally:
        # Remove original uploaded temp
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    # Return manifest path served via /media
    return {
        "movie_id": movie_id,
        "manifest": f"/media/{movie_id}/index.m3u8",
        "dir": output_dir,
    }


