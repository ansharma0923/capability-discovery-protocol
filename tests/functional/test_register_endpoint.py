"""Functional tests for the /register endpoints."""
import pytest
from fastapi.testclient import TestClient
from adp.main import app
from adp.registry.store import get_store


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def registered_provider_id(client):
    """Register a provider and return its ID."""
    response = client.post("/register/provider", json={
        "name": "Functional Test Provider",
        "description": "A provider for functional testing",
        "categories": ["product"],
        "regions": ["us-east"],
        "trust_level": "verified",
    })
    assert response.status_code == 200
    return response.json()["provider_id"]


class TestRegisterProviderEndpoint:
    def test_register_provider_returns_200(self, client):
        response = client.post("/register/provider", json={
            "name": "New Provider",
            "description": "A new provider",
            "categories": ["service"],
            "regions": ["us-east"],
        })
        assert response.status_code == 200

    def test_register_provider_returns_provider_id(self, client):
        response = client.post("/register/provider", json={
            "name": "ID Test Provider",
            "description": "Provider to test ID return",
            "categories": ["api"],
            "regions": ["us-west"],
        })
        data = response.json()
        assert "provider_id" in data
        assert "status" in data
        assert data["status"] == "registered"
        assert "registered_at" in data

    def test_register_provider_persists(self, client, registered_provider_id):
        response = client.get(f"/providers/{registered_provider_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["provider_id"] == registered_provider_id

    def test_register_provider_invalid_category(self, client):
        response = client.post("/register/provider", json={
            "name": "Incomplete Provider",
        })
        assert response.status_code == 422

    def test_register_provider_missing_fields(self, client):
        response = client.post("/register/provider", json={
            "name": "Incomplete Provider",
        })
        assert response.status_code == 422


class TestRegisterOfferingEndpoint:
    def test_register_offering_returns_200(self, client, registered_provider_id):
        response = client.post("/register/offering", json={
            "provider_id": registered_provider_id,
            "name": "Test Product",
            "description": "A test product offering",
            "category": "product",
            "price": 99.99,
            "region": ["us-east"],
        })
        assert response.status_code == 200

    def test_register_offering_returns_offering_id(self, client, registered_provider_id):
        response = client.post("/register/offering", json={
            "provider_id": registered_provider_id,
            "name": "ID Test Offering",
            "description": "Offering to test ID return",
            "category": "product",
        })
        data = response.json()
        assert "offering_id" in data
        assert "provider_id" in data
        assert "status" in data
        assert data["status"] == "registered"
        assert data["provider_id"] == registered_provider_id

    def test_register_offering_nonexistent_provider(self, client):
        response = client.post("/register/offering", json={
            "provider_id": "nonexistent-provider-id",
            "name": "Orphan Offering",
            "description": "Offering with no provider",
            "category": "service",
        })
        assert response.status_code == 404

    def test_register_offering_persists(self, client, registered_provider_id):
        reg_response = client.post("/register/offering", json={
            "provider_id": registered_provider_id,
            "name": "Persistent Offering",
            "description": "Should be retrievable",
            "category": "product",
        })
        offering_id = reg_response.json()["offering_id"]
        get_response = client.get(f"/offerings/{offering_id}")
        assert get_response.status_code == 200
        assert get_response.json()["offering_id"] == offering_id


class TestGetEndpoints:
    def test_get_nonexistent_provider(self, client):
        response = client.get("/providers/nonexistent-id")
        assert response.status_code == 404

    def test_get_nonexistent_offering(self, client):
        response = client.get("/offerings/nonexistent-id")
        assert response.status_code == 404

    def test_update_provider(self, client, registered_provider_id):
        response = client.patch(
            f"/update/provider/{registered_provider_id}",
            json={"name": "Updated Provider Name"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "updated"
        assert data["provider_id"] == registered_provider_id

    def test_update_nonexistent_provider(self, client):
        response = client.patch(
            "/update/provider/nonexistent-id",
            json={"name": "Will Fail"}
        )
        assert response.status_code == 404
