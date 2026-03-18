"""Functional tests for the /discover endpoint."""
import pytest
from fastapi.testclient import TestClient
from adp.main import app
from adp.registry.store import get_store
from adp.registry.models import ProviderDescriptor, OfferingDescriptor, TrustLevel


@pytest.fixture(autouse=True)
def setup_registry():
    """Populate the global store with test data before each test."""
    store = get_store()
    # Clear existing data by creating a temporary store view
    # Register test providers
    provider = ProviderDescriptor(
        provider_id="test-prov-disc-001",
        name="Test Electronics",
        description="Test electronics provider",
        categories=["product"],
        regions=["us-east", "us-west"],
        trust_level=TrustLevel.CERTIFIED,
        availability_score=0.999,
    )
    store.register_provider(provider)

    offering = OfferingDescriptor(
        offering_id="test-off-disc-001",
        provider_id="test-prov-disc-001",
        name="Premium Noise Canceling Headphones",
        description="High quality noise canceling headphones with bluetooth",
        category="product",
        tags=["headphones", "noise-canceling", "bluetooth", "premium"],
        price=249.99,
        region=["us-east", "us-west"],
        delivery_days=2,
        availability=0.99,
        compliance=["CE", "FCC"],
        capabilities=["anc", "bluetooth"],
        active=True,
    )
    store.register_offering(offering)
    yield
    # No teardown needed - tests use fresh client per test


@pytest.fixture
def client():
    return TestClient(app)


class TestDiscoverEndpoint:
    def test_discover_returns_200(self, client):
        response = client.post("/discover", json={
            "intent_text": "I need noise-canceling headphones",
            "category": "product",
        })
        assert response.status_code == 200

    def test_discover_response_structure(self, client):
        response = client.post("/discover", json={
            "intent_text": "I need noise-canceling headphones for remote work",
            "category": "product",
        })
        data = response.json()
        assert "intent_id" in data
        assert "version" in data
        assert "category" in data
        assert "total_candidates" in data
        assert "total_results" in data
        assert "results" in data
        assert "pipeline" in data
        assert "generated_at" in data

    def test_discover_with_constraints(self, client):
        response = client.post("/discover", json={
            "intent_text": "noise-canceling headphones under budget",
            "category": "product",
            "constraints": {
                "max_price": 300.0,
                "region": ["us-east"]
            }
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_results"] >= 0

    def test_discover_filters_by_category(self, client):
        response = client.post("/discover", json={
            "intent_text": "I need GPU compute resources",
            "category": "compute",
        })
        assert response.status_code == 200
        data = response.json()
        # No compute offerings in test setup from conftest, but should return 200
        assert data["category"] == "compute"

    def test_discover_invalid_category(self, client):
        response = client.post("/discover", json={
            "intent_text": "test",
            "category": "invalid_category",
        })
        assert response.status_code == 422

    def test_discover_empty_intent_text(self, client):
        response = client.post("/discover", json={
            "intent_text": "",
            "category": "product",
        })
        assert response.status_code == 422

    def test_discover_pipeline_stages(self, client):
        response = client.post("/discover", json={
            "intent_text": "noise-canceling headphones",
            "category": "product",
        })
        data = response.json()
        stages = data["pipeline"]["stages_executed"]
        assert "parse_request" in stages
        assert "normalize_intent" in stages
        assert "deterministic_filtering" in stages
        assert "semantic_matching" in stages
        assert "ranking" in stages
        assert "response_generation" in stages

    def test_discover_result_has_score(self, client):
        response = client.post("/discover", json={
            "intent_text": "noise-canceling headphones bluetooth premium",
            "category": "product",
        })
        data = response.json()
        if data["total_results"] > 0:
            result = data["results"][0]
            assert "total_score" in result
            assert 0.0 <= result["total_score"] <= 1.0
            assert "score_breakdown" in result
            assert "explanation" in result

    def test_discover_max_results_respected(self, client):
        response = client.post("/discover", json={
            "intent_text": "headphones",
            "category": "product",
            "preferences": {"max_results": 1}
        })
        data = response.json()
        assert len(data["results"]) <= 1

    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["protocol"] == "ADP"
        assert "registry" in data
