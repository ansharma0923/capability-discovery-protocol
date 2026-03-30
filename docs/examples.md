# Examples

See the `examples/` directory for working Python scripts.

## Product Discovery

```python
# examples/product_discovery.py
from cdp.intent.models import DiscoveryIntent, Category, Constraints
from cdp.service.discovery import run_discovery_pipeline

intent = DiscoveryIntent(
    intent_text="I need noise-canceling headphones under $300 for remote work",
    category=Category.PRODUCT,
    constraints=Constraints(max_price=300.0, region=["us-east"]),
)
result = run_discovery_pipeline(intent)
for r in result["results"]:
    print(f"Score: {r['total_score']:.2f} | {r['offering_id']}")
```

## Agent Discovery

```python
intent = DiscoveryIntent(
    intent_text="I need an LLM for code generation with low latency",
    category=Category.AGENT,
    constraints=Constraints(max_latency_ms=300),
)
```

## Cost-Optimized Search

```python
from cdp.intent.models import Preferences, RankingProfile

intent = DiscoveryIntent(
    intent_text="cheapest GPU compute available",
    category=Category.COMPUTE,
    preferences=Preferences(ranking_profile=RankingProfile.COST_OPTIMIZED),
)
```

## Compliance-Filtered

```python
intent = DiscoveryIntent(
    intent_text="HIPAA-compliant data storage API",
    category=Category.API,
    constraints=Constraints(compliance=["HIPAA", "SOC2"]),
)
```
