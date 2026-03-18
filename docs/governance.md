# Governance

## Project Structure

ADP is an open protocol governed by its contributors under the Apache 2.0 license.

## Decision Making

- Protocol changes require a Protocol Change Proposal (PCP) via GitHub Issues
- Non-breaking changes can be merged with two approvals
- Breaking changes require a formal review period of 14 days
- Security fixes may be fast-tracked

## Protocol Versioning

- `MAJOR.MINOR.PATCH` versioning
- Breaking wire format changes increment MINOR
- Backward-compatible additions increment PATCH
- All messages include a `version` field for negotiation

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full contributing guide.

## Code of Conduct

See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).
