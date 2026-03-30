# CDP Wire Specification v0.1

## Overview

This document defines the wire format for CDP v0.1.0 messages.

## Transport

- **Protocol**: HTTP/1.1 or HTTP/2
- **Encoding**: JSON (application/json)
- **Method**: POST for mutations, GET for reads

## Endpoints

### POST /discover

Execute a discovery pipeline.

**Request**: `DiscoveryIntent`

```json
{
  "intent_id": "550e8400-e29b-41d4-a716-446655440000",
  "version": "0.1.0",
  "intent_text": "I need noise-canceling headphones under $300",
  "category": "product",
  "constraints": {
    "max_price": 300.0,
    "currency": "USD",
    "region": ["us-east"],
    "max_latency_ms": null,
    "delivery_days": 5,
    "compliance": null,
    "availability_min": null
  },
  "preferences": {
    "ranking_profile": "default",
    "max_results": 10,
    "include_federation": false
  },
  "metadata": {},
  "created_at": "2024-01-15T10:00:00Z"
}
```

**Response**: `DiscoveryResponse`

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
        "relevance": 0.27,
        "price": 0.15,
        "latency": 0.15,
        "availability": 0.149,
        "trust": 0.15,
        "freshness": 0.05
      },
      "explanation": {
        "matched_constraints": ["price <= $300.0"],
        "relevance_reason": "Semantic match score: 0.90",
        "price_fit": "Price $249.99 vs budget $300.0",
        "latency_fit": "No latency constraint",
        "trust_reason": "Provider trust level: certified",
        "summary": "Offering 'ProANC Headphones X1' scored 0.85"
      },
      "_source": "local"
    }
  ],
  "pipeline": {
    "stages_executed": ["parse_request", "normalize_intent", "...", "response_generation"],
    "duration_ms": 2.4,
    "federation_used": false
  },
  "generated_at": "2024-01-15T10:00:00.123Z"
}
```

### POST /register/provider

Register a new provider.

**Request**: `ProviderDescriptor` (partial — `provider_id`, `registered_at`, `updated_at` are auto-generated)

**Response**:
```json
{
  "status": "registered",
  "provider_id": "11111111-1111-1111-1111-111111111111",
  "version": "0.1.0",
  "registered_at": "2024-01-15T10:00:00Z"
}
```

### POST /register/offering

Register a new offering. The `provider_id` must reference a registered provider.

**Response**:
```json
{
  "status": "registered",
  "offering_id": "off-elec-001",
  "provider_id": "11111111-1111-1111-1111-111111111111",
  "version": "0.1.0",
  "registered_at": "2024-01-15T10:00:00Z"
}
```

### GET /health

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "protocol": "CDP",
  "registry": {
    "providers": 5,
    "offerings": 15
  },
  "timestamp": "2024-01-15T10:00:00Z"
}
```

## Categories

Valid values for `category`: `product`, `service`, `agent`, `data`, `compute`, `api`

## Ranking Profiles

| Profile | Description |
|---------|-------------|
| `default` | Balanced weights across all dimensions |
| `cost_optimized` | Maximizes price score (weight: 0.40) |
| `latency_optimized` | Maximizes latency score (weight: 0.40) |
| `trust_optimized` | Maximizes trust score (weight: 0.35) |

## Trust Levels

| Level | Score |
|-------|-------|
| `unverified` | 0.1 |
| `basic` | 0.4 |
| `verified` | 0.75 |
| `certified` | 1.0 |

## Error Responses

```json
{"detail": "Provider 'xyz' not found"}
```

HTTP status codes: 200 OK, 404 Not Found, 422 Unprocessable Entity
