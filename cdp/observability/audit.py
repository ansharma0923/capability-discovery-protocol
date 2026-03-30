"""Audit logging and observability."""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..registry.store import get_store


class DiscoveryAuditRecord:
    def __init__(
        self,
        intent_id: str,
        intent_text: str,
        category: str,
        candidates_found: int,
        results_returned: int,
        pipeline_stages: List[str],
        top_score: Optional[float],
        federation_used: bool,
        duration_ms: float,
        metadata: Dict[str, Any],
    ):
        self.audit_id = str(uuid.uuid4())
        self.version = "0.1.0"
        self.intent_id = intent_id
        self.intent_text = intent_text
        self.category = category
        self.candidates_found = candidates_found
        self.results_returned = results_returned
        self.pipeline_stages = pipeline_stages
        self.top_score = top_score
        self.federation_used = federation_used
        self.duration_ms = duration_ms
        self.metadata = metadata
        self.recorded_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "version": self.version,
            "intent_id": self.intent_id,
            "intent_text": self.intent_text,
            "category": self.category,
            "candidates_found": self.candidates_found,
            "results_returned": self.results_returned,
            "pipeline_stages": self.pipeline_stages,
            "top_score": self.top_score,
            "federation_used": self.federation_used,
            "duration_ms": self.duration_ms,
            "metadata": self.metadata,
            "recorded_at": self.recorded_at,
        }


def log_audit(record: DiscoveryAuditRecord) -> None:
    store = get_store()
    store.add_audit_log(record.to_dict())
