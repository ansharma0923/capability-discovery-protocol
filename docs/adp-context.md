# ADP Context

## Problem

AI agents, applications, and automated systems increasingly need to locate external capabilities at runtime — services, data sources, APIs, compute resources, products, and other agents. The current ecosystem provides no standardized mechanism for expressing *what is needed* and receiving a ranked, policy-filtered list of providers capable of fulfilling that need.

## Current Ecosystem Limitations

Existing approaches address adjacent but distinct concerns:

- **Agent registries** maintain a directory of agents and their declared metadata. They do not resolve intent, apply constraints, or rank results.
- **Merchant and service catalogs** are optimized for human browsing. They lack structured constraint handling, real-time resolution, and machine-readable ranking signals.
- **API directories** require callers to know what they are looking for. They do not operate on natural language intent or apply trust and compliance filters automatically.

None of these systems close the gap between a caller's expressed need and a ranked set of matching providers.

## The Gap

There is no standardized **discovery plane** in the agentic stack — a layer that accepts a structured intent from a caller and returns a ranked, policy-filtered set of offerings from registered providers, resolved in real time.

Without such a layer, every agent or application must implement its own ad hoc discovery logic, leading to fragmentation, non-interoperable catalogs, and undiscoverable capabilities.

## Goal

Define and implement a protocol — the Agent Discovery Protocol (ADP) — that:

- Accepts intent expressed in natural language with optional structured constraints.
- Indexes provider capabilities and offerings in a machine-readable format.
- Resolves intent to a ranked result set at request time.
- Filters results by price, region, latency, compliance, trust, and availability.
- Returns explainable scores so callers can make informed selection decisions.
- Operates across federated ADP nodes.

## Role of ADP

ADP is the **intent-driven discovery layer** in a multi-plane agentic stack. It is not:

- A task executor — it does not invoke or run capabilities.
- An agent registry — it does not maintain a static directory of agents.
- A merchant catalog — it is not optimized for human browsing or manual lookup.
- A negotiation protocol — it does not handle contracting or terms agreement.
- A payment protocol — it does not manage transactions or settlement.

ADP's sole responsibility is to resolve a structured intent into a ranked set of matching providers and offerings, ready for the caller to select and proceed.

## Interaction with Other Layers

ADP operates within a layered agentic stack:

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

**Interaction flow:**

```
Intent → Discovery (ADP) → Negotiation → Transaction
```

1. **Intent**: A caller forms a capability need — either autonomously or in response to an instruction from an upstream signal plane (SIP).
2. **Discovery**: ADP receives the `DiscoveryIntent`, resolves it against registered providers and offerings, applies filters and ranking, and returns a `DiscoveryResponse`.
3. **Negotiation**: The caller and selected provider negotiate terms at the A2A layer, using ADP's response as the starting point.
4. **Transaction**: The agreed capability is executed, fulfilled, and settled at the UCP and AP2 layers.

ADP does not reach into the negotiation or transaction layers. It produces discovery output only.

## Core Idea

Move the ecosystem from **static catalog lookup** to **intent-driven discovery**:

- Providers index their capabilities and offerings in a machine-readable format.
- Callers express what they need using natural language and structured constraints.
- ADP resolves and ranks matches at request time, based on relevance, price, trust, and availability.

This shifts the discovery model from a pull-based, keyword-driven search to a push-and-resolve model where intent drives the result.

## Build Direction

The ADP protocol and reference implementation are designed around the following principles:

- **Intent-first**: Every discovery request begins with a natural language intent and optional structured constraints.
- **Capability and offering indexing**: Providers register machine-readable descriptors for their capabilities and offerings, enabling real-time resolution.
- **Real-time resolution**: Discovery is performed at request time, not pre-computed or cached beyond TTL boundaries.
- **Ranking based on relevance, price, trust, and availability**: Results are scored using a weighted multi-factor model with explainable breakdowns.
- **Federation-ready**: Discovery can span multiple ADP nodes, enabling distributed capability indexing.
- **Auditable**: Every discovery event is logged for observability and compliance.
- **Open and language-agnostic**: Apache 2.0 licensed, schema-first, with a JSON Schema wire format.
