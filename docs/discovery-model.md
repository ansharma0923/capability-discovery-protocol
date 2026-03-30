# Discovery Model

## Intent-Driven Discovery

CDP uses a two-phase discovery model:

1. **Deterministic Filtering**: Hard constraints eliminate impossible candidates
2. **Semantic Scoring**: Soft relevance scoring ranks remaining candidates

## Constraint Types

| Constraint | Type | Description |
|-----------|------|-------------|
| `max_price` | Hard | Offering price must be ≤ this value |
| `region` | Hard | Offering must serve at least one listed region |
| `max_latency_ms` | Hard | Offering latency must be ≤ this value |
| `delivery_days` | Hard | Delivery time must be ≤ this value |
| `compliance` | Hard | Offering must have ALL listed certifications |
| `availability_min` | Hard | Offering availability must be ≥ this value |

## Semantic Matching

Semantic matching extracts keywords from the intent text (removing stop words) and searches offering name, description, tags, and capabilities. The score is `matched_keywords / total_keywords`.

## Capability Validation

Before ranking, each (offering, provider) pair is validated:
- Provider must support the requested category
- Provider must serve at least one requested region
