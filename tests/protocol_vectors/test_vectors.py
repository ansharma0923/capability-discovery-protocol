"""Tests for protocol vector validation."""
import json
from pathlib import Path

import jsonschema

SCHEMA_DIR = Path(__file__).parent.parent.parent / "schema"
VECTORS_DIR = Path(__file__).parent.parent.parent / "protocol-vectors"


def load_schema(name: str) -> dict:
    with open(SCHEMA_DIR / name) as f:
        return json.load(f)


def load_vector(name: str) -> dict:
    with open(VECTORS_DIR / name) as f:
        return json.load(f)


class TestProtocolVectors:
    def test_all_vector_files_exist(self):
        expected = [
            "discovery_intent_v0.1.json",
            "provider_descriptor_v0.1.json",
            "offering_descriptor_v0.1.json",
            "discovery_result_v0.1.json",
            "federation_query_v0.1.json",
            "discovery_response_v0.1.json",
            "federation_response_v0.1.json",
            "discovery_audit_record_v0.1.json",
            "discovery_intent_service_v0.1.json",
            "discovery_intent_agent_v0.1.json",
        ]
        for name in expected:
            assert (VECTORS_DIR / name).exists(), f"Vector file missing: {name}"

    def test_discovery_intent_vector_is_valid_json(self):
        vector = load_vector("discovery_intent_v0.1.json")
        assert isinstance(vector, dict)

    def test_provider_descriptor_vector_is_valid_json(self):
        vector = load_vector("provider_descriptor_v0.1.json")
        assert isinstance(vector, dict)

    def test_offering_descriptor_vector_is_valid_json(self):
        vector = load_vector("offering_descriptor_v0.1.json")
        assert isinstance(vector, dict)

    def test_discovery_result_vector_is_valid_json(self):
        vector = load_vector("discovery_result_v0.1.json")
        assert isinstance(vector, dict)

    def test_federation_query_vector_is_valid_json(self):
        vector = load_vector("federation_query_v0.1.json")
        assert isinstance(vector, dict)

    def test_discovery_response_vector_is_valid_json(self):
        vector = load_vector("discovery_response_v0.1.json")
        assert isinstance(vector, dict)

    def test_federation_response_vector_is_valid_json(self):
        vector = load_vector("federation_response_v0.1.json")
        assert isinstance(vector, dict)

    def test_discovery_audit_record_vector_is_valid_json(self):
        vector = load_vector("discovery_audit_record_v0.1.json")
        assert isinstance(vector, dict)

    def test_service_intent_vector_is_valid_json(self):
        vector = load_vector("discovery_intent_service_v0.1.json")
        assert isinstance(vector, dict)

    def test_agent_intent_vector_is_valid_json(self):
        vector = load_vector("discovery_intent_agent_v0.1.json")
        assert isinstance(vector, dict)


class TestVectorSchemaConformance:
    def test_discovery_intent_vector_validates(self):
        schema = load_schema("discovery_intent.json")
        vector = load_vector("discovery_intent_v0.1.json")
        jsonschema.validate(vector, schema)

    def test_provider_descriptor_vector_validates(self):
        schema = load_schema("provider_descriptor.json")
        vector = load_vector("provider_descriptor_v0.1.json")
        jsonschema.validate(vector, schema)

    def test_offering_descriptor_vector_validates(self):
        schema = load_schema("offering_descriptor.json")
        vector = load_vector("offering_descriptor_v0.1.json")
        jsonschema.validate(vector, schema)

    def test_discovery_result_vector_validates(self):
        schema = load_schema("discovery_result.json")
        vector = load_vector("discovery_result_v0.1.json")
        jsonschema.validate(vector, schema)

    def test_discovery_audit_record_vector_validates(self):
        schema = load_schema("discovery_audit_record.json")
        vector = load_vector("discovery_audit_record_v0.1.json")
        jsonschema.validate(vector, schema)

    def test_service_intent_vector_validates(self):
        schema = load_schema("discovery_intent.json")
        vector = load_vector("discovery_intent_service_v0.1.json")
        jsonschema.validate(vector, schema)

    def test_agent_intent_vector_validates(self):
        schema = load_schema("discovery_intent.json")
        vector = load_vector("discovery_intent_agent_v0.1.json")
        jsonschema.validate(vector, schema)


