# Quickstart

Get up and running with the Capability Discovery Protocol (CDP) in under 5 minutes.

## Prerequisites

- Python 3.11 or 3.12
- `pip`

## 1. Clone the Repository

```bash
git clone https://github.com/ansharma0923/agent-discovery-protocol.git
cd agent-discovery-protocol
```

## 2. Install Dependencies

```bash
pip install -e ".[dev]"
```

This installs the `adp` package in editable mode along with all development dependencies (pytest, ruff, jsonschema).

## 3. Run the Tests

```bash
make test
```

You should see all tests pass:

```
============================= 127 passed in 2.5s ==============================
```

## 4. Start the API Server

```bash
make run-api
```

The REST API is now available at `http://localhost:8000`.

## 5. Register a Provider

```bash
curl -X POST http://localhost:8000/register/provider \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Provider",
    "description": "Demo provider",
    "categories": ["product"],
    "regions": ["us-east"]
  }'
```

## 6. Register an Offering

```bash
curl -X POST http://localhost:8000/register/offering \
  -H "Content-Type: application/json" \
  -d '{
    "provider_id": "<PROVIDER_ID>",
    "name": "Pro ANC Headphones",
    "description": "Professional noise-canceling headphones",
    "category": "product",
    "price": 249.99,
    "region": ["us-east"],
    "active": true
  }'
```

Replace `<PROVIDER_ID>` with the `provider_id` returned in step 5.

## 7. Discover an Offering

```bash
curl -X POST http://localhost:8000/discover \
  -H "Content-Type: application/json" \
  -d '{
    "intent_text": "I need noise-canceling headphones under $300",
    "category": "product",
    "constraints": {"max_price": 300.0, "region": ["us-east"]}
  }'
```

## 8. Run the Examples

Self-contained Python demos — no running server needed:

```bash
make run-examples
```

Or run individual examples:

```bash
python examples/product_discovery.py
python examples/service_discovery.py
python examples/agent_discovery.py
python examples/federation_demo.py
python examples/policy_demo.py
```

## 9. Validate Schemas and Protocol Vectors

```bash
make validate-schema
```

## Next Steps

- Read [docs/examples-walkthrough.md](examples-walkthrough.md) for a deep dive into each example
- Read [docs/python-sdk.md](python-sdk.md) to use CDP as a Python library
- Read [docs/architecture.md](architecture.md) for the full system design
- Read [docs/adp-wire-spec-v0.1.md](adp-wire-spec-v0.1.md) for the wire protocol spec
