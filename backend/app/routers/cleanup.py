from fastapi import APIRouter, Path
from ..services.cleanup import delete_movie_dir

router = APIRouter(prefix="/cleanup", tags=["cleanup"])


@router.post("/{movie_id}")
async def cleanup_movie(movie_id: str = Path(...)) -> dict:
    deleted = delete_movie_dir(movie_id)
    return {"movie_id": movie_id, "deleted": deleted}


