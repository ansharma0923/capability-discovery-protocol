"""Service discovery example."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cdp.intent.models import Category, Constraints, DiscoveryIntent, Preferences
from cdp.registry.models import OfferingDescriptor, ProviderDescriptor, TrustLevel
from cdp.registry.store import RegistryStore
from cdp.service.discovery import run_discovery_pipeline


def setup_demo_registry() -> RegistryStore:
    store = RegistryStore()

    provider = ProviderDescriptor(
        provider_id="svc-prov-001",
        name="Enterprise Solutions Co",
        description="B2B enterprise software services",
        categories=["service", "api"],
        regions=["us-east", "eu-west"],
        trust_level=TrustLevel.CERTIFIED,
        compliance_certifications=["SOC2", "ISO27001", "HIPAA", "PCI-DSS"],
    )
    store.register_provider(provider)

    offerings = [
        OfferingDescriptor(
            offering_id="svc-off-001",
            provider_id="svc-prov-001",
            name="CRM Integration Service",
            description="Salesforce and HubSpot CRM integration with analytics",
            category="service",
            tags=["crm", "salesforce", "hubspot", "integration"],
            price=499.0,
            region=["us-east", "eu-west"],
            availability=0.999,
            compliance=["SOC2", "ISO27001"],
            capabilities=["crm-sync", "analytics", "webhooks"],
            active=True,
        ),
        OfferingDescriptor(
            offering_id="svc-off-002",
            provider_id="svc-prov-001",
            name="Payment Processing API",
            description="PCI-DSS compliant payment processing, multi-currency",
            category="service",
            tags=["payments", "pci-dss", "billing", "multi-currency"],
            price=0.25,
            price_unit="per-transaction",
            region=["us-east", "eu-west"],
            availability=0.9995,
            compliance=["PCI-DSS", "SOC2"],
            capabilities=["payments", "subscriptions", "refunds"],
            active=True,
        ),
    ]
    for o in offerings:
        store.register_offering(o)
    return store


def main():
    store = setup_demo_registry()

    print("=== Service Discovery Demo ===\n")

    intent = DiscoveryIntent(
        intent_text="I need a CRM integration service with SOC2 compliance",
        category=Category.SERVICE,
        constraints=Constraints(compliance=["SOC2"], region=["us-east"]),
        preferences=Preferences(max_results=5),
    )

    print(f"Intent: {intent.intent_text}")
    print(f"Required compliance: {intent.constraints.compliance}\n")

    result = run_discovery_pipeline(intent, store=store)

    print(f"Found {result['total_results']} results\n")
    for i, r in enumerate(result["results"], 1):
        print(f"{i}. Score: {r['total_score']:.4f} | {r['offering_id']}")
        print(f"   {r['explanation']['summary']}")
        print()


if __name__ == "__main__":
    main()
