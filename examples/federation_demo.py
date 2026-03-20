"""Federation demo example - local simulation of multi-node ADP federation."""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adp.federation.client import FederationClient, LocalFederationSimulator
from adp.intent.models import Category, Constraints, DiscoveryIntent, Preferences
from adp.registry.models import OfferingDescriptor, ProviderDescriptor, TrustLevel
from adp.registry.store import RegistryStore
from adp.service.discovery import run_discovery_pipeline


def build_node1_registry() -> tuple:
    """Build offerings and providers for simulated node-1 (US East cluster)."""
    provider = ProviderDescriptor(
        provider_id="fed-prov-node1-001",
        name="ANC Audio US",
        description="US-focused premium headphone and audio accessories",
        categories=["product"],
        regions=["us-east"],
        trust_level=TrustLevel.VERIFIED,
    )
    offerings = [
        OfferingDescriptor(
            offering_id="fed-off-node1-001",
            provider_id="fed-prov-node1-001",
            name="StudioPro ANC 500",
            description="Professional studio noise-canceling headphones, 50hr battery, Hi-Res audio",
            category="product",
            tags=["headphones", "anc", "noise-canceling", "studio", "hi-res"],
            price=279.99,
            currency="USD",
            region=["us-east"],
            delivery_days=2,
            availability=0.995,
            compliance=["CE", "FCC"],
            capabilities=["anc", "hi-res", "50hr-battery", "bluetooth"],
            active=True,
        ),
    ]
    return offerings, [provider]


def build_node2_registry() -> tuple:
    """Build offerings and providers for simulated node-2 (EU West cluster)."""
    provider = ProviderDescriptor(
        provider_id="fed-prov-node2-001",
        name="AudioTech Europe",
        description="EU-based audio and headphone distributor",
        categories=["product"],
        regions=["eu-west", "us-east"],
        trust_level=TrustLevel.BASIC,
    )
    offerings = [
        OfferingDescriptor(
            offering_id="fed-off-node2-001",
            provider_id="fed-prov-node2-001",
            name="ANC Headphones Lite",
            description="Lightweight noise-canceling headphones, 30hr battery, compact design",
            category="product",
            tags=["headphones", "anc", "noise-canceling", "lightweight", "bluetooth"],
            price=199.99,
            currency="USD",
            region=["eu-west", "us-east"],
            delivery_days=5,
            availability=0.99,
            compliance=["CE"],
            capabilities=["anc", "bluetooth", "30hr-battery"],
            active=True,
        ),
    ]
    return offerings, [provider]


def main():
    print("=== Federation Demo (Local Simulation) ===\n")

    # Local registry for this node
    local_store = RegistryStore()
    local_provider = ProviderDescriptor(
        provider_id="local-prov-001",
        name="ElectroMart Local",
        description="Local premium electronics retailer",
        categories=["product"],
        regions=["us-east", "us-west"],
        trust_level=TrustLevel.CERTIFIED,
    )
    local_store.register_provider(local_provider)
    local_store.register_offering(OfferingDescriptor(
        offering_id="local-off-001",
        provider_id="local-prov-001",
        name="ProANC Headphones X1",
        description="Premium noise-canceling over-ear headphones with 40-hour battery",
        category="product",
        tags=["headphones", "anc", "noise-canceling", "bluetooth", "premium"],
        price=249.99,
        currency="USD",
        region=["us-east", "us-west"],
        delivery_days=2,
        availability=0.99,
        capabilities=["anc", "bluetooth", "hi-fi"],
        active=True,
    ))

    # Build local federation simulators for 2 remote nodes
    node1_offerings, node1_providers = build_node1_registry()
    node2_offerings, node2_providers = build_node2_registry()

    sim_node1 = LocalFederationSimulator(
        "https://node1.adp.example.com", node1_offerings, node1_providers
    )
    sim_node2 = LocalFederationSimulator(
        "https://node2.adp.example.com", node2_offerings, node2_providers
    )

    client = FederationClient(nodes=["https://node1.adp.example.com", "https://node2.adp.example.com"])
    client.register_simulator(sim_node1)
    client.register_simulator(sim_node2)

    print(f"Configured {len(client.nodes)} federation nodes (local simulation):")
    for n in client.nodes:
        print(f"  - {n}")
    print()

    intent = DiscoveryIntent(
        intent_text="I need noise-canceling headphones under $300",
        category=Category.PRODUCT,
        constraints=Constraints(max_price=300.0, region=["us-east"]),
        preferences=Preferences(max_results=10, include_federation=True),
    )

    print(f"Intent: {intent.intent_text}")
    print(f"Constraints: max_price=${intent.constraints.max_price}, region={intent.constraints.region}\n")

    # Query remote nodes
    federated_results = asyncio.run(client.federate(intent))
    print(f"Results from remote nodes: {len(federated_results)}")
    for r in federated_results:
        print(f"  [{r.get('_node', 'unknown')}] {r['offering_id']} score={r['total_score']:.4f}")
    print()

    # Run full pipeline with federated results merged in
    response = run_discovery_pipeline(intent, store=local_store, federated_results=federated_results)

    print(f"Total results after merge+dedup+rerank: {response['total_results']}")
    print(f"Federation used: {response['pipeline']['federation_used']}")
    print(f"Pipeline duration: {response['pipeline']['duration_ms']}ms\n")

    print("Final ranked results:")
    for i, r in enumerate(response["results"], 1):
        source = r.get("_source", "local")
        print(f"  {i}. [{source:9s}] score={r['total_score']:.4f} | {r['offering_id']}")
        print(f"         {r['explanation']['summary']}")
    print()


if __name__ == "__main__":
    main()
