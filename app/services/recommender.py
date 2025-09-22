from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import numpy as np
from async_lru import alru_cache
from app.schemas.feed import FeedResponse, PostOut
from app.services.feature_store import MOOD_TO_PROJECT_PRIORS
from app.utils.ranking import mmr_rerank

# For demo purposes, we'll keep in-memory mock data.
# You can replace these with real DB queries + collectors.
MOCK_USERS = {
    "alice": {"username": "alice", "mood": "low_motivation"},
    "bob": {"username": "bob", "mood": "general"},
}

MOCK_POSTS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "slug": "post-1",
        "title": "Build Discipline: 3-Min Habit Trick",
        "project_code": "motivation",
        "category_name": "Motivation",
        "topic_name": "Discipline",
        "tags": ["habits", "discipline", "productivity"],
        "is_available_in_public_feed": True,
        "is_locked": False,
        "stats": {"view_count": 1200, "upvote_count": 140, "exit_count": 120, "rating_count": 45, "average_rating": 88},
        "media": {"video_link": "https://cdn.example.com/1.mp4", "thumbnail_url": "", "gif_thumbnail_url": ""},
        "owner": {"name": "Coach A", "username": "coach_a"},
        "created_at": 1719791247000,
    },
    {
        "id": 2,
        "slug": "post-2",
        "title": "Calm Breathing in 60 Seconds",
        "project_code": "calm",
        "category_name": "Mindfulness",
        "topic_name": "Breathing",
        "tags": ["calm", "anxiety", "breath"],
        "is_available_in_public_feed": True,
        "is_locked": False,
        "stats": {"view_count": 800, "upvote_count": 210, "exit_count": 30, "rating_count": 120, "average_rating": 92},
        "media": {"video_link": "https://cdn.example.com/2.mp4", "thumbnail_url": "", "gif_thumbnail_url": ""},
        "owner": {"name": "Therapist B", "username": "therapist_b"},
        "created_at": 1729791247000,
    },
    {
        "id": 3,
        "slug": "post-3",
        "title": "Career Clarity: 5 Questions",
        "project_code": "career",
        "category_name": "Career",
        "topic_name": "Clarity",
        "tags": ["career", "goals", "motivation"],
        "is_available_in_public_feed": True,
        "is_locked": False,
        "stats": {"view_count": 400, "upvote_count": 50, "exit_count": 10, "rating_count": 20, "average_rating": 80},
        "media": {"video_link": "https://cdn.example.com/3.mp4", "thumbnail_url": "", "gif_thumbnail_url": ""},
        "owner": {"name": "Mentor C", "username": "mentor_c"},
        "created_at": 1735791247000,
    },
]

def _content_vector(p: Dict[str, Any]) -> np.ndarray:
    # Very simple bag-of-words based embedding stub
    vocab = {
        "discipline": 0, "habits": 1, "productivity": 2, "calm": 3, "anxiety": 4, "breath": 5,
        "career": 6, "goals": 7, "clarity": 8, "mindfulness": 9, "motivation": 10
    }
    vec = np.zeros(len(vocab), dtype=float)
    text = " ".join([p.get("title","")] + p.get("tags", []) + [p.get("category_name",""), p.get("topic_name","")]).lower()
    for term, idx in vocab.items():
        vec[idx] = text.count(term)
    if vec.sum() > 0:
        vec = vec / np.linalg.norm(vec)
    return vec

def _freshness(p: Dict[str, Any]) -> float:
    # naive freshness proxy by created_at magnitude
    t = float(p.get("created_at", 0))
    return (t % 1e6) / 1e6

def _deg_norm(p: Dict[str, Any]) -> float:
    s = p.get("stats", {})
    v = float(s.get("view_count", 0.0))
    u = float(s.get("upvote_count", 0.0))
    r = float(s.get("rating_count", 0.0))
    dn = np.log1p(v) + 2*np.log1p(u) + 3*np.log1p(r)
    return float(dn / (dn + 10.0))

