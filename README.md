# Video Recommendation Assignment — FastAPI

A production-grade, **hybrid** video recommendation backend for the assignment. It includes:
- Personalized feed (`/feed?username=...`)
- Category feed (`/feed?username=...&project_code=...`)
- Data collection jobs from Socialverse APIs (views, likes, inspires, ratings, posts, users)
- Hybrid ranking: content similarity + lightweight collaborative filtering + graph signals + business rules
- Cold-start via **mood → topic/category** mapping
- Caching, pagination, alembic migrations, Postman collection, and docs

> Ref apps: Empowerverse (Android/iOS).

## Quickstart

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Fill API_BASE_URL & FLIC_TOKEN in .env

alembic upgrade head
uvicorn app.main:app --reload
```

## Endpoints

- `GET /feed?username={username}` — personalized
- `GET /feed?username={username}&project_code={project_code}` — category/project filtered

Open API docs at `/docs`.

## Collect Data (Internal tasks)
Run the collector functions (see `app/services/collector.py`) to hydrate the DB from Socialverse APIs using `FLIC_TOKEN`.

## How the Recommender Works
See `docs/algorithm.md` for the detailed math and ranking formula. TL;DR:
- **Content-based**: TF-IDF embeddings from `title + tags + topic + category`
- **CF-lite**: item-item similarity via co-engagement (likes/views/ratings)
- **Graph**: bipartite user–post graph with degree-normalized signals
- **Cold-start**: mood/project_code priors + global engagement score
- **Re-rank**: MMR diversity + freshness + business rules (ban locked, prefer public)

## Submission
- Include this repo
- Export Postman collection in `/postman/VideoRecommendation.postman_collection.json`
- Record 30–40s intro + 3–5 min Postman demo
- Add details in `docs/`

