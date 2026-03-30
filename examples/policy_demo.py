"""Policy engine demo example."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Tuple

from cdp.policy.engine import ActiveOnlyPolicy, PolicyEngine, PolicyRule, VerifiedProviderPolicy
from cdp.registry.models import OfferingDescriptor, ProviderDescriptor, TrustLevel


class SOC2RequiredPolicy(PolicyRule):
    """Custom policy: all offerings must have SOC2 compliance."""
    name = "soc2_required"

    def apply(self, offering, provider) -> Tuple[bool, str]:
        if "SOC2" not in offering.compliance:
            return False, f"Offering '{offering.name}' missing SOC2 compliance"
        return True, "SOC2 compliance verified"


def main():
    print("=== Policy Engine Demo ===\n")

    provider_certified = ProviderDescriptor(
        provider_id="prov-cert",
        name="Certified Provider",
        description="Fully certified provider",
        categories=["service"],
        regions=["us-east"],
        trust_level=TrustLevel.CERTIFIED,
    )
    provider_unverified = ProviderDescriptor(
        provider_id="prov-unverified",
        name="Unverified Provider",
        description="New provider, not yet verified",
        categories=["service"],
        regions=["us-east"],
        trust_level=TrustLevel.UNVERIFIED,
    )

    offering_active_soc2 = OfferingDescriptor(
        offering_id="off-active-soc2",
        provider_id="prov-cert",
        name="Active SOC2 Service",
        description="Active service with SOC2",
        category="service",
        compliance=["SOC2", "ISO27001"],
        active=True,
    )
    offering_inactive = OfferingDescriptor(
        offering_id="off-inactive",
        provider_id="prov-cert",
        name="Inactive Service",
        description="Decommissioned service",
        category="service",
        compliance=["SOC2"],
        active=False,
    )
    offering_no_soc2 = OfferingDescriptor(
        offering_id="off-no-soc2",
        provider_id="prov-cert",
        name="Service without SOC2",
        description="Service without SOC2 compliance",
        category="service",
        compliance=["ISO9001"],
        active=True,
    )

    providers = {
        "prov-cert": provider_certified,
        "prov-unverified": provider_unverified,
    }
    offerings = [offering_active_soc2, offering_inactive, offering_no_soc2]

    # Default policy engine
    print("--- Default Policy Engine ---")
    engine = PolicyEngine()
    allowed = engine.filter(offerings, providers)
    print(f"Allowed: {len(allowed)}/{len(offerings)} offerings")
    for o, reasons in allowed:
        print(f"  ✓ {o.offering_id}: {reasons[-1]}")
    print()

    # Custom policy with SOC2 requirement
    print("--- Custom Policy (SOC2 Required) ---")
    engine2 = PolicyEngine(rules=[ActiveOnlyPolicy(), VerifiedProviderPolicy(), SOC2RequiredPolicy()])
    allowed2 = engine2.filter(offerings, providers)
    print(f"Allowed: {len(allowed2)}/{len(offerings)} offerings")
    for o, reasons in allowed2:
        print(f"  ✓ {o.offering_id}")
    print()


if __name__ == "__main__":
    main()
