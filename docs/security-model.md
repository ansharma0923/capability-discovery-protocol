# Security Model

## Trust Levels

Providers are assigned a trust level that affects their ranking score:

| Level | Trust Score | Requirements |
|-------|-------------|--------------|
| unverified | 0.1 | Self-registered, no verification |
| basic | 0.4 | Basic identity verification |
| verified | 0.75 | Identity + compliance verification |
| certified | 1.0 | Full certification audit |

## Policy Engine

The default policy engine enforces:
1. **ActiveOnlyPolicy**: Inactive offerings are excluded
2. **VerifiedProviderPolicy**: Providers must be at `basic` trust level or above

Custom policies can be added by extending `PolicyRule`.

## API Security Recommendations

For production deployments:
- Add authentication middleware (API keys, JWT, mTLS)
- Rate-limit `/discover` endpoints
- Restrict registration endpoints to authorized clients
- Enable HTTPS/TLS

## Audit Logging

Every discovery execution generates a `DiscoveryAuditRecord` containing:
- Intent ID and text
- Pipeline stages and duration
- Number of candidates and results
- Top score
- Federation usage

Audit logs should be stored with appropriate retention policies.

## Input Validation

All inputs are validated via Pydantic v2 schemas before processing. Invalid inputs return HTTP 422 with detailed error messages.
