# Known Limitations — CDP v0.1.0

This document describes the known limitations and design constraints of the v0.1.0 reference implementation. These are deliberate trade-offs for an early release and will be addressed in future versions.

---

## Semantic Matching

**Limitation:** Semantic matching is keyword-based, not embedding-based.

The current implementation extracts keywords from the intent text and matches them against provider and offering metadata using simple string overlap. It does not use vector embeddings or a language model.

**Impact:** Results may be less precise for intents expressed in varied natural language. Synonyms and paraphrases that share no keywords with provider metadata will not match.

**Planned:** Vector-embedding-based matching in a future minor version.

---

## Registry Persistence

**Limitation:** The registry is in-memory only. All registered providers and offerings are lost when the server restarts.

**Impact:** Not suitable for production use without adding a persistence layer.

**Planned:** Pluggable storage backends (e.g., Redis, PostgreSQL) are planned for v0.2.

---

## Authentication and Authorization

**Limitation:** The reference server has no built-in authentication. All endpoints (`/discover`, `/register/provider`, `/register/offering`) are open.

**Impact:** The server must not be exposed to the public internet without adding authentication middleware.

**Guidance:** See `SECURITY.md` for deployment recommendations.

---

## Federation

**Limitation:** Federation uses a simple HTTP fan-out with no node authentication, no loop detection beyond `ttl_hops`, and no result deduplication across deeply nested federation graphs.

**Impact:** Federation is suitable for controlled environments and demos. Production federation deployments should add node identity verification.

---

## Ranking

**Limitation:** Ranking weights are static profiles. There is no per-caller or per-intent dynamic weight adjustment.

**Impact:** Callers can select a profile (`default`, `cost_optimized`, `latency_optimized`, `trust_optimized`) but cannot specify arbitrary weights.

---

## Protocol Stability

**Limitation:** The v0.1 wire format and schema are not yet stable. Field names, types, and semantics may change before v1.0.

**Impact:** Implementations built against v0.1 should treat the protocol as experimental. Breaking changes will be noted in `CHANGELOG.md`.

---

## SDK Coverage

**Limitation:** Only a Python reference implementation exists. The Go SDK stub in `sdk/go/` is a placeholder with no implementation.

**Planned:** Community contributions for Go, TypeScript, and other SDKs are welcome.

---

## Scale

**Limitation:** The reference implementation is not benchmarked or optimized for high throughput. It is intended as a protocol reference, not a production-grade service.

**Planned:** Performance profiling and optimization are planned after the protocol stabilizes.
