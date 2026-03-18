"""Tests for JSON schema validation."""
import json
from pathlib import Path
import pytest
import jsonschema

SCHEMA_DIR = Path(__file__).parent.parent.parent / "schema"
VECTORS_DIR = Path(__file__).parent.parent.parent / "protocol-vectors"


def load_schema(name: str) -> dict:
    with open(SCHEMA_DIR / name) as f:
        return json.load(f)


def load_vector(name: str) -> dict:
    with open(VECTORS_DIR / name) as f:
        return json.load(f)


class TestSchemaFiles:
    def test_all_schema_files_exist(self):
        expected = [
            "discovery_intent.json",
            "provider_descriptor.json",
            "offering_descriptor.json",
            "discovery_candidate.json",
            "discovery_result.json",
            "discovery_response.json",
            "federation_query.json",
            "federation_response.json",
            "discovery_audit_record.json",
        ]
        for name in expected:
            assert (SCHEMA_DIR / name).exists(), f"Schema file missing: {name}"

    def test_schemas_have_required_fields(self):
        for schema_file in SCHEMA_DIR.glob("*.json"):
            with open(schema_file) as f:
                schema = json.load(f)
            assert "$schema" in schema, f"Missing $schema in {schema_file.name}"
            assert "title" in schema, f"Missing title in {schema_file.name}"
            assert "type" in schema, f"Missing type in {schema_file.name}"

    def test_schemas_are_valid_json(self):
        for schema_file in SCHEMA_DIR.glob("*.json"):
            with open(schema_file) as f:
                try:
                    json.load(f)
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in {schema_file.name}: {e}")


class TestDiscoveryIntentSchema:
    def test_valid_intent_validates(self):
        schema = load_schema("discovery_intent.json")
        instance = load_vector("discovery_intent_v0.1.json")
        jsonschema.validate(instance, schema)

    def test_missing_required_field_fails(self):
        schema = load_schema("discovery_intent.json")
        instance = {
            "version": "0.1.0",
            "category": "product",
            "created_at": "2024-01-15T10:00:00Z",
            # missing intent_id and intent_text
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance, schema)

    def test_invalid_category_fails(self):
        schema = load_schema("discovery_intent.json")
        instance = {
            "intent_id": "test-id",
            "version": "0.1.0",
            "intent_text": "test",
            "category": "invalid_category",
            "created_at": "2024-01-15T10:00:00Z",
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance, schema)


class TestProviderDescriptorSchema:
    def test_valid_provider_validates(self):
        schema = load_schema("provider_descriptor.json")
        instance = load_vector("provider_descriptor_v0.1.json")
        jsonschema.validate(instance, schema)

    def test_empty_categories_fails(self):
        schema = load_schema("provider_descriptor.json")
        instance = {
            "provider_id": "test",
            "version": "0.1.0",
            "name": "Test",
            "description": "Test provider",
            "categories": [],  # minItems: 1
            "regions": ["us-east"],
            "registered_at": "2024-01-15T10:00:00Z",
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance, schema)


class TestOfferingDescriptorSchema:
    def test_valid_offering_validates(self):
        schema = load_schema("offering_descriptor.json")
        instance = load_vector("offering_descriptor_v0.1.json")
        jsonschema.validate(instance, schema)


class TestDiscoveryResultSchema:
    def test_valid_result_validates(self):
        schema = load_schema("discovery_result.json")
        instance = load_vector("discovery_result_v0.1.json")
        jsonschema.validate(instance, schema)


class TestAuditRecordSchema:
    def test_schema_loads(self):
        schema = load_schema("discovery_audit_record.json")
        assert schema["title"] == "DiscoveryAuditRecord"

    def test_valid_audit_record_validates(self):
        schema = load_schema("discovery_audit_record.json")
        instance = {
            "audit_id": "audit-001",
            "version": "0.1.0",
            "intent_id": "intent-001",
            "intent_text": "find headphones",
            "category": "product",
            "candidates_found": 5,
            "results_returned": 3,
            "pipeline_stages": ["parse_request", "response_generation"],
            "top_score": 0.85,
            "federation_used": False,
            "duration_ms": 12.5,
            "metadata": {},
            "recorded_at": "2024-01-15T10:00:00Z",
        }
        jsonschema.validate(instance, schema)
