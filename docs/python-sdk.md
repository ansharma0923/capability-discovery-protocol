# Python SDK Reference

The `adp` Python package provides the full Capability Discovery Protocol implementation. Use it directly in your applications without running the HTTP server.

## Installation

```bash
pip install -e ".[dev]"   # from source (editable)
```

Or add `agent-discovery-protocol` to your project dependencies once published to PyPI.

## Core Modules

| Module | Description |
|--------|-------------|
| `adp.intent.models` | Pydantic models for discovery intent, constraints, preferences |
| `adp.registry.models` | Provider and offering descriptors |
| `adp.registry.store` | In-memory registry with TTL support |
| `adp.service.discovery` | 14-stage discovery pipeline |
| `adp.federation.client` | Federation client and local simulator |
| `adp.policy.engine` | Pluggable policy rules |
| `adp.ranking.scorer` | Composite score and ranking profiles |
| `adp.matching.filter` | Deterministic constraint filtering |
| `adp.matching.semantic` | Keyword-based semantic scoring |
| `adp.observability.audit` | Audit record logging |

---

## Quick Example

```python
from adp.intent.models import DiscoveryIntent, Category, Constraints, Preferences
from adp.registry.models import ProviderDescriptor, OfferingDescriptor, TrustLevel
from adp.registry.store import RegistryStore
from adp.service.discovery import run_discovery_pipeline

# 1. Create a registry
store = RegistryStore()

# 2. Register a provider
provider = ProviderDescriptor(
    name="My Store",
    description="Electronics retailer",
    categories=["product"],
    regions=["us-east"],
    trust_level=TrustLevel.VERIFIED,
)
store.register_provider(provider)

# 3. Register an offering
offering = OfferingDescriptor(
    provider_id=provider.provider_id,
    name="Pro ANC Headphones",
    description="Professional noise-canceling headphones",
    category="product",
    price=249.99,
    region=["us-east"],
    active=True,
)
store.register_offering(offering)

# 4. Build a discovery intent
intent = DiscoveryIntent(
    intent_text="I need noise-canceling headphones under $300",
    category=Category.PRODUCT,
    constraints=Constraints(max_price=300.0, region=["us-east"]),
    preferences=Preferences(max_results=5),
)

# 5. Run the pipeline
response = run_discovery_pipeline(intent, store=store)
print(f"Found {response['total_results']} results")
for r in response["results"]:
    print(f"  {r['offering_id']} — score {r['total_score']:.4f}")
    print(f"  {r['explanation']['summary']}")
```

---

## Models

### `DiscoveryIntent`

```python
class DiscoveryIntent(BaseModel):
    intent_id: str          # UUID, auto-generated
    version: str            # "0.1.0"
    intent_text: str        # 1–2000 characters
    category: Category      # product | service | agent | data | compute | api
    constraints: Constraints
    preferences: Preferences
    metadata: Dict[str, Any]
    created_at: datetime
```

### `Category`

```python
class Category(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"
    AGENT   = "agent"
    DATA    = "data"
    COMPUTE = "compute"
    API     = "api"
```

### `Constraints`

```python
class Constraints(BaseModel):
    max_price: Optional[float]        # upper price bound
    currency: Optional[str]           # default "USD"
    region: Optional[List[str]]       # e.g. ["us-east", "eu-west"]
    max_latency_ms: Optional[int]     # maximum acceptable latency
    delivery_days: Optional[int]      # maximum delivery time
    compliance: Optional[List[str]]   # e.g. ["SOC2", "HIPAA"]
    availability_min: Optional[float] # minimum availability (0–1)
```

### `Preferences`

```python
class Preferences(BaseModel):
    ranking_profile: RankingProfile   # default | cost_optimized | latency_optimized | trust_optimized
    max_results: int                  # 1–100, default 10
    include_federation: bool          # default False
```

### `ProviderDescriptor`

```python
class ProviderDescriptor(BaseModel):
    provider_id: str
    version: str
    name: str
    description: str
    categories: List[str]
    regions: List[str]
    trust_level: TrustLevel           # unverified | basic | verified | certified
    compliance_certifications: List[str]
    avg_latency_ms: Optional[int]
    availability_score: float         # 0–1
    ttl_seconds: int                  # default 3600
```

### `OfferingDescriptor`

```python
class OfferingDescriptor(BaseModel):
    offering_id: str
    version: str
    provider_id: str
    name: str
    description: str
    category: str
    tags: List[str]
    price: Optional[float]
    price_unit: Optional[str]         # e.g. "per-1k-tokens", "per-transaction"
    currency: str                     # default "USD"
    region: List[str]
    latency_ms: Optional[int]
    delivery_days: Optional[int]
    availability: float               # 0–1
    compliance: List[str]
    capabilities: List[str]
    active: bool
    ttl_seconds: int
```

