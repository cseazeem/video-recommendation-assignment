import numpy as np

def mmr_rerank(candidates, embeddings, lam=0.7, top_k=50):
    # candidates: list of (post, score)
    # embeddings: dict post_id -> vector
    if not candidates:
        return []

    selected = []
    remaining = candidates[:]
    # sort by score desc
    remaining.sort(key=lambda x: x[1], reverse=True)

    while remaining and len(selected) < min(top_k, len(candidates)):
        if not selected:
            selected.append(remaining.pop(0))
            continue
        best = None
        best_val = -1e9
        for idx, (p, s) in enumerate(remaining):
            rel = s
            div = 0.0
            if embeddings and selected:
                # cosine with the most similar already selected item
                vec_p = embeddings.get(p["id"])
                if vec_p is not None:
                    max_sim = 0.0
                    for (q, _) in selected:
                        vec_q = embeddings.get(q["id"])
                        if vec_q is None:
                            continue
                        denom = (np.linalg.norm(vec_p) * np.linalg.norm(vec_q) + 1e-9)
                        sim = float(np.dot(vec_p, vec_q)) / denom
                        if sim > max_sim:
                            max_sim = sim
                    div = max_sim
            mmr = lam * rel - (1 - lam) * div
            if mmr > best_val:
                best_val = mmr
                best = idx
        selected.append(remaining.pop(best))
    return selected
