# CDP Context

> **Naming note:** CDP (Capability Discovery Protocol), previously referred to in earlier drafts as CFP (Capability Fabric Protocol), is the capability-centric evolution of the original ADP (Agent Discovery Protocol) work.

## Problem

AI agents, applications, and automated systems increasingly need to locate external capabilities at runtime — services, data sources, APIs, compute resources, products, skills, workflows, and other agents. The current ecosystem provides no standardized mechanism for expressing *what is needed* and receiving a ranked, policy-filtered list of providers capable of fulfilling that need.

## Current Ecosystem Limitations

Existing approaches address adjacent but distinct concerns:

- **Agent registries** maintain a directory of agents and their declared metadata. They do not resolve intent, apply constraints, or rank results.
- **Merchant and service catalogs** are optimized for human browsing. They lack structured constraint handling, real-time resolution, and machine-readable ranking signals.
- **API directories** require callers to know what they are looking for. They do not operate on natural language intent or apply trust and compliance filters automatically.

None of these systems close the gap between a caller's expressed need and a ranked set of matching providers.

## The Gap

There is no standardized **capability discovery plane** in the agentic stack — a layer that accepts a structured intent from a caller and returns a ranked, policy-filtered set of offerings from registered providers, resolved in real time.

Without such a layer, every agent or application must implement its own ad hoc discovery logic, leading to fragmentation, non-interoperable catalogs, and undiscoverable capabilities.

## Goal

Define and implement a protocol — the Capability Discovery Protocol (CDP) — that:

- Accepts intent expressed in natural language with optional structured constraints.
- Indexes provider capabilities and offerings in a machine-readable format.
- Resolves intent to a ranked result set at request time.
- Filters results by price, region, latency, compliance, trust, and availability.
- Returns explainable scores so callers can make informed selection decisions.
- Operates across federated CDP nodes.

## Role of CDP

CDP is the **capability discovery plane** in a multi-plane agentic stack. It is a capability-centric discovery system for agentic and non-agentic systems. CDP is not:

- A task executor — it does not invoke or run capabilities.
- An agent registry — it does not maintain a static directory of agents.
- A merchant catalog — it is not optimized for human browsing or manual lookup.
- A negotiation protocol — it does not handle contracting or terms agreement.
- A payment protocol — it does not manage transactions or settlement.
- An intent validator — it does not validate intent or enforce policy.
- A plan generator — it does not generate execution plans.

CDP's sole responsibility is to resolve a structured intent into a ranked set of matching providers and offerings, answering:
- **What capabilities exist?**
- **Which ones match?**
- **Which ones are best?**

## Interaction with Other Layers

CDP operates within a layered agentic stack:

```
SIP  (Signal / Instruction Plane)   — intent originates here
 │
CDP  (Capability Discovery Protocol) — capability discovery plane
 │
A2A  (Agent-to-Agent)               — negotiation and contracting
 │
UCP  (Unified Commerce Protocol)    — transaction and fulfillment
 │
AP2  (Agentic Payment Protocol)     — payment and settlement
```

**Interaction flow:**

```
Intent → Discovery (CDP) → Negotiation → Transaction
```

1. **Intent**: A caller forms a capability need — either autonomously or in response to an instruction from an upstream signal plane (SIP).
2. **Discovery**: CDP receives the `DiscoveryIntent`, resolves it against registered providers and offerings, applies filters and ranking, and returns a `DiscoveryResponse`.
3. **Negotiation**: The caller and selected provider negotiate terms at the A2A layer, using CDP's response as the starting point.
4. **Transaction**: The agreed capability is executed, fulfilled, and settled at the UCP and AP2 layers.

CDP does not reach into the negotiation or transaction layers. It produces discovery output only.

## Core Idea

Move the ecosystem from **static catalog lookup** to **intent-driven capability discovery**:

- Providers index their capabilities and offerings in a machine-readable format.
- Callers express what they need using natural language and structured constraints.
- CDP resolves and ranks matches at request time, based on relevance, price, trust, and availability.

This shifts the discovery model from a pull-based, keyword-driven search to a push-and-resolve model where intent drives the result.

## Compatibility Notes

- **ADP** (Agent Discovery Protocol) was the original agent-centric framing of this work.
- **CFP** (Capability Fabric Protocol) was an intermediate rename during capability-centric evolution.
- **CDP** (Capability Discovery Protocol) is the final preferred name.

The Python reference implementation retains the `adp` package name for backward compatibility.

## Build Direction

The CDP protocol and reference implementation are designed around the following principles:

- **Intent-first**: Every discovery request begins with a natural language intent and optional structured constraints.
- **Capability and offering indexing**: Providers register machine-readable descriptors for their capabilities and offerings, enabling real-time resolution.
- **Real-time resolution**: Discovery is performed at request time, not pre-computed or cached beyond TTL boundaries.
- **Ranking based on relevance, price, trust, and availability**: Results are scored using a weighted multi-factor model with explainable breakdowns.
- **Federation-ready**: Discovery can span multiple CDP nodes, enabling distributed capability indexing.
- **Auditable**: Every discovery event is logged for observability and compliance.
- **Open and language-agnostic**: Apache 2.0 licensed, schema-first, with a JSON Schema wire format.
