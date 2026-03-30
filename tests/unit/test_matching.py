"""Tests for semantic matching."""
import pytest

from cdp.intent.models import Category, DiscoveryIntent
from cdp.matching.semantic import rank_by_semantic, semantic_score
from cdp.registry.models import OfferingDescriptor


@pytest.fixture
def headphone_offering():
    return OfferingDescriptor(
        offering_id="off-match-001",
        provider_id="prov-001",
        name="ProANC Headphones",
        description="Premium noise-canceling headphones with bluetooth",
        category="product",
        tags=["headphones", "anc", "noise-canceling", "bluetooth"],
        capabilities=["anc", "bluetooth"],
        active=True,
    )


@pytest.fixture
def unrelated_offering():
    return OfferingDescriptor(
        offering_id="off-match-002",
        provider_id="prov-001",
        name="Office Chair",
        description="Ergonomic office chair with lumbar support",
        category="product",
        tags=["chair", "ergonomic", "office"],
        capabilities=["adjustable", "lumbar"],
        active=True,
    )


class TestSemanticScore:
    def test_high_score_for_matching_intent(self, headphone_offering):
        intent = DiscoveryIntent(
            intent_text="noise-canceling headphones bluetooth",
            category=Category.PRODUCT,
        )
        score = semantic_score(intent, headphone_offering)
        assert score > 0.5

    def test_low_score_for_unrelated(self, unrelated_offering):
        intent = DiscoveryIntent(
            intent_text="noise-canceling headphones bluetooth",
            category=Category.PRODUCT,
        )
        score = semantic_score(intent, unrelated_offering)
        assert score < 0.5

    def test_score_in_range(self, headphone_offering):
        intent = DiscoveryIntent(
            intent_text="anything at all",
            category=Category.PRODUCT,
        )
        score = semantic_score(intent, headphone_offering)
        assert 0.0 <= score <= 1.0

    def test_empty_keywords_returns_half(self, headphone_offering):
        # "a the for" are all stop words
        intent = DiscoveryIntent(
            intent_text="a the for",
            category=Category.PRODUCT,
        )
        score = semantic_score(intent, headphone_offering)
        assert score == 0.5

    def test_perfect_match(self, headphone_offering):
        intent = DiscoveryIntent(
            intent_text="headphones anc noise-canceling bluetooth",
            category=Category.PRODUCT,
        )
        score = semantic_score(intent, headphone_offering)
        assert score >= 0.8


class TestRankBySemantic:
    def test_returns_sorted_descending(self, headphone_offering, unrelated_offering):
        intent = DiscoveryIntent(
            intent_text="noise-canceling headphones bluetooth",
            category=Category.PRODUCT,
        )
        ranked = rank_by_semantic(intent, [unrelated_offering, headphone_offering])
        assert len(ranked) == 2
        assert ranked[0][1] >= ranked[1][1]
        assert ranked[0][0].offering_id == headphone_offering.offering_id

    def test_empty_list(self):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
        )
        ranked = rank_by_semantic(intent, [])
        assert ranked == []

    def test_returns_tuple_pairs(self, headphone_offering):
        intent = DiscoveryIntent(
            intent_text="headphones",
            category=Category.PRODUCT,
        )
        ranked = rank_by_semantic(intent, [headphone_offering])
        assert len(ranked) == 1
        offering, score = ranked[0]
        assert isinstance(score, float)
        assert offering.offering_id == headphone_offering.offering_id