---

## Registry Store

```python
from adp.registry.store import RegistryStore

store = RegistryStore()

# Providers
store.register_provider(provider)       # -> ProviderDescriptor
store.get_provider(provider_id)         # -> Optional[ProviderDescriptor]
store.list_providers()                  # -> List[ProviderDescriptor]
store.update_provider(id, {"name": "New Name"})  # -> Optional[ProviderDescriptor]

# Offerings
store.register_offering(offering)       # -> OfferingDescriptor
store.get_offering(offering_id)         # -> Optional[OfferingDescriptor]
store.list_offerings(provider_id=None)  # -> List[OfferingDescriptor]
store.update_offering(id, {"price": 199.99})     # -> Optional[OfferingDescriptor]
```

TTL is enforced on every read: expired entries return `None` and are removed.

### Shared Global Store

The API server uses a process-wide singleton:

```python
from adp.registry.store import get_store
store = get_store()
```

---

## Discovery Pipeline

```python
from adp.service.discovery import run_discovery_pipeline

response = run_discovery_pipeline(
    intent,                          # DiscoveryIntent
    store=store,                     # optional RegistryStore (uses global if None)
    federated_results=None,          # optional pre-fetched federated results
)
```

**Response shape:**

```python
{
    "intent_id": str,
    "version": str,
    "category": str,
    "total_candidates": int,         # offerings passing deterministic filters
    "total_results": int,
    "results": [
        {
            "offering_id": str,
            "provider_id": str,
            "total_score": float,    # 0–1
            "score_breakdown": {
                "relevance": float,
                "price": float,
                "latency": float,
                "availability": float,
                "trust": float,
                "freshness": float,
            },
            "explanation": {
                "matched_constraints": List[str],
                "relevance_reason": str,
                "price_fit": str,
                "latency_fit": str,
                "trust_reason": str,
                "summary": str,
            },
            "_source": "local" | "federated",
        }
    ],
    "pipeline": {
        "stages_executed": List[str],
        "duration_ms": float,
        "federation_used": bool,
    },
    "generated_at": str,             # ISO 8601
}
```

---

## Federation

### Real Remote Nodes

```python
from adp.federation.client import configure_federation, get_federation_client
import asyncio

configure_federation([
    "https://node1.cdp.example.com",
    "https://node2.cdp.example.com",
])

client = get_federation_client()
federated_results = asyncio.run(client.federate(intent))
response = run_discovery_pipeline(intent, federated_results=federated_results)
```

### Local Simulation (Testing / Demos)

```python
from adp.federation.client import FederationClient, LocalFederationSimulator

sim = LocalFederationSimulator(
    node_url="https://node1.cdp.example.com",
    offerings=[offering1, offering2],
    providers=[provider1],
)

client = FederationClient(nodes=["https://node1.cdp.example.com"])
client.register_simulator(sim)

federated_results = asyncio.run(client.federate(intent))
```

---

## Policy Engine

Add custom filtering rules that run at stage 8 of the pipeline:

```python
from adp.policy.engine import PolicyRule, PolicyEngine, get_policy_engine
from adp.registry.models import OfferingDescriptor, ProviderDescriptor

class SOC2RequiredPolicy(PolicyRule):
    name = "soc2_required"

    def apply(self, offering, provider):
        if "SOC2" not in offering.compliance:
            return False, "SOC2 certification required"
        return True, "SOC2 certified"

# Replace the global engine
import adp.policy.engine as eng
eng._engine = PolicyEngine(rules=[SOC2RequiredPolicy()])
```

---

## Ranking Profiles

```python
from adp.ranking.profiles import get_profile

profile = get_profile("cost_optimized")
print(profile)
# {'relevance': 0.25, 'price': 0.25, 'latency': 0.15, ...}
```

Available profiles: `default`, `cost_optimized`, `latency_optimized`, `trust_optimized`.

---

## REST API

If you prefer HTTP, start the server:

```bash
uvicorn adp.main:app --reload
```

Key endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/discover` | Run discovery pipeline |
| `POST` | `/register/provider` | Register a provider |
| `POST` | `/register/offering` | Register an offering |
| `PATCH` | `/update/provider/{id}` | Update a provider |
| `PATCH` | `/update/offering/{id}` | Update an offering |
| `GET` | `/providers/{id}` | Get a provider |
| `GET` | `/offerings/{id}` | Get an offering |
| `POST` | `/federate/discover` | Federated discovery |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc UI |
