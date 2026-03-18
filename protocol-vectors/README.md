# ADP Protocol Vectors

Protocol vectors are canonical test fixtures that validate ADP implementations for correctness and interoperability.

## What Are Protocol Vectors?

Protocol vectors are reference JSON documents that serve as ground-truth examples of valid ADP messages. Any conformant implementation MUST accept these vectors without errors.

## Vector Files

| File | Schema | Description |
|------|--------|-------------|
| `discovery_intent_v0.1.json` | `schema/discovery_intent.json` | A product discovery intent |
| `provider_descriptor_v0.1.json` | `schema/provider_descriptor.json` | A provider registration |
| `offering_descriptor_v0.1.json` | `schema/offering_descriptor.json` | A product offering |
| `discovery_result_v0.1.json` | `schema/discovery_result.json` | A ranked discovery result |
| `federation_query_v0.1.json` | `schema/federation_query.json` | A federation query |

## Running Validation

```bash
pytest tests/protocol_vectors/ -v
```

## Adding New Vectors

1. Create a new JSON file following the naming convention `<type>_v<version>.json`
2. Validate it against the corresponding schema
3. Add a test case in `tests/protocol_vectors/test_vectors.py`

## Versioning

Vectors are versioned with the protocol version. Breaking changes require a new vector file.
