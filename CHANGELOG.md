# Changelog

All notable changes to the Capability Discovery Protocol (CDP) will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Naming note:** This project was originally released as ADP (Agent Discovery Protocol). It was later renamed CFP (Capability Fabric Protocol) during capability-centric evolution, and is now called CDP (Capability Discovery Protocol).

---

## [0.1.1] — 2026-03-30

### Changed
- Finalized rename from ADP/CFP to CDP (Capability Discovery Protocol)
- Standardized naming across repository (README, docs, schemas, examples)
- Updated project positioning to capability-centric discovery
- Added and refined architecture diagrams (indexed, federated, hybrid, agent-less flows)
- Expanded documentation for agent-less execution mode
- Clarified Provider → Skill → Offering model across docs and examples

### Fixed
- Corrected Makefile and tooling references after package rename (adp → cdp)
- Updated lint, format, and validation commands to use cdp/
- Ensured CI workflow uses correct paths
- Removed stale references to adp/ in code and documentation

### Documentation
- Updated README to reflect CDP naming and positioning
- Added docs/no-agent-mode.md
- Renamed docs/adp-context.md → docs/cdp-context.md
- Improved protocol overview and architecture sections
- Added clear explanation of CDP vs ADP vs CFP evolution

### Notes
- This is a stabilization and consistency release after the CDP transition
- No functional breaking changes to discovery behavior
- Python package now uses `cdp` instead of `adp`

---

## [0.1.0] — 2024-01-15

Initial public release of the Capability Discovery Protocol reference implementation.

### Added

#### Protocol
- `DiscoveryIntent` schema with 6 categories: `product`, `service`, `agent`, `data`, `compute`, `api`
- `ProviderDescriptor` and `OfferingDescriptor` schemas
- 14-stage discovery pipeline: parse → normalize → extract constraints → retrieve candidates → deterministic filter → semantic matching → capability validation → policy filtering → ranking → explanation generation → federation merge → deduplication → audit logging → response generation
- 4 ranking profiles: `default`, `cost_optimized`, `latency_optimized`, `trust_optimized`
- Federation support for distributed CDP node queries
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

[0.1.1]: https://github.com/ansharma0923/capability-discovery-protocol/releases/tag/v0.1.1
[0.1.0]: https://github.com/ansharma0923/agent-discovery-protocol/releases/tag/v0.1.0
