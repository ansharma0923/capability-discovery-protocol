# Protocol Overview

## Core Concepts

### DiscoveryIntent

A `DiscoveryIntent` is the primary input to ADP. It encapsulates:
- **intent_text**: Natural language description of what is needed
- **category**: One of `product`, `service`, `agent`, `data`, `compute`, `api`
- **constraints**: Hard constraints (price, region, latency, compliance, availability)
- **preferences**: Soft preferences (ranking profile, max results, federation)

### ProviderDescriptor

Providers register themselves with metadata:
- Identity, categories, regions, trust level
- Compliance certifications, availability score
- TTL for cache invalidation

### OfferingDescriptor

Offerings are specific capabilities provided by a provider:
- Name, description, category, tags, capabilities
- Pricing, region, latency, compliance
- TTL and active status

### DiscoveryResponse

The protocol response includes:
- Ranked list of matching offerings
- Score breakdown per result
- Human-readable explanation per result
- Pipeline execution metadata
- Audit information

## Protocol Flow

```
1. Client sends POST /discover with DiscoveryIntent
2. ADP normalizes the intent
3. Registry is queried for matching offerings
4. Deterministic filters applied (price, region, compliance, etc.)
5. Semantic matching scores each candidate
6. Capability validation checks provider-offering consistency
7. Policy engine filters by trust and compliance rules
8. Weighted ranking produces final scores
9. Optional federation merge from remote nodes
10. Deduplication applied
11. Audit record written
12. DiscoveryResponse returned
```

## Versioning

ADP uses semantic versioning. The current protocol version is `0.1.0`.
All messages include a `version` field.
