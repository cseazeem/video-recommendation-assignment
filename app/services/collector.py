import httpx
from typing import Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings

HEADERS = {"Flic-Token": settings.FLIC_TOKEN}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
async def fetch(endpoint: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    url = f"{settings.API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, headers=HEADERS, params=params or {})
        r.raise_for_status()
        return r.json()

async def get_viewed_posts(page=1, page_size=1000, resonance_algorithm: str | None = None):
    params = {"page": page, "page_size": page_size}
    if resonance_algorithm:
        params["resonance_algorithm"] = resonance_algorithm
    return await fetch("posts/view", params)

async def get_liked_posts(page=1, page_size=1000, resonance_algorithm: str | None = None):
    params = {"page": page, "page_size": page_size}
    if resonance_algorithm:
        params["resonance_algorithm"] = resonance_algorithm
    return await fetch("posts/like", params)

async def get_inspired_posts(page=1, page_size=1000, resonance_algorithm: str | None = None):
    params = {"page": page, "page_size": page_size}
    if resonance_algorithm:
        params["resonance_algorithm"] = resonance_algorithm
    return await fetch("posts/inspire", params)

async def get_rated_posts(page=1, page_size=1000, resonance_algorithm: str | None = None):
    params = {"page": page, "page_size": page_size}
    if resonance_algorithm:
        params["resonance_algorithm"] = resonance_algorithm
    return await fetch("posts/rating", params)

async def get_all_posts(page=1, page_size=1000):
    params = {"page": page, "page_size": page_size}
    return await fetch("posts/summary/get", params)

async def get_all_users(page=1, page_size=1000):
    params = {"page": page, "page_size": page_size}
    return await fetch("users/get_all", params)
