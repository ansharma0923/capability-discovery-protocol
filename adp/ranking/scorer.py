"""Weighted ranking scorer with explanation."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..intent.models import DiscoveryIntent
from ..registry.models import OfferingDescriptor, ProviderDescriptor, TrustLevel
from .profiles import RankingWeights, get_profile

TRUST_SCORES = {
    TrustLevel.UNVERIFIED: 0.1,
    TrustLevel.BASIC: 0.4,
    TrustLevel.VERIFIED: 0.75,
    TrustLevel.CERTIFIED: 1.0,
}


def score_offering(
    intent: DiscoveryIntent,
    offering: OfferingDescriptor,
    provider: Optional[ProviderDescriptor],
    semantic_score: float,
    weights: RankingWeights,
) -> Dict[str, Any]:
    """Compute weighted score with explanation."""
    relevance = semantic_score

    # Price score: 1.0 if free or within budget, decreasing otherwise
    price_score = 1.0
    price_fit = "No price constraint"
    if offering.price is not None:
        max_p = intent.constraints.max_price
        if max_p is not None and max_p > 0:
            price_score = max(0.0, 1.0 - (offering.price / max_p))
            price_fit = f"Price ${offering.price} vs budget ${max_p}"
        else:
            price_score = max(0.0, 1.0 - (offering.price / 1000.0))
            price_fit = f"Price ${offering.price} (no budget constraint)"

    # Latency score
    latency_score = 1.0
    latency_fit = "No latency constraint"
    if offering.latency_ms is not None:
        max_l = intent.constraints.max_latency_ms
        if max_l is not None and max_l > 0:
            latency_score = max(0.0, 1.0 - (offering.latency_ms / max_l))
            latency_fit = f"Latency {offering.latency_ms}ms vs max {max_l}ms"
        else:
            latency_score = max(0.0, 1.0 - (offering.latency_ms / 5000.0))
            latency_fit = f"Latency {offering.latency_ms}ms"

    # Availability score
    availability_score = offering.availability

    # Trust score
    trust_score = 0.5
    trust_reason = "Unknown trust level"
    if provider:
        trust_score = TRUST_SCORES.get(provider.trust_level, 0.4)
        trust_reason = f"Provider trust level: {provider.trust_level.value}"

    # Freshness score (based on how recently updated)
    freshness_score = 1.0
    updated = offering.updated_at
    if updated.tzinfo is None:
        from datetime import timezone as _tz
        updated = updated.replace(tzinfo=_tz.utc)
    age_hours = (datetime.now(timezone.utc) - updated).total_seconds() / 3600
    if age_hours > 1:
        freshness_score = max(0.3, 1.0 - (age_hours / (offering.ttl_seconds / 3600)))

    # Weighted total
    total_score = (
        weights.relevance * relevance
        + weights.price * price_score
        + weights.latency * latency_score
        + weights.availability * availability_score
        + weights.trust * trust_score
        + weights.freshness * freshness_score
    )
    total_score = round(min(1.0, max(0.0, total_score)), 4)

    matched_constraints = []
    if intent.constraints.max_price is not None and offering.price is not None:
        if offering.price <= intent.constraints.max_price:
            matched_constraints.append(f"price <= ${intent.constraints.max_price}")
    if intent.constraints.region and offering.region:
        if any(r in offering.region for r in intent.constraints.region):
            matched_constraints.append(f"region in {intent.constraints.region}")
    if intent.constraints.compliance and offering.compliance:
        matched = [c for c in intent.constraints.compliance if c in offering.compliance]
        if matched:
            matched_constraints.append(f"compliance: {matched}")

    summary = (
        f"Offering '{offering.name}' scored {total_score:.2f} for intent "
        f"'{intent.intent_text[:60]}...'"
        if len(intent.intent_text) > 60
        else f"Offering '{offering.name}' scored {total_score:.2f}"
    )

    return {
        "offering_id": offering.offering_id,
        "provider_id": offering.provider_id,
        "total_score": total_score,
        "score_breakdown": {
            "relevance": round(relevance * weights.relevance, 4),
            "price": round(price_score * weights.price, 4),
            "latency": round(latency_score * weights.latency, 4),
            "availability": round(availability_score * weights.availability, 4),
            "trust": round(trust_score * weights.trust, 4),
            "freshness": round(freshness_score * weights.freshness, 4),
        },
        "explanation": {
            "matched_constraints": matched_constraints,
            "relevance_reason": f"Semantic match score: {relevance:.2f}",
            "price_fit": price_fit,
            "latency_fit": latency_fit,
            "trust_reason": trust_reason,
            "summary": summary,
        },
    }


def rank_candidates(
    intent: DiscoveryIntent,
    scored_offerings: List[Tuple[OfferingDescriptor, float]],
    providers: Dict[str, ProviderDescriptor],
) -> List[Dict[str, Any]]:
    """Rank candidates using weighted scoring and return sorted results."""
    weights = get_profile(intent.preferences.ranking_profile.value)
    results = []

    for offering, sem_score in scored_offerings:
        provider = providers.get(offering.provider_id)
        result = score_offering(intent, offering, provider, sem_score, weights)
        results.append(result)

    return sorted(results, key=lambda x: x["total_score"], reverse=True)
