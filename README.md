# Agent Discovery Protocol (ADP)

![Build](https://github.com/ansharma0923/agent-discovery-protocol/actions/workflows/ci.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.11%2B-blue) ![License](https://img.shields.io/badge/license-Apache%202.0-green) ![Version](https://img.shields.io/badge/version-0.1.0-orange)

> **Status**: v0.1.0 — early reference implementation. APIs and wire format are subject to change before v1.0.

**Intent-driven discovery of agents, services, products, data, and APIs.**

ADP solves the problem of how AI agents, applications, and humans can discover the right provider for any capability — using natural language intent rather than rigid query syntax.

## Key Features

- 🎯 **Intent-driven**: Natural language discovery requests
- 🔍 **14-stage pipeline**: Parse → Filter → Semantic Match → Validate → Rank → Audit → Respond
- 🏆 **Explainable ranking**: Score breakdowns with human-readable explanations
- 🌐 **Federation**: Query distributed ADP nodes
- 🛡️ **Policy engine**: Pluggable provider trust and compliance rules
- 📊 **Audit logging**: Full observability for every discovery
- ⚡ **6 categories**: product, service, agent, data, compute, api

## Agent Discovery Plane (ADP) Context

### The Gap

Current agent ecosystems lack a structured layer for capability discovery. Agents can invoke tools and call APIs, but there is no standardized mechanism for an agent to express *what it needs* and receive a ranked, policy-filtered set of providers capable of fulfilling that need.

Agent registries list agents. Merchant catalogs list products. Neither resolves intent to the right provider in real time.

### Role of ADP in the Stack

ADP operates as the **discovery plane** in a multi-layer agentic stack:

```
SIP  (Signal / Instruction Plane)   — intent originates here
 │
ADP  (Agent Discovery Protocol)     — intent-driven discovery layer
 │
A2A  (Agent-to-Agent)               — negotiation and contracting
 │
UCP  (Unified Commerce Protocol)    — transaction and fulfillment
 │
AP2  (Agentic Payment Protocol)     — payment and settlement
```

ADP sits between intent formation and negotiation. It does not execute tasks, manage payments, or handle post-discovery communication. Its sole function is to resolve a structured intent into a ranked set of matching providers and offerings.

### Interaction Flow

```
Intent → Discovery (ADP) → Negotiation → Transaction
```

1. **Intent**: A caller expresses a capability need in natural language with optional structured constraints.
2. **Discovery**: ADP indexes capabilities and offerings, resolves the intent against registered providers, and returns a ranked result set scored on relevance, price, trust, and availability.
3. **Negotiation**: The selected provider and caller negotiate terms (handled at the A2A layer).
4. **Transaction**: The agreed capability is executed and settled (handled at UCP/AP2 layers).

### How ADP Differs

| Concept | Description |
|---|---|
| **Agent registry** | A static list of agents and their metadata. Does not resolve intent or rank results. |
| **Merchant catalog** | A product listing optimized for human browsing. Does not support structured constraints or real-time resolution. |
| **ADP** | An intent-driven discovery layer that resolves natural language capability requests against indexed providers in real time, ranked by relevance, price, trust, and availability. |

### Design Principle

ADP moves the ecosystem from **static catalog lookup** to **intent-driven discovery**: providers index their capabilities and offerings; callers express intent; ADP resolves and ranks matches at request time.

See [docs/adp-context.md](docs/adp-context.md) for the full protocol context document.

## Architecture

```
DiscoveryIntent
      │
      ▼
┌─────────────────────────────────────────────────┐
│              14-Stage Pipeline                   │
│  1. parse_request      8. policy_filtering       │
│  2. normalize_intent   9. ranking                │
│  3. extract_constraints 10. explanation_gen      │
│  4. retrieve_candidates 11. federation_merge     │
│  5. deterministic_filter 12. deduplication       │
│  6. semantic_matching   13. audit_logging        │
│  7. capability_validation 14. response_gen       │
└─────────────────────────────────────────────────┘
      │
      ▼
  DiscoveryResponse (ranked results + explanations)
```

## Quick Start

### Install

```bash
pip install -e ".[dev]"
```

### Run Server

```bash
uvicorn adp.main:app --reload --port 8000
```

### First Query

```bash
curl -X POST http://localhost:8000/discover \
  -H "Content-Type: application/json" \
  -d '{
    "intent_text": "I need noise-canceling headphones under $300",
    "category": "product",
    "constraints": {"max_price": 300.0, "region": ["us-east"]}
  }'
```

### Example Response

```json
{
  "intent_id": "550e8400-e29b-41d4-a716-446655440000",
  "version": "0.1.0",
  "category": "product",
  "total_candidates": 3,
  "total_results": 2,
  "results": [
    {
      "offering_id": "off-elec-001",
      "provider_id": "11111111-1111-1111-1111-111111111111",
      "total_score": 0.8542,
      "score_breakdown": {
        "relevance": 0.27, "price": 0.15, "latency": 0.15,
        "availability": 0.149, "trust": 0.15, "freshness": 0.05
      },
      "explanation": {
        "summary": "Offering 'ProANC Headphones X1' scored 0.85",
        "matched_constraints": ["price <= $300.0", "region in ['us-east']"]
      }
    }
  ],
  "pipeline": {
    "stages_executed": ["parse_request", "...", "response_generation"],
    "duration_ms": 2.4,
    "federation_used": false
  }
}
```

## Repository Structure

```
├── adp/              # Python implementation
│   ├── intent/       # Intent parsing and models
│   ├── registry/     # Provider and offering registry
│   ├── matching/     # Filter, semantic, validator
│   ├── ranking/      # Scorer and profiles
│   ├── federation/   # Federated discovery client
│   ├── policy/       # Policy enforcement engine
│   ├── observability/# Audit logging
│   ├── api/          # FastAPI routes and middleware
│   └── service/      # Core discovery pipeline
├── schema/           # JSON Schema Draft 7 definitions
├── protocol-vectors/ # Canonical test fixtures
├── data/             # Sample providers and offerings
├── docs/             # Protocol documentation
├── examples/         # Usage examples
├── tests/            # Test suites
└── sdk/              # SDK stubs (Go planned)
```

## Testing

```bash
# All tests
pytest tests/ -v

# By suite
pytest tests/unit/ -v
pytest tests/functional/ -v
pytest tests/schema_validation/ -v
pytest tests/protocol_vectors/ -v
pytest tests/interoperability/ -v
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).
