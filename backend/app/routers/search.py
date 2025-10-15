from fastapi import APIRouter, Query

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
async def search_movies(query: str = Query(..., min_length=2)) -> dict:
    # Placeholder: integrate Telethon search later
    return {"query": query, "results": []}


