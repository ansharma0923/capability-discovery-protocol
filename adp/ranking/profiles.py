"""Ranking weight profiles."""
from dataclasses import dataclass
from typing import Dict


@dataclass
class RankingWeights:
    relevance: float = 0.30
    price: float = 0.20
    latency: float = 0.15
    availability: float = 0.15
    trust: float = 0.15
    freshness: float = 0.05


PROFILES: Dict[str, RankingWeights] = {
    "default": RankingWeights(),
    "cost_optimized": RankingWeights(
        relevance=0.20, price=0.40, latency=0.10,
        availability=0.10, trust=0.10, freshness=0.10,
    ),
    "latency_optimized": RankingWeights(
        relevance=0.20, price=0.10, latency=0.40,
        availability=0.15, trust=0.10, freshness=0.05,
    ),
    "trust_optimized": RankingWeights(
        relevance=0.25, price=0.10, latency=0.10,
        availability=0.15, trust=0.35, freshness=0.05,
    ),
}


def get_profile(profile_name: str) -> RankingWeights:
    return PROFILES.get(profile_name, PROFILES["default"])
