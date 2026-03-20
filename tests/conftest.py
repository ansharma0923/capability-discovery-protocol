"""Pytest configuration and shared fixtures."""
import pytest
from fastapi.testclient import TestClient

from adp.intent.models import Category, Constraints, DiscoveryIntent, Preferences
from adp.main import app
from adp.registry.models import OfferingDescriptor, ProviderDescriptor, TrustLevel
from adp.registry.store import RegistryStore


@pytest.fixture
def store() -> RegistryStore:
    """Fresh registry store for each test."""
    return RegistryStore()


@pytest.fixture
def provider_certified(store: RegistryStore) -> ProviderDescriptor:
    """A certified provider registered in the store."""
    p = ProviderDescriptor(
        provider_id="11111111-1111-1111-1111-111111111111",
        name="ElectroMart",
        description="Consumer electronics and audio",
        categories=["product"],
        regions=["us-east", "us-west"],
        trust_level=TrustLevel.CERTIFIED,
        availability_score=0.999,
    )
    store.register_provider(p)
    return p


@pytest.fixture
def provider_verified(store: RegistryStore) -> ProviderDescriptor:
    """A verified provider registered in the store."""
    p = ProviderDescriptor(
        provider_id="22222222-2222-2222-2222-222222222222",
        name="CloudCompute Pro",
        description="Cloud compute resources",
        categories=["compute", "api"],
        regions=["us-east", "us-west", "eu-west"],
        trust_level=TrustLevel.VERIFIED,
        availability_score=0.9999,
    )
    store.register_provider(p)
    return p


@pytest.fixture
def offering_product(store: RegistryStore, provider_certified: ProviderDescriptor) -> OfferingDescriptor:
    """A product offering registered in the store."""
    o = OfferingDescriptor(
        offering_id="off-test-001",
        provider_id=provider_certified.provider_id,
        name="ProANC Headphones X1",
        description="Premium noise-canceling headphones with 40-hour battery",
        category="product",
        tags=["headphones", "anc", "noise-canceling", "bluetooth"],
        price=249.99,
        currency="USD",
        region=["us-east", "us-west"],
        delivery_days=2,
        availability=0.99,
        compliance=["CE", "FCC"],
        capabilities=["anc", "bluetooth", "hi-fi"],
        active=True,
    )
    store.register_offering(o)
    return o


@pytest.fixture
def offering_compute(store: RegistryStore, provider_verified: ProviderDescriptor) -> OfferingDescriptor:
    """A compute offering registered in the store."""
    o = OfferingDescriptor(
        offering_id="off-test-002",
        provider_id=provider_verified.provider_id,
        name="GPU Cluster H100",
        description="NVIDIA H100 GPU cluster for ML training",
        category="compute",
        tags=["gpu", "h100", "ml-training", "cuda"],
        price=3.50,
        price_unit="per-hour",
        currency="USD",
        region=["us-east", "us-west"],
        latency_ms=10,
        availability=0.999,
        compliance=["SOC2"],
        capabilities=["gpu", "ml-training", "cuda"],
        active=True,
    )
    store.register_offering(o)
    return o


@pytest.fixture
def intent_product() -> DiscoveryIntent:
    """A product discovery intent."""
    return DiscoveryIntent(
        intent_text="I need noise-canceling headphones for remote work",
        category=Category.PRODUCT,
        constraints=Constraints(max_price=300.0, region=["us-east"]),
        preferences=Preferences(max_results=10),
    )


@pytest.fixture
def intent_compute() -> DiscoveryIntent:
    """A compute discovery intent."""
    return DiscoveryIntent(
        intent_text="I need GPU compute for machine learning training",
        category=Category.COMPUTE,
        constraints=Constraints(max_latency_ms=100),
        preferences=Preferences(max_results=5),
    )


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)