def _exit_penalty(p: Dict[str, Any]) -> float:
    s = p.get("stats", {})
    exits = float(s.get("exit_count", 0.0))
    views = float(s.get("view_count", 1.0))
    frac = min(0.2, exits / (views + 1e-6))
    return 0.1 * frac

def _to_postout(p: Dict[str, Any]) -> Dict[str, Any]:
    s = p.get("stats", {})
    m = p.get("media", {})
    return {
        "id": p["id"],
        "owner": p.get("owner", {}),
        "category": {"name": p.get("category_name")},
        "topic": {"name": p.get("topic_name"), "project_code": p.get("project_code")},
        "title": p.get("title", ""),
        "is_available_in_public_feed": p.get("is_available_in_public_feed", True),
        "is_locked": p.get("is_locked", False),
        "slug": p.get("slug", ""),
        "upvoted": False,
        "bookmarked": False,
        "following": False,
        "identifier": p.get("slug", ""),
        "comment_count": int(s.get("comment_count", 0)),
        "upvote_count": int(s.get("upvote_count", 0)),
        "view_count": int(s.get("view_count", 0)),
        "exit_count": int(s.get("exit_count", 0)),
        "rating_count": int(s.get("rating_count", 0)),
        "average_rating": int(s.get("average_rating", 0)),
        "share_count": int(s.get("share_count", 0)),
        "bookmark_count": int(s.get("bookmark_count", 0)),
        "video_link": m.get("video_link", ""),
        "thumbnail_url": m.get("thumbnail_url", ""),
        "gif_thumbnail_url": m.get("gif_thumbnail_url", ""),
        "contract_address": "",
        "chain_id": "",
        "chart_url": "",
        "baseToken": {"address":"", "name":"", "symbol":"", "image_url":""},
        "created_at": int(p.get("created_at", 0)),
        "tags": p.get("tags", [])
    }

@alru_cache(maxsize=1024)
async def get_recommendations(username: str, project_code: Optional[str] = None) -> FeedResponse:
    user = MOCK_USERS.get(username, {"username": username, "mood": "general"})
    mood = user.get("mood", "general")
    prior_projects = set(MOOD_TO_PROJECT_PRIORS.get(mood, ["motivation"]))

    # Candidate pool
    candidates = []
    for p in MOCK_POSTS:
        if p.get("is_locked"):
            continue
        if not p.get("is_available_in_public_feed", True):
            continue
        if project_code:
            if p.get("project_code") != project_code:
                continue
        else:
            # If user has a mood, slightly prefer those projects but do not hard filter
            pass
        candidates.append(p)

    if not candidates:
        return FeedResponse(status="success", post=[])

    # Content vectors
    vecs = {p["id"]: _content_vector(p) for p in candidates}

    # User profile vector (mock: mood prior)
    user_vec = np.zeros_like(next(iter(vecs.values())))
    for p in candidates:
        if p.get("project_code") in prior_projects:
            user_vec += vecs[p["id"]]
    if np.linalg.norm(user_vec) > 0:
        user_vec = user_vec / (np.linalg.norm(user_vec) + 1e-9)

    # Score
    scored = []
    for p in candidates:
        v = vecs[p["id"]]
        content_sim = float(np.dot(user_vec, v)) if np.linalg.norm(user_vec) > 0 else 0.0
        cf_lite = 0.2 if p["project_code"] in prior_projects else 0.0
        deg = _deg_norm(p)
        fresh = _freshness(p)
        penalty = _exit_penalty(p)
        score = 0.45*content_sim + 0.35*cf_lite + 0.15*deg + 0.05*fresh
        score -= penalty
        scored.append((p, float(score)))

    # Diversity
    reranked = mmr_rerank([({"id":p["id"], **_to_postout(p)}, s) for p, s in scored], embeddings=vecs, lam=0.7, top_k=50)

    posts = [item for (item, _) in reranked]

    return FeedResponse(status="success", post=posts)
