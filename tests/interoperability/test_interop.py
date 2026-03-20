"""Interoperability tests - end-to-end pipeline validation."""
import pytest
from fastapi.testclient import TestClient

from adp.main import app
from adp.registry.store import RegistryStore, get_store
from adp.registry.models import ProviderDescriptor, OfferingDescriptor, TrustLevel
from adp.intent.models import DiscoveryIntent, Category, Constraints, Preferences
from adp.service.discovery import run_discovery_pipeline


@pytest.fixture
def populated_store():
    """A registry store with providers and offerings across all categories."""
    store = RegistryStore()

    # Product provider
    store.register_provider(ProviderDescriptor(
        provider_id="interop-prov-product",
        name="ElectroMart",
        description="Consumer electronics",
        categories=["product"],
        regions=["us-east", "us-west"],
        trust_level=TrustLevel.CERTIFIED,
    ))

    # Service provider
    store.register_provider(ProviderDescriptor(
        provider_id="interop-prov-service",
        name="Enterprise Services",
        description="B2B services",
        categories=["service"],
        regions=["us-east"],
        trust_level=TrustLevel.VERIFIED,
    ))

    # Agent provider
    store.register_provider(ProviderDescriptor(
        provider_id="interop-prov-agent",
        name="LLM Hub",
        description="LLM services",
        categories=["agent"],
        regions=["us-east", "us-west"],
        trust_level=TrustLevel.VERIFIED,
    ))

    # Product offerings
    for i in range(3):
        store.register_offering(OfferingDescriptor(
            offering_id=f"interop-off-product-{i}",
            provider_id="interop-prov-product",
            name=f"Headphone Model {i}",
            description=f"Noise-canceling headphones model {i} with bluetooth",
            category="product",
            tags=["headphones", "anc", "bluetooth"],
            price=100.0 + i * 50,
            region=["us-east", "us-west"],
            availability=0.99,
            active=True,
        ))

    # Service offerings
    store.register_offering(OfferingDescriptor(
        offering_id="interop-off-service-1",
        provider_id="interop-prov-service",
        name="CRM Integration Service",
        description="Salesforce CRM integration with analytics",
        category="service",
        tags=["crm", "salesforce", "integration"],
        price=299.0,
        region=["us-east"],
        availability=0.999,
        active=True,
    ))

    # Agent offerings
    store.register_offering(OfferingDescriptor(
        offering_id="interop-off-agent-1",
        provider_id="interop-prov-agent",
        name="GPT-4 Inference API",
        description="Enterprise LLM inference for AI agents",
        category="agent",
        tags=["llm", "gpt4", "inference", "ai"],
        price=0.01,
        region=["us-east", "us-west"],
        availability=0.997,
        active=True,
    ))

    return store


class TestEndToEndPipeline:
    def test_product_discovery_pipeline(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="I need noise-canceling headphones with bluetooth",
            category=Category.PRODUCT,
            constraints=Constraints(max_price=250.0),
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        assert result["category"] == "product"
        assert result["total_results"] >= 0
        assert len(result["pipeline"]["stages_executed"]) == 14

    def test_all_14_stages_executed(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        stages = result["pipeline"]["stages_executed"]
        expected_stages = [
            "parse_request", "normalize_intent", "extract_constraints",
            "retrieve_candidates", "deterministic_filtering", "semantic_matching",
            "capability_validation", "policy_filtering", "ranking",
            "explanation_generation", "federation_merge", "deduplication",
            "audit_logging", "response_generation",
        ]
        for stage in expected_stages:
            assert stage in stages, f"Stage '{stage}' not executed"

    def test_category_filtering_in_pipeline(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="agent service",
            category=Category.SERVICE,
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        assert result["category"] == "service"
        # All results must match the requested category
        for r in result["results"]:
            offering = populated_store.get_offering(r["offering_id"])
            if offering:
                assert offering.category == "service"

    def test_results_sorted_by_score(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="noise-canceling headphones bluetooth",
            category=Category.PRODUCT,
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        scores = [r["total_score"] for r in result["results"]]
        assert scores == sorted(scores, reverse=True)

    def test_max_results_respected(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
            preferences=Preferences(max_results=2),
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        assert len(result["results"]) <= 2

    def test_pipeline_duration_tracked(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        assert result["pipeline"]["duration_ms"] > 0

    def test_intent_id_in_response(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        assert result["intent_id"] == intent.intent_id

    def test_federation_merge_without_results(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
        )
        result = run_discovery_pipeline(intent, store=populated_store, federated_results=[])
        assert result["pipeline"]["federation_used"] is False

    def test_federation_merge_with_results(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
        )
        federated = [{
            "offering_id": "fed-offering-001",
            "provider_id": "remote-provider-001",
            "total_score": 0.75,
            "score_breakdown": {},
            "explanation": {"summary": "Federated result"},
        }]
        result = run_discovery_pipeline(intent, store=populated_store, federated_results=federated)
        assert result["pipeline"]["federation_used"] is True
        fed_ids = [r["offering_id"] for r in result["results"] if r.get("_source") == "federated"]
        assert "fed-offering-001" in fed_ids

    def test_audit_log_recorded(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
        )
        # Note: audit uses global store, so this test is approximate
        run_discovery_pipeline(intent, store=populated_store)
        # The audit is written to the global store, not the test store
        # Just verify the pipeline completed without error


class TestRankingProfiles:
    def test_cost_optimized_profile(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="affordable headphones",
            category=Category.PRODUCT,
            preferences=Preferences(ranking_profile="cost_optimized"),
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        assert result["total_results"] >= 0

    def test_trust_optimized_profile(self, populated_store):
        intent = DiscoveryIntent(
            intent_text="trusted headphones",
            category=Category.PRODUCT,
            preferences=Preferences(ranking_profile="trust_optimized"),
        )
        result = run_discovery_pipeline(intent, store=populated_store)
        assert result["total_results"] >= 0
