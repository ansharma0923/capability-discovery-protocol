# ADP Overview

## What is Agent Discovery Protocol?

The Agent Discovery Protocol (ADP) is an open protocol for **intent-driven discovery** of agents, services, products, data, compute resources, and APIs. It accepts a structured intent from any caller — AI agent, application, or human — and returns a ranked set of matching providers resolved in real time.

ADP is:

- An **intent-driven discovery layer** — it resolves natural language capability requests to ranked provider matches in real time.
- A **capability and offering indexing protocol** — providers register machine-readable descriptors; ADP indexes and resolves against them.

ADP is not:

- A **catalog** — it does not serve pre-built listings for human browsing.
- A **registry** — it does not maintain a static directory of agents or services without discovery semantics.
- An **execution layer** — it does not invoke, run, or manage capabilities after discovery.

## The Problem

As the number of AI agents, microservices, and digital products grows, discovering the right one becomes increasingly difficult. Traditional approaches rely on:
- Static catalogs that require exact keyword matching
- Search engines that return pages of irrelevant results
- Manual API documentation browsing

None of these approaches support structured intent, constraint filtering, or real-time resolution ranked by relevance, price, trust, and availability.

ADP replaces these with a structured, intent-first discovery model.

## Core Principles

1. **Intent-first**: Requests are expressed as natural language intents, not query strings
2. **Structured constraints**: Price, region, latency, compliance filters are first-class citizens
3. **Explainable ranking**: Every result includes a score breakdown and human-readable explanation
4. **Federation-ready**: Discovery can span multiple ADP nodes
5. **Auditable**: Every discovery is logged for observability and compliance
6. **Open**: Apache 2.0 licensed, schema-first, language-agnostic

## Where ADP Fits

```
Agent / Application / Human
          │
          │  DiscoveryIntent (natural language + constraints)
          ▼
    ADP Protocol Layer
          │
    ┌─────┴──────────────────────────┐
    │  Registry  │  Matching  │ Rank │
    └─────┬──────────────────────────┘
          │
          │  DiscoveryResponse (ranked results + explanations)
          ▼
   Provider / Offering
```

## Supported Categories

| Category | Description |
|----------|-------------|
| `product` | Physical or digital products |
| `service` | Managed services, SaaS, B2B |
| `agent` | AI agents, LLM inference, fine-tuning |
| `data` | Data APIs, streams, datasets |
| `compute` | Cloud compute, GPU clusters, serverless |
| `api` | REST APIs, GraphQL, storage |
