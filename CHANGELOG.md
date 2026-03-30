# Changelog

All notable changes to Agent Discovery Protocol will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2024-01-15

Initial public release of the Agent Discovery Protocol reference implementation.

### Added

#### Protocol
- `DiscoveryIntent` schema with 6 categories: `product`, `service`, `agent`, `data`, `compute`, `api`
- `ProviderDescriptor` and `OfferingDescriptor` schemas
- 14-stage discovery pipeline: parse → normalize → extract constraints → retrieve candidates → deterministic filter → semantic matching → capability validation → policy filtering → ranking → explanation generation → federation merge → deduplication → audit logging → response generation
- 4 ranking profiles: `default`, `cost_optimized`, `latency_optimized`, `trust_optimized`
- Federation support for distributed ADP node queries
- Policy engine with trust-level enforcement

#### Reference Implementation (Python 3.11+)
- FastAPI server with `/discover`, `/register/provider`, `/register/offering`, `/health` endpoints
- In-memory registry with TTL-based expiry
- Keyword-based semantic matching
- Weighted scoring with per-field explainability
- Audit logging via `DiscoveryAuditRecord`

#### Schema & Vectors
- 9 JSON Schema Draft 7 definitions in `schema/`
- 10 canonical protocol vectors in `protocol-vectors/`

#### Tests
- Unit, functional, schema validation, protocol vector, and interoperability test suites

#### Documentation
- Architecture overview, wire spec, discovery model, federation model, ranking model, security model
- Quickstart guide and example walkthroughs

### Known Limitations

- Semantic matching is keyword-based (no vector embeddings in v0.1)
- Registry is in-memory only (no persistence layer)
- No built-in authentication (must be added at deployment)

---

[0.1.0]: https://github.com/ansharma0923/agent-discovery-protocol/releases/tag/v0.1.0
