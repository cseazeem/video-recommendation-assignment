# Demo Script (3–5 minutes)

1. **Intro (10s)**: Name, goal: "Hybrid recommender with FastAPI for personalized motivational videos."
2. **Run server**: `uvicorn app.main:app --reload`
3. **Swagger**: Open `/docs` and show `/feed` with `username` only.
4. **Postman**: Hit `/feed?username=alice` and `/feed?username=alice&project_code=flic`
5. **Explain** short: signals (content, CF-lite, graph, cold-start), caching, pagination.
6. **Error handling**: Try an unknown user → graceful cold-start.
7. **Close**: Mention extensibility to deep embeddings (SBERT) and online-learning.
