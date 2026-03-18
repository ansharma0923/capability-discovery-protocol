"""Policy engine for enforcing discovery policies."""
from typing import List, Dict, Any, Optional, Tuple
from ..registry.models import OfferingDescriptor, ProviderDescriptor


class PolicyRule:
    """Base class for policy rules."""

    name: str = "base_rule"

    def apply(
        self,
        offering: OfferingDescriptor,
        provider: Optional[ProviderDescriptor],
    ) -> Tuple[bool, str]:
        """Returns (allowed, reason)."""
        return True, "No policy"


class ActiveOnlyPolicy(PolicyRule):
    name = "active_only"

    def apply(
        self,
        offering: OfferingDescriptor,
        provider: Optional[ProviderDescriptor],
    ) -> Tuple[bool, str]:
        if not offering.active:
            return False, "Offering is not active"
        return True, "Offering is active"


class VerifiedProviderPolicy(PolicyRule):
    name = "verified_provider"

    def apply(
        self,
        offering: OfferingDescriptor,
        provider: Optional[ProviderDescriptor],
    ) -> Tuple[bool, str]:
        if provider is None:
            return False, "Provider not found"
        from ..registry.models import TrustLevel

        allowed_levels = [TrustLevel.BASIC, TrustLevel.VERIFIED, TrustLevel.CERTIFIED]
        if provider.trust_level not in allowed_levels:
            return False, f"Provider trust level '{provider.trust_level.value}' not sufficient"
        return True, f"Provider trust level '{provider.trust_level.value}' is acceptable"


class PolicyEngine:
    def __init__(self, rules: Optional[List[PolicyRule]] = None):
        self.rules = rules or [ActiveOnlyPolicy(), VerifiedProviderPolicy()]

    def filter(
        self,
        offerings: List[OfferingDescriptor],
        providers: Dict[str, ProviderDescriptor],
    ) -> List[Tuple[OfferingDescriptor, List[str]]]:
        """Filter offerings through all policy rules."""
        allowed = []
        for offering in offerings:
            provider = providers.get(offering.provider_id)
            all_passed = True
            reasons: List[str] = []
            for rule in self.rules:
                passed, reason = rule.apply(offering, provider)
                if not passed:
                    all_passed = False
                    reasons.append(f"BLOCKED by {rule.name}: {reason}")
                    break
                reasons.append(f"PASSED {rule.name}: {reason}")
            if all_passed:
                allowed.append((offering, reasons))
        return allowed


_engine = PolicyEngine()


def get_policy_engine() -> PolicyEngine:
    return _engine
