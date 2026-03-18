# ADP Overview

## What is Agent Discovery Protocol?

The Agent Discovery Protocol (ADP) is an open protocol for **intent-driven discovery** of agents, services, products, data, compute resources, and APIs. It enables AI agents, applications, and humans to find the right provider for any capability using natural language.

## The Problem

As the number of AI agents, microservices, and digital products grows, discovering the right one becomes increasingly difficult. Traditional approaches rely on:
- Static catalogs that require exact keyword matching
- Search engines that return pages of irrelevant results
- Manual API documentation browsing

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
