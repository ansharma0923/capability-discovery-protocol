#!/usr/bin/env bash
# CDP curl examples - assumes server running on localhost:8000

BASE_URL="http://localhost:8000"

echo "=== CDP curl Examples ==="
echo ""

# Health check
echo "--- Health Check ---"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""

# Register a provider
echo "--- Register Provider ---"
curl -s -X POST "$BASE_URL/register/provider" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo Provider",
    "description": "A demo provider for curl examples",
    "categories": ["product"],
    "regions": ["us-east"],
    "trust_level": "verified"
  }' | python3 -m json.tool
echo ""

# Discover products
echo "--- Discover Products ---"
curl -s -X POST "$BASE_URL/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "intent_text": "I need noise-canceling headphones under $300",
    "category": "product",
    "constraints": {
      "max_price": 300.0,
      "region": ["us-east"]
    },
    "preferences": {
      "ranking_profile": "default",
      "max_results": 5
    }
  }' | python3 -m json.tool
echo ""

# Discover compute resources
echo "--- Discover Compute ---"
curl -s -X POST "$BASE_URL/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "intent_text": "I need GPU compute for machine learning training",
    "category": "compute",
    "constraints": {
      "max_latency_ms": 100
    },
    "preferences": {
      "ranking_profile": "latency_optimized"
    }
  }' | python3 -m json.tool
echo ""

# Discover agents
echo "--- Discover Agents ---"
curl -s -X POST "$BASE_URL/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "intent_text": "I need an LLM inference API with large context window",
    "category": "agent",
    "preferences": {
      "ranking_profile": "trust_optimized",
      "max_results": 3
    }
  }' | python3 -m json.tool
echo ""
