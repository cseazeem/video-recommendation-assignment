from __future__ import annotations
from typing import Dict, List

# Example mapping. Extend as needed.
MOOD_TO_PROJECT_PRIORS: Dict[str, List[str]] = {
    "stressed": ["mindfulness", "calm", "gratitude"],
    "low_motivation": ["career", "discipline", "fitness"],
    "confused": ["career", "learning", "productivity"],
    "general": ["flic", "motivation", "growth"]
}
