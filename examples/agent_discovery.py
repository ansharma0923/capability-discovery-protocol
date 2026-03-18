"""Agent discovery example."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adp.intent.models import DiscoveryIntent, Category, Constraints, Preferences
from adp.registry.models import ProviderDescriptor, OfferingDescriptor, TrustLevel
from adp.registry.store import RegistryStore
from adp.service.discovery import run_discovery_pipeline


def setup_demo_registry() -> RegistryStore:
    store = RegistryStore()

    provider = ProviderDescriptor(
        provider_id="llm-prov-001",
        name="LLM Services Hub",
        description="Enterprise LLM inference and AI agent hosting",
        categories=["agent", "service"],
        regions=["us-east", "us-west", "eu-west"],
        trust_level=TrustLevel.VERIFIED,
        compliance_certifications=["SOC2"],
    )
    store.register_provider(provider)

    offerings = [
        OfferingDescriptor(
            offering_id="agent-off-001",
            provider_id="llm-prov-001",
            name="GPT-4 Turbo Inference",
            description="Enterprise GPT-4 Turbo inference API with 128K context",
            category="agent",
            tags=["llm", "gpt4", "inference", "nlp", "large-context"],
            price=0.01,
            price_unit="per-1k-tokens",
            region=["us-east", "us-west", "eu-west"],
            latency_ms=200,
            availability=0.997,
            compliance=["SOC2"],
            capabilities=["text-generation", "reasoning", "code", "128k-context"],
            active=True,
        ),
        OfferingDescriptor(
            offering_id="agent-off-002",
            provider_id="llm-prov-001",
            name="Fast LLM Inference",
            description="Low-latency LLM inference optimized for real-time applications",
            category="agent",
            tags=["llm", "inference", "low-latency", "real-time"],
            price=0.005,
            price_unit="per-1k-tokens",
            region=["us-east", "us-west"],
            latency_ms=50,
            availability=0.999,
            compliance=["SOC2"],
            capabilities=["text-generation", "low-latency"],
            active=True,
        ),
    ]
    for o in offerings:
        store.register_offering(o)
    return store


def main():
    store = setup_demo_registry()

    print("=== Agent Discovery Demo ===\n")

    intent = DiscoveryIntent(
        intent_text="I need a low-latency LLM inference API for real-time code generation",
        category=Category.AGENT,
        constraints=Constraints(max_latency_ms=300, region=["us-east"]),
        preferences=Preferences(max_results=5, ranking_profile="latency_optimized"),
    )

    print(f"Intent: {intent.intent_text}")
    print(f"Profile: {intent.preferences.ranking_profile}\n")

    result = run_discovery_pipeline(intent, store=store)

    print(f"Found {result['total_results']} results\n")
    for i, r in enumerate(result["results"], 1):
        print(f"{i}. Score: {r['total_score']:.4f} | {r['offering_id']}")
        print(f"   {r['explanation']['latency_fit']}")
        print()


if __name__ == "__main__":
    main()
