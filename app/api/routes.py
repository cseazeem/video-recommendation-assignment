from fastapi import APIRouter, Query, Header
from typing import Optional
from app.schemas.feed import FeedResponse
from app.services.recommender import get_recommendations

router = APIRouter()

@router.get("/feed", response_model=FeedResponse, tags=["feed"])
async def feed(
    username: str = Query(..., description="Username for personalization"),
    project_code: Optional[str] = Query(None, description="Filter by project/topic code"),
    flic_token: Optional[str] = Header(default=None, alias="Flic-Token")
):
    # Flic-Token is accepted for parity with external calls; internal logic may not require it
    resp = await get_recommendations(username=username, project_code=project_code)
    return resp
