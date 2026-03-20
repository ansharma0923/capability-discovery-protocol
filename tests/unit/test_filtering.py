"""Tests for deterministic filtering."""
from adp.intent.models import Category, Constraints, DiscoveryIntent
from adp.matching.filter import apply_filters
from adp.registry.models import OfferingDescriptor


def make_offering(**kwargs) -> OfferingDescriptor:
    defaults = dict(
        offering_id="off-filter-001",
        provider_id="prov-001",
        name="Test Offering",
        description="A test offering",
        category="product",
        tags=[],
        price=100.0,
        region=["us-east"],
        availability=0.99,
        compliance=[],
        capabilities=[],
        active=True,
    )
    defaults.update(kwargs)
    return OfferingDescriptor(**defaults)


class TestCategoryFilter:
    def test_filters_correct_category(self):
        intent = DiscoveryIntent(intent_text="test", category=Category.PRODUCT)
        offerings = [
            make_offering(offering_id="p1", category="product"),
            make_offering(offering_id="s1", category="service"),
            make_offering(offering_id="a1", category="agent"),
        ]
        result = apply_filters(intent, offerings)
        assert len(result) == 1
        assert result[0].offering_id == "p1"

    def test_returns_empty_if_no_match(self):
        intent = DiscoveryIntent(intent_text="test", category=Category.AGENT)
        offerings = [make_offering(category="product")]
        result = apply_filters(intent, offerings)
        assert result == []


class TestPriceFilter:
    def test_filters_above_max_price(self):
        intent = DiscoveryIntent(
            intent_text="test",
            category=Category.PRODUCT,
            constraints=Constraints(max_price=200.0),
        )
        offerings = [
            make_offering(offering_id="cheap", price=100.0),
            make_offering(offering_id="exact", price=200.0),
            make_offering(offering_id="expensive", price=300.0),
        ]
        result = apply_filters(intent, offerings)
        ids = [o.offering_id for o in result]
        assert "cheap" in ids
        assert "exact" in ids
        assert "expensive" not in ids

    def test_no_price_constraint_passes_all(self):
        intent = DiscoveryIntent(intent_text="test", category=Category.PRODUCT)
        offerings = [
            make_offering(offering_id="p1", price=1000.0),
            make_offering(offering_id="p2", price=0.01),
        ]
        result = apply_filters(intent, offerings)
        assert len(result) == 2

    def test_none_price_offering_passes(self):
        intent = DiscoveryIntent(
            intent_text="test",
            category=Category.PRODUCT,
            constraints=Constraints(max_price=100.0),
        )
        offerings = [make_offering(price=None)]
        result = apply_filters(intent, offerings)
        assert len(result) == 1


class TestRegionFilter:
    def test_filters_outside_region(self):
        intent = DiscoveryIntent(
            intent_text="test",
            category=Category.PRODUCT,
            constraints=Constraints(region=["us-east"]),
        )
        offerings = [
            make_offering(offering_id="east", region=["us-east"]),
            make_offering(offering_id="west", region=["us-west"]),
            make_offering(offering_id="multi", region=["us-east", "eu-west"]),
        ]
        result = apply_filters(intent, offerings)
        ids = [o.offering_id for o in result]
        assert "east" in ids
        assert "multi" in ids
        assert "west" not in ids

    def test_empty_offering_region_passes(self):
        intent = DiscoveryIntent(
            intent_text="test",
            category=Category.PRODUCT,
            constraints=Constraints(region=["us-east"]),
        )
        offerings = [make_offering(region=[])]
        result = apply_filters(intent, offerings)
        assert len(result) == 1


class TestActiveFilter:
    def test_inactive_offerings_excluded(self):
        intent = DiscoveryIntent(intent_text="test", category=Category.PRODUCT)
        offerings = [
            make_offering(offering_id="active", active=True),
            make_offering(offering_id="inactive", active=False),
        ]
        result = apply_filters(intent, offerings)
        ids = [o.offering_id for o in result]
        assert "active" in ids
        assert "inactive" not in ids


class TestComplianceFilter:
    def test_filters_missing_compliance(self):
        intent = DiscoveryIntent(
            intent_text="test",
            category=Category.PRODUCT,
            constraints=Constraints(compliance=["SOC2", "HIPAA"]),
        )
        offerings = [
            make_offering(offering_id="full", compliance=["SOC2", "HIPAA", "ISO27001"]),
            make_offering(offering_id="partial", compliance=["SOC2"]),
            make_offering(offering_id="none", compliance=[]),
        ]
        result = apply_filters(intent, offerings)
        assert len(result) == 1
        assert result[0].offering_id == "full"


class TestAvailabilityFilter:
    def test_filters_below_min_availability(self):
        intent = DiscoveryIntent(
            intent_text="test",
            category=Category.PRODUCT,
            constraints=Constraints(availability_min=0.99),
        )
        offerings = [
            make_offering(offering_id="high", availability=0.999),
            make_offering(offering_id="exact", availability=0.99),
            make_offering(offering_id="low", availability=0.95),
        ]
        result = apply_filters(intent, offerings)
        ids = [o.offering_id for o in result]
        assert "high" in ids
        assert "exact" in ids
        assert "low" not in ids
