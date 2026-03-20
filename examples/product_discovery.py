"""Product discovery example."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adp.intent.models import Category, Constraints, DiscoveryIntent, Preferences
from adp.registry.models import OfferingDescriptor, ProviderDescriptor, TrustLevel
from adp.registry.store import RegistryStore
from adp.service.discovery import run_discovery_pipeline


def setup_demo_registry() -> RegistryStore:
    store = RegistryStore()
    provider = ProviderDescriptor(
        provider_id="demo-prov-001",
        name="ElectroMart",
        description="Premium consumer electronics",
        categories=["product"],
        regions=["us-east", "us-west"],
        trust_level=TrustLevel.CERTIFIED,
        availability_score=0.999,
    )
    store.register_provider(provider)

    offerings = [
        OfferingDescriptor(
            offering_id="demo-off-001",
            provider_id="demo-prov-001",
            name="ProANC Headphones X1",
            description="Premium noise-canceling over-ear headphones with 40-hour battery",
            category="product",
            tags=["headphones", "anc", "noise-canceling", "bluetooth", "premium"],
            price=249.99,
            region=["us-east", "us-west"],
            delivery_days=2,
            availability=0.99,
            capabilities=["anc", "bluetooth", "hi-fi"],
            active=True,
        ),
        OfferingDescriptor(
            offering_id="demo-off-002",
            provider_id="demo-prov-001",
            name="BudPro Wireless Earbuds",
            description="Compact noise-canceling earbuds, 8-hour battery, bluetooth",
            category="product",
            tags=["earbuds", "wireless", "anc", "bluetooth"],
            price=129.99,
            region=["us-east", "us-west"],
            delivery_days=3,
            availability=0.98,
            capabilities=["anc", "bluetooth"],
            active=True,
        ),
        OfferingDescriptor(
            offering_id="demo-off-003",
            provider_id="demo-prov-001",
            name="SmartHub 4K Display",
            description="4K OLED smart display, 32 inches, HDR10+",
            category="product",
            tags=["display", "4k", "oled", "smart"],
            price=599.99,
            region=["us-east", "us-west"],
            delivery_days=5,
            availability=0.97,
            capabilities=["4k", "oled"],
            active=True,
        ),
    ]
    for o in offerings:
        store.register_offering(o)
    return store


def main():
    store = setup_demo_registry()

    print("=== Product Discovery Demo ===\n")

    intent = DiscoveryIntent(
        intent_text="I need noise-canceling headphones under $300 for remote work",
        category=Category.PRODUCT,
        constraints=Constraints(max_price=300.0, region=["us-east"]),
        preferences=Preferences(max_results=5),
    )

    print(f"Intent: {intent.intent_text}")
    print(f"Category: {intent.category.value}")
    print(f"Constraints: max_price=${intent.constraints.max_price}, region={intent.constraints.region}\n")

    result = run_discovery_pipeline(intent, store=store)

    print(f"Found {result['total_results']} results from {result['total_candidates']} candidates")
    print(f"Pipeline: {len(result['pipeline']['stages_executed'])} stages in {result['pipeline']['duration_ms']}ms\n")

    for i, r in enumerate(result["results"], 1):
        print(f"{i}. Score: {r['total_score']:.4f} | Offering: {r['offering_id']}")
        print(f"   {r['explanation']['summary']}")
        if r["explanation"]["matched_constraints"]:
            print(f"   Matched: {', '.join(r['explanation']['matched_constraints'])}")
        print()


if __name__ == "__main__":
    main()
