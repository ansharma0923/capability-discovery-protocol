"""Capability validation - ensures provider can fulfill the intent."""
from typing import Optional, Tuple

from ..intent.models import DiscoveryIntent
from ..registry.models import OfferingDescriptor, ProviderDescriptor


def validate_capability(
    intent: DiscoveryIntent,
    offering: OfferingDescriptor,
    provider: Optional[ProviderDescriptor],
) -> Tuple[bool, str]:
    """Validate that the offering can fulfill the intent."""
    if not offering.active:
        return False, "Offering is not active"

    if provider is None:
        return False, "Provider not found"

    if intent.category.value not in provider.categories:
        return False, f"Provider does not support category '{intent.category.value}'"

    if intent.constraints.region and provider.regions:
        if not any(r in provider.regions for r in intent.constraints.region):
            return False, "Provider does not operate in requested regions"

    return True, "Capability validated"
