"""Intent parsing and normalization."""
from typing import List
from .models import DiscoveryIntent


def normalize_intent(intent: DiscoveryIntent) -> DiscoveryIntent:
    """Normalize intent text and extract structured constraints."""
    normalized_text = intent.intent_text.strip()
    return intent.model_copy(update={"intent_text": normalized_text})


def extract_keywords(intent: DiscoveryIntent) -> List[str]:
    """Extract keywords from intent text for semantic matching."""
    text = intent.intent_text.lower()
    stop_words = {
        "a", "an", "the", "for", "with", "and", "or", "in", "of", "to",
        "that", "i", "need", "want", "find", "get", "me", "some", "any",
        "is", "are", "be", "my", "under", "over", "between",
    }
    words = [w.strip(".,!?;:\"'") for w in text.split()]
    return [w for w in words if w and w not in stop_words and len(w) > 2]
