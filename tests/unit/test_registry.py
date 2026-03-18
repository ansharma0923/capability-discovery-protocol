"""Tests for the registry store."""
import time
import pytest
from adp.registry.store import RegistryStore
from adp.registry.models import ProviderDescriptor, OfferingDescriptor, TrustLevel


@pytest.fixture
def store():
    return RegistryStore()


@pytest.fixture
def provider():
    return ProviderDescriptor(
        provider_id="prov-reg-001",
        name="Test Provider",
        description="A test provider",
        categories=["product"],
        regions=["us-east"],
        trust_level=TrustLevel.VERIFIED,
        ttl_seconds=3600,
    )


@pytest.fixture
def offering(provider):
    return OfferingDescriptor(
        offering_id="off-reg-001",
        provider_id=provider.provider_id,
        name="Test Offering",
        description="A test offering",
        category="product",
        active=True,
        ttl_seconds=3600,
    )


class TestProviderRegistration:
    def test_register_and_get_provider(self, store, provider):
        store.register_provider(provider)
        result = store.get_provider(provider.provider_id)
        assert result is not None
        assert result.provider_id == provider.provider_id
        assert result.name == provider.name

    def test_get_nonexistent_returns_none(self, store):
        result = store.get_provider("nonexistent-id")
        assert result is None

    def test_list_providers(self, store, provider):
        store.register_provider(provider)
        providers = store.list_providers()
        assert len(providers) == 1
        assert providers[0].provider_id == provider.provider_id

    def test_update_provider(self, store, provider):
        store.register_provider(provider)
        updated = store.update_provider(provider.provider_id, {"name": "Updated Name"})
        assert updated is not None
        assert updated.name == "Updated Name"
        # Verify the update is persisted
        retrieved = store.get_provider(provider.provider_id)
        assert retrieved.name == "Updated Name"

    def test_update_nonexistent_returns_none(self, store):
        result = store.update_provider("nonexistent-id", {"name": "Test"})
        assert result is None


class TestOfferingRegistration:
    def test_register_and_get_offering(self, store, offering):
        store.register_offering(offering)
        result = store.get_offering(offering.offering_id)
        assert result is not None
        assert result.offering_id == offering.offering_id

    def test_get_nonexistent_returns_none(self, store):
        result = store.get_offering("nonexistent-id")
        assert result is None

    def test_list_offerings(self, store, offering):
        store.register_offering(offering)
        offerings = store.list_offerings()
        assert len(offerings) == 1

    def test_list_offerings_by_provider(self, store, offering):
        store.register_offering(offering)
        # Different provider offering
        other = OfferingDescriptor(
            offering_id="off-other-001",
            provider_id="other-provider",
            name="Other",
            description="Other",
            category="service",
            active=True,
        )
        store.register_offering(other)
        filtered = store.list_offerings(provider_id=offering.provider_id)
        assert len(filtered) == 1
        assert filtered[0].offering_id == offering.offering_id

    def test_update_offering(self, store, offering):
        store.register_offering(offering)
        updated = store.update_offering(offering.offering_id, {"name": "Updated"})
        assert updated is not None
        assert updated.name == "Updated"


class TestTTL:
    def test_expired_provider_returns_none(self, store):
        provider = ProviderDescriptor(
            provider_id="prov-ttl-001",
            name="TTL Test",
            description="TTL test provider",
            categories=["product"],
            regions=["us-east"],
            ttl_seconds=1,
        )
        store.register_provider(provider)
        time.sleep(1.1)
        result = store.get_provider(provider.provider_id)
        assert result is None

    def test_expired_offering_returns_none(self, store):
        offering = OfferingDescriptor(
            offering_id="off-ttl-001",
            provider_id="prov-001",
            name="TTL Test",
            description="TTL test offering",
            category="product",
            active=True,
            ttl_seconds=1,
        )
        store.register_offering(offering)
        time.sleep(1.1)
        result = store.get_offering(offering.offering_id)
        assert result is None


class TestAuditLog:
    def test_add_and_get_audit_log(self, store):
        record = {"audit_id": "test-123", "intent_text": "test intent"}
        store.add_audit_log(record)
        logs = store.get_audit_logs()
        assert len(logs) == 1
        assert logs[0]["audit_id"] == "test-123"

    def test_audit_log_limit(self, store):
        for i in range(10):
            store.add_audit_log({"audit_id": f"test-{i}"})
        logs = store.get_audit_logs(limit=5)
        assert len(logs) == 5
