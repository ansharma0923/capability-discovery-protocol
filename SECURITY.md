# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

To report a security vulnerability, please email the maintainers directly or use GitHub's private security advisory feature.

### What to Include

- Type of issue (e.g., injection, authentication bypass, data exposure)
- Full paths of affected source files
- Location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce
- Proof-of-concept or exploit code (if possible)
- Impact assessment

### Response Timeline

| Milestone | Timeline |
|-----------|----------|
| Initial acknowledgment | 48 hours |
| Issue confirmation | 7 days |
| Fix development | 30 days |
| Public disclosure | After fix is released |

## Security Considerations for ADP Deployments

### Registry Access

- The default registry is in-memory with no authentication. Production deployments should add authentication middleware.
- Restrict `/register/provider` and `/register/offering` endpoints to authorized clients.

### Federation

- Validate the identity of federation nodes before enabling federation.
- Use TLS for all federation connections.
- Set appropriate `ttl_hops` limits to prevent federation loops.

### Data Privacy

- Discovery intents may contain sensitive information. Implement audit log retention policies.
- Do not log full intent text in production without appropriate access controls.

### Input Validation

- All inputs are validated via Pydantic schemas.
- Implement rate limiting on `/discover` endpoints in production.