class TestVectorFieldValues:
    def test_intent_vector_has_correct_category(self):
        vector = load_vector("discovery_intent_v0.1.json")
        assert vector["category"] == "product"

    def test_intent_vector_has_constraints(self):
        vector = load_vector("discovery_intent_v0.1.json")
        assert "constraints" in vector
        assert vector["constraints"]["max_price"] == 300.0

    def test_provider_vector_has_trust_level(self):
        vector = load_vector("provider_descriptor_v0.1.json")
        assert "trust_level" in vector
        assert vector["trust_level"] in ["unverified", "basic", "verified", "certified"]

    def test_offering_vector_has_pricing(self):
        vector = load_vector("offering_descriptor_v0.1.json")
        assert "price" in vector
        assert vector["price"] > 0

    def test_result_vector_has_score(self):
        vector = load_vector("discovery_result_v0.1.json")
        assert "total_score" in vector
        assert 0.0 <= vector["total_score"] <= 1.0

    def test_result_vector_has_score_breakdown(self):
        vector = load_vector("discovery_result_v0.1.json")
        assert "score_breakdown" in vector
        breakdown = vector["score_breakdown"]
        for key in ["relevance", "price", "latency", "availability", "trust", "freshness"]:
            assert key in breakdown

    def test_federation_query_has_intent(self):
        vector = load_vector("federation_query_v0.1.json")
        assert "intent" in vector
        assert "source_node" in vector
        assert "federation_id" in vector

    def test_discovery_response_vector_has_pipeline(self):
        vector = load_vector("discovery_response_v0.1.json")
        assert "pipeline" in vector
        assert "stages_executed" in vector["pipeline"]
        assert vector["pipeline"]["federation_used"] is False

    def test_federation_response_vector_has_responding_node(self):
        vector = load_vector("federation_response_v0.1.json")
        assert "responding_node" in vector
        assert "results" in vector
        assert vector["total_results"] >= 0

    def test_audit_record_vector_has_pipeline_stages(self):
        vector = load_vector("discovery_audit_record_v0.1.json")
        assert "pipeline_stages" in vector
        assert len(vector["pipeline_stages"]) > 0
        assert "duration_ms" in vector

    def test_service_intent_has_correct_category(self):
        vector = load_vector("discovery_intent_service_v0.1.json")
        assert vector["category"] == "service"
        assert "compliance" in vector["constraints"]

    def test_agent_intent_has_correct_category(self):
        vector = load_vector("discovery_intent_agent_v0.1.json")
        assert vector["category"] == "agent"
        assert "max_latency_ms" in vector["constraints"]


class TestVectorParsability:
    """Test that vectors can be parsed by CDP Python models."""

    def test_intent_vector_parseable_by_model(self):
        from adp.intent.models import DiscoveryIntent
        vector = load_vector("discovery_intent_v0.1.json")
        intent = DiscoveryIntent(**vector)
        assert intent.category.value == "product"
        assert intent.constraints.max_price == 300.0

    def test_provider_vector_parseable_by_model(self):
        from adp.registry.models import ProviderDescriptor
        vector = load_vector("provider_descriptor_v0.1.json")
        provider = ProviderDescriptor(**vector)
        assert provider.trust_level.value == "verified"

    def test_offering_vector_parseable_by_model(self):
        from adp.registry.models import OfferingDescriptor
        vector = load_vector("offering_descriptor_v0.1.json")
        offering = OfferingDescriptor(**vector)
        assert offering.category == "product"
        assert offering.active is True

    def test_service_intent_vector_parseable_by_model(self):
        from adp.intent.models import DiscoveryIntent
        vector = load_vector("discovery_intent_service_v0.1.json")
        intent = DiscoveryIntent(**vector)
        assert intent.category.value == "service"
        assert "SOC2" in intent.constraints.compliance

    def test_agent_intent_vector_parseable_by_model(self):
        from adp.intent.models import DiscoveryIntent
        vector = load_vector("discovery_intent_agent_v0.1.json")
        intent = DiscoveryIntent(**vector)
        assert intent.category.value == "agent"
        assert intent.constraints.max_latency_ms == 300
