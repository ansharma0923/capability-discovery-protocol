# Examples Walkthrough

This document walks through each example in the `examples/` directory and explains the concepts they demonstrate.

## Prerequisites

Install the package before running any example:

```bash
pip install -e ".[dev]"
```

All examples are self-contained — they create an in-memory registry, register providers and offerings, run the discovery pipeline, and print results. No running server is required.

---

## 1. Product Discovery (`product_discovery.py`)

Demonstrates discovering physical products that match a budget and region constraint.

**Key concepts:**
- Registering a `ProviderDescriptor` with `TrustLevel.CERTIFIED`
- Registering multiple `OfferingDescriptor` objects in the `product` category
- Running discovery with `max_price` and `region` constraints
- Inspecting the 14-stage pipeline output

**Run:**

```bash
python examples/product_discovery.py
```

**Expected output:**
```
=== Product Discovery Demo ===
Intent: I need noise-canceling headphones under $300 for remote work
...
Found 2 results from 2 candidates
Pipeline: 14 stages in X.XXms
...
```

The pipeline executes all 14 stages: parse_request → normalize_intent → extract_constraints → retrieve_candidates → deterministic_filtering → semantic_matching → capability_validation → policy_filtering → ranking → explanation_generation → federation_merge → deduplication → audit_logging → response_generation.

---

## 2. Service Discovery (`service_discovery.py`)

Demonstrates discovering B2B services with compliance requirements.

**Key concepts:**
- Filtering by `compliance` constraint (SOC2, PCI-DSS)
- `TrustLevel.CERTIFIED` providers score higher
- Pricing for services (monthly flat fee, per-transaction)

**Run:**

```bash
python examples/service_discovery.py
```

The `compliance` constraint filters out any offering that does not list the required certifications. The semantic scorer then ranks the remaining offerings by text similarity to the intent.

---

## 3. Agent Discovery (`agent_discovery.py`)

Demonstrates discovering LLM inference APIs with a latency-optimized ranking profile.

**Key concepts:**
- `category = "agent"` for AI agent / LLM offerings
- `max_latency_ms` constraint eliminates high-latency offerings
- `ranking_profile = "latency_optimized"` boosts the latency score weight
- `price_unit = "per-1k-tokens"` for usage-based pricing

**Run:**

```bash
python examples/agent_discovery.py
```

The latency-optimized profile applies higher weight to the latency component of the composite score, so the fast-inference offering ranks first even though it is priced lower.

---

## 4. Federation Demo (`federation_demo.py`)

Demonstrates multi-node ADP federation using a local in-process simulation.

**Key concepts:**
- `LocalFederationSimulator` — simulates a remote ADP node without network I/O
- `FederationClient.register_simulator()` — registers a simulator for a node URL
- Remote node results are tagged `_source = "federated"` and `_node = <url>`
- Results from all nodes are merged, deduplicated (by `offering_id`), and re-ranked

**Run:**

```bash
python examples/federation_demo.py
```

**Expected output:**
```
Configured 2 federation nodes (local simulation):
  - https://node1.adp.example.com
  - https://node2.adp.example.com

Results from remote nodes: 2
  [https://node1.adp.example.com] fed-off-node1-001 score=0.68
  [https://node2.adp.example.com] fed-off-node2-001 score=0.68

Total results after merge+dedup+rerank: 3
Federation used: True
...
Final ranked results:
  1. [local    ] score=0.73 | local-off-001  ...
  2. [federated] score=0.68 | fed-off-node2-001 ...
  3. [federated] score=0.68 | fed-off-node1-001 ...
```

The local node's result ranks first because the provider has `TrustLevel.CERTIFIED` (vs `BASIC` on node-2 and `VERIFIED` on node-1), giving it a higher trust component in the composite score.

> **Note:** In production, `FederationClient` makes real HTTP POST requests to `/discover` on each remote node. The `LocalFederationSimulator` is provided for testing and demos.

---

## 5. Policy Demo (`policy_demo.py`)

Demonstrates the policy engine with built-in and custom rules.

**Key concepts:**
- `ActiveOnlyPolicy` — excludes inactive offerings
- `VerifiedProviderPolicy` — excludes providers below `TrustLevel.VERIFIED`
- Custom policy class implementing `FilterPolicy`

**Run:**

```bash
python examples/policy_demo.py
```

The policy engine runs after capability validation (stage 8) and before ranking (stage 9). Multiple policies are composed with AND semantics — an offering is excluded if any policy rejects it.

---

## Understanding the Discovery Pipeline

Every call to `run_discovery_pipeline()` executes 14 stages:

| Stage | Name | Description |
|-------|------|-------------|
| 1 | parse_request | Validate the incoming intent |
| 2 | normalize_intent | Lowercase, strip whitespace |
| 3 | extract_constraints | Pull keywords from the intent text |
| 4 | retrieve_candidates | Load all offerings from the registry |
| 5 | deterministic_filtering | Apply hard constraints (price, region, compliance, ...) |
| 6 | semantic_matching | Score offerings by keyword overlap with the intent |
| 7 | capability_validation | Verify provider/offering capability match |
| 8 | policy_filtering | Apply configured policy rules |
| 9 | ranking | Composite score using weighted sub-scores |
| 10 | explanation_generation | Build human-readable explanation per result |
| 11 | federation_merge | Merge any results from remote nodes |
| 12 | deduplication | Remove duplicate offering_ids |
| 13 | audit_logging | Write a `DiscoveryAuditRecord` |
| 14 | response_generation | Assemble the final response dict |

## Ranking Profiles

| Profile | Emphasis |
|---------|----------|
| `default` | Balanced across relevance, price, latency, availability, trust, freshness |
| `cost_optimized` | Higher weight on price component |
| `latency_optimized` | Higher weight on latency component |
| `trust_optimized` | Higher weight on trust component |
