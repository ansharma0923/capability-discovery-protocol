"""Semantic matching engine."""
from typing import List, Tuple

from ..intent.models import DiscoveryIntent
from ..intent.parser import extract_keywords
from ..registry.models import OfferingDescriptor


def semantic_score(intent: DiscoveryIntent, offering: OfferingDescriptor) -> float:
    """Compute keyword-based semantic relevance score [0.0, 1.0]."""
    keywords = extract_keywords(intent)
    if not keywords:
        return 0.5

    text = " ".join([
        offering.name.lower(),
        offering.description.lower(),
        " ".join(t.lower() for t in offering.tags),
        " ".join(c.lower() for c in offering.capabilities),
    ])

    matches = sum(1 for kw in keywords if kw in text)
    score = min(matches / len(keywords), 1.0)
    return round(score, 4)


def rank_by_semantic(
    intent: DiscoveryIntent,
    offerings: List[OfferingDescriptor],
) -> List[Tuple[OfferingDescriptor, float]]:
    """Return offerings with semantic scores, sorted descending."""
    scored = [(o, semantic_score(intent, o)) for o in offerings]
    return sorted(scored, key=lambda x: x[1], reverse=True)
