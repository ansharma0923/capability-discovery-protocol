.PHONY: install test run-api lint format clean validate-schema run-examples ci

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

run-api:
	uvicorn adp.main:app --reload --host 0.0.0.0 --port 8000

lint:
	ruff check adp/ tests/ examples/

format:
	ruff format adp/ tests/ examples/

validate-schema:
	pytest tests/schema_validation/ tests/protocol_vectors/ -v

run-examples:
	python examples/product_discovery.py
	python examples/service_discovery.py
	python examples/agent_discovery.py
	python examples/federation_demo.py
	python examples/policy_demo.py

ci: install lint test validate-schema

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ .ruff_cache/ dist/ build/ *.egg-info/
