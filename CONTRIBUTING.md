# Contributing to Agent Discovery Protocol

Thank you for your interest in contributing to ADP! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) to file issues. Include:
- ADP version, Python version, and OS
- Steps to reproduce
- Expected vs actual behavior

### Requesting Features

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md). Describe:
- The use case and problem you're solving
- Your proposed solution
- Alternatives you've considered

### Protocol Changes

Protocol changes require a [Protocol Change Proposal](.github/ISSUE_TEMPLATE/protocol_change.md) with:
- Motivation and rationale
- Wire format changes
- Backward compatibility analysis
- Reference implementation

## Development Setup

### Prerequisites

- Python 3.11+
- Git

### Setup

```bash
git clone https://github.com/ansharma0923/agent-discovery-protocol.git
cd agent-discovery-protocol
pip install -e ".[dev]"
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test suite
pytest tests/unit/ -v
pytest tests/functional/ -v
pytest tests/schema_validation/ -v
pytest tests/protocol_vectors/ -v
pytest tests/interoperability/ -v
```

### Running the Server

```bash
uvicorn adp.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Style

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check adp/ tests/
ruff format adp/ tests/
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes with tests
4. Ensure all tests pass: `pytest tests/ -v`
5. Run linting: `ruff check adp/ tests/`
6. Submit a PR using the [PR template](.github/PULL_REQUEST_TEMPLATE.md)

## Coding Standards

- Follow PEP 8 and use type annotations
- Write docstrings for public APIs
- Add tests for new functionality
- Keep functions small and focused
- Use Pydantic models for data validation

## Commit Messages

Use clear, imperative commit messages:
- `Add semantic matching for agent category`
- `Fix TTL expiry in registry store`
- `Update ranking profile weights`

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.
