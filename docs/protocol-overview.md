# Protocol Overview

## Core Concepts

### DiscoveryIntent

A `DiscoveryIntent` is the primary input to CDP. It encapsulates:
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
2. CDP normalizes the intent
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

## Multi-Plane Architecture

CDP is one layer in a multi-plane agentic stack. Understanding its position clarifies its scope and boundaries.

```
SIP  (Signal / Instruction Plane)   — intent originates here
 │
CDP  (Capability Discovery Protocol)     — intent-driven discovery layer
 │
A2A  (Agent-to-Agent)               — negotiation and contracting
 │
UCP  (Unified Commerce Protocol)    — transaction and fulfillment
 │
AP2  (Agentic Payment Protocol)     — payment and settlement
```

### Flow: Intent → Discovery → Negotiation → Transaction

```
Intent
  │  Caller forms a capability need (natural language + constraints).
  ▼
Discovery (CDP)
  │  CDP resolves the intent against indexed providers and offerings.
  │  Returns a ranked DiscoveryResponse scored on relevance, price,
  │  trust, and availability.
  ▼
Negotiation (A2A)
  │  Caller and selected provider negotiate terms using the
  │  DiscoveryResponse as the starting point.
  ▼
Transaction (UCP / AP2)
     Agreed capability is executed, fulfilled, and settled.
```

CDP does not participate in negotiation, execution, or payment. It produces discovery output only — a ranked list of providers and offerings that match the expressed intent.

### Scope Boundaries

| Layer | Responsibility | CDP's role |
|---|---|---|
| SIP | Signal formation and instruction routing | Upstream of CDP — provides the intent |
| **CDP** | **Intent-driven discovery and ranking** | **This layer** |
| A2A | Agent-to-agent negotiation and contracting | Downstream — consumes CDP output |
| UCP | Transaction and fulfillment | Downstream — post-discovery |
| AP2 | Payment and settlement | Downstream — post-discovery |

## Versioning

CDP uses semantic versioning. The current protocol version is `0.1.0`.
All messages include a `version` field.
