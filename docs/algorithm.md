# Algorithm — Hybrid Recommender

We combine signals to score each candidate post for a user.

## 1) Content Embedding
- Build TF-IDF vectors from: `title + tags + topic.name + category.name`
- For a user, aggregate their interacted items to form a profile vector `u_vec` (weighted: like=3, inspire=4, rate=rating/20, view=1, bookmark=2).
- Score content similarity: `S_content = cos(u_vec, p_vec)`

## 2) Co-engagement (CF-lite)
- Compute item-item similarities from co-likes/co-views: `sim(i,j) = (# users who engaged both) / sqrt(freq(i)*freq(j))`
- For target user u, let `I_u` be items they engaged. `S_cf(p) = mean_j in I_u sim(p, j)`

## 3) Graph Signal
- User–Post bipartite graph. Post centrality proxy:
  - `deg_norm(p) = log(1 + views) + 2*log(1 + likes) + 3*log(1 + rating_count)`
  - Normalize to [0,1]. This is a cheap PageRank-ish heuristic.

## 4) Cold Start
- If user has little/no data:
  - Use mood/project priors (mapping in `feature_store.py`).
  - Rank by `GlobalScore = 0.4*Freshness + 0.4*Engagement + 0.2*EditorPick`

## 5) Business Rules & Filters
- Exclude `is_locked=true`
- If `is_available_in_public_feed=false` → push down unless explicitly followed
- Respect `project_code` filter if provided

## 6) Final Score
For known user:
```
score = 0.45*S_content + 0.35*S_cf + 0.15*deg_norm + 0.05*freshness
score -= exit_penalty
```
Where `exit_penalty = min(0.2, exit_count / (view_count+1e-6)) * 0.1`

## 7) Diversity (MMR)
- After sorting by `score`, re-rank with Maximal Marginal Relevance using cosine similarity of content vectors.
- `lambda=0.7` keeps relevance while improving diversity.

## 8) Pagination & Cache
- Cache per-user page for 60–120s (memory/redis)
- Stable pagination via post `slug`/`id` order-key

Implementation details are in `app/services/recommender.py` and helpers.
