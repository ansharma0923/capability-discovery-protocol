# CDP JSON Schemas

This directory contains the JSON Schema Draft 7 definitions for all CDP protocol data structures.

## Schema Files

| File | Title | Description |
|------|-------|-------------|
| `discovery_intent.json` | DiscoveryIntent | An intent-driven discovery request |
| `provider_descriptor.json` | ProviderDescriptor | A registered provider of offerings |
| `offering_descriptor.json` | OfferingDescriptor | A single product, service, agent, data, compute, or API offering |
| `discovery_candidate.json` | DiscoveryCandidate | A ranked result candidate with full score breakdown |
| `discovery_result.json` | DiscoveryResult | A single result item in a discovery response |
| `discovery_response.json` | DiscoveryResponse | Full API response from `/discover` |
| `federation_query.json` | FederationQuery | A federation query wrapping a DiscoveryIntent |
| `federation_response.json` | FederationResponse | A response from a remote federation node |
| `discovery_audit_record.json` | DiscoveryAuditRecord | An audit record for a pipeline execution |

## Schema Version

All schemas are at version `0.1.0` and use JSON Schema Draft 7 (`http://json-schema.org/draft-07/schema#`).

## Validation

To validate a document against a schema:

```python
import json
import jsonschema

with open("schema/discovery_intent.json") as f:
    schema = json.load(f)

with open("protocol-vectors/discovery_intent_v0.1.json") as f:
    instance = json.load(f)

jsonschema.validate(instance, schema)
```

Or use the test suite:

```bash
pytest tests/schema_validation/ -v
```
