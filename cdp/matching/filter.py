"""Deterministic constraint-based filtering."""
from typing import List

from ..intent.models import DiscoveryIntent
from ..registry.models import OfferingDescriptor


def apply_filters(
    intent: DiscoveryIntent,
    offerings: List[OfferingDescriptor],
) -> List[OfferingDescriptor]:
    """Apply all constraint filters deterministically."""
    candidates = [o for o in offerings if o.active]

    c = intent.constraints

    # Category filter
    candidates = [o for o in candidates if o.category == intent.category.value]

    # Price filter
    if c.max_price is not None:
        candidates = [o for o in candidates if o.price is None or o.price <= c.max_price]

    # Region filter
    if c.region:
        candidates = [
            o for o in candidates
            if not o.region or any(r in o.region for r in c.region)
        ]

    # Latency filter
    if c.max_latency_ms is not None:
        candidates = [
            o for o in candidates
            if o.latency_ms is None or o.latency_ms <= c.max_latency_ms
        ]

    # Delivery days filter
    if c.delivery_days is not None:
        candidates = [
            o for o in candidates
            if o.delivery_days is None or o.delivery_days <= c.delivery_days
        ]

    # Compliance filter
    if c.compliance:
        candidates = [
            o for o in candidates
            if all(cert in o.compliance for cert in c.compliance)
        ]

    # Availability filter
    if c.availability_min is not None:
        candidates = [
            o for o in candidates
            if o.availability >= c.availability_min
        ]

    return candidates
