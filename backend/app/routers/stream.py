from fastapi import APIRouter, Path

router = APIRouter(prefix="/stream", tags=["stream"])


@router.get("/{movie_id}")
async def stream_movie_manifest(movie_id: str = Path(...)) -> dict:
    # Placeholder: will return .m3u8 URL
    return {"movie_id": movie_id, "m3u8": f"/media/{movie_id}/index.m3u8"}


