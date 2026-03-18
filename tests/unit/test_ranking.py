"""Tests for the ranking scorer."""
import pytest
from adp.intent.models import DiscoveryIntent, Category, Constraints, Preferences, RankingProfile
from adp.registry.models import OfferingDescriptor, ProviderDescriptor, TrustLevel
from adp.ranking.scorer import score_offering, rank_candidates, TRUST_SCORES
from adp.ranking.profiles import get_profile, PROFILES


@pytest.fixture
def provider():
    return ProviderDescriptor(
        provider_id="prov-001",
        name="Test Provider",
        description="A test provider",
        categories=["product"],
        regions=["us-east"],
        trust_level=TrustLevel.CERTIFIED,
        availability_score=0.999,
    )


@pytest.fixture
def offering():
    return OfferingDescriptor(
        offering_id="off-rank-001",
        provider_id="prov-001",
        name="ProANC Headphones",
        description="Premium noise-canceling headphones",
        category="product",
        tags=["headphones", "anc", "noise-canceling"],
        price=249.99,
        region=["us-east"],
        availability=0.99,
        compliance=["CE"],
        capabilities=["anc", "bluetooth"],
        active=True,
    )


@pytest.fixture
def intent():
    return DiscoveryIntent(
        intent_text="noise-canceling headphones for remote work",
        category=Category.PRODUCT,
        constraints=Constraints(max_price=300.0, region=["us-east"]),
        preferences=Preferences(ranking_profile=RankingProfile.DEFAULT),
    )


class TestScoreOffering:
    def test_score_in_range(self, intent, offering, provider):
        weights = get_profile("default")
        result = score_offering(intent, offering, provider, 0.8, weights)
        assert 0.0 <= result["total_score"] <= 1.0

    def test_score_has_breakdown(self, intent, offering, provider):
        weights = get_profile("default")
        result = score_offering(intent, offering, provider, 0.8, weights)
        breakdown = result["score_breakdown"]
        assert "relevance" in breakdown
        assert "price" in breakdown
        assert "latency" in breakdown
        assert "availability" in breakdown
        assert "trust" in breakdown
        assert "freshness" in breakdown

    def test_score_has_explanation(self, intent, offering, provider):
        weights = get_profile("default")
        result = score_offering(intent, offering, provider, 0.8, weights)
        explanation = result["explanation"]
        assert "summary" in explanation
        assert "matched_constraints" in explanation

    def test_certified_provider_higher_trust(self, intent, offering):
        weights = get_profile("default")
        certified_provider = ProviderDescriptor(
            provider_id="prov-cert",
            name="Certified",
            description="Certified provider",
            categories=["product"],
            regions=["us-east"],
            trust_level=TrustLevel.CERTIFIED,
        )
        unverified_provider = ProviderDescriptor(
            provider_id="prov-unverified",
            name="Unverified",
            description="Unverified provider",
            categories=["product"],
            regions=["us-east"],
            trust_level=TrustLevel.UNVERIFIED,
        )
        cert_result = score_offering(intent, offering, certified_provider, 0.8, weights)
        unverified_result = score_offering(intent, offering, unverified_provider, 0.8, weights)
        assert cert_result["total_score"] > unverified_result["total_score"]

    def test_price_within_budget(self, intent, offering, provider):
        weights = get_profile("default")
        result = score_offering(intent, offering, provider, 0.8, weights)
        assert result["explanation"]["price_fit"].startswith("Price")
        assert "matched_constraints" in result["explanation"]
        constraints = result["explanation"]["matched_constraints"]
        assert any("price" in c for c in constraints)

    def test_no_provider_lowers_score(self, intent, offering):
        weights = get_profile("default")
        with_provider = ProviderDescriptor(
            provider_id="prov-001",
            name="Prov",
            description="desc",
            categories=["product"],
            regions=["us-east"],
            trust_level=TrustLevel.CERTIFIED,
        )
        result_with = score_offering(intent, offering, with_provider, 0.8, weights)
        result_without = score_offering(intent, offering, None, 0.8, weights)
        assert result_with["total_score"] >= result_without["total_score"]


class TestRankCandidates:
    def test_returns_sorted_descending(self, intent, offering, provider):
        offering2 = OfferingDescriptor(
            offering_id="off-rank-002",
            provider_id="prov-001",
            name="Budget Headphones",
            description="Basic headphones",
            category="product",
            tags=["headphones"],
            price=49.99,
            region=["us-east"],
            availability=0.95,
            active=True,
        )
        providers = {"prov-001": provider}
        ranked = rank_candidates(intent, [(offering, 0.9), (offering2, 0.3)], providers)
        assert len(ranked) == 2
        assert ranked[0]["total_score"] >= ranked[1]["total_score"]

    def test_empty_offerings(self, intent):
        ranked = rank_candidates(intent, [], {})
        assert ranked == []


class TestProfiles:
    def test_all_profiles_exist(self):
        for profile_name in ["default", "cost_optimized", "latency_optimized", "trust_optimized"]:
            profile = get_profile(profile_name)
            assert profile is not None

    def test_cost_optimized_has_higher_price_weight(self):
        default = get_profile("default")
        cost = get_profile("cost_optimized")
        assert cost.price > default.price

    def test_latency_optimized_has_higher_latency_weight(self):
        default = get_profile("default")
        latency = get_profile("latency_optimized")
        assert latency.latency > default.latency

    def test_trust_optimized_has_higher_trust_weight(self):
        default = get_profile("default")
        trust = get_profile("trust_optimized")
        assert trust.trust > default.trust

    def test_unknown_profile_returns_default(self):
        profile = get_profile("nonexistent_profile")
        default = get_profile("default")
        assert profile.relevance == default.relevance
