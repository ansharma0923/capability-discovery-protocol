"""Core discovery pipeline - 14 stages."""
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..intent.models import DiscoveryIntent
from ..intent.parser import extract_keywords, normalize_intent
from ..matching.filter import apply_filters
from ..matching.semantic import rank_by_semantic
from ..matching.validator import validate_capability
from ..observability.audit import DiscoveryAuditRecord, log_audit
from ..policy.engine import get_policy_engine
from ..ranking.scorer import rank_candidates
from ..registry.models import OfferingDescriptor, ProviderDescriptor
from ..registry.store import RegistryStore, get_store


def run_discovery_pipeline(
    intent: DiscoveryIntent,
    store: Optional[RegistryStore] = None,
    federated_results: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Execute the 14-stage ADP discovery pipeline.

    Stages:
    1.  parse_request
    2.  normalize_intent
    3.  extract_constraints
    4.  retrieve_candidates
    5.  deterministic_filtering
    6.  semantic_matching
    7.  capability_validation
    8.  policy_filtering
    9.  ranking
    10. explanation_generation
    11. federation_merge
    12. deduplication
    13. audit_logging
    14. response_generation
    """
    start_time = time.time()
    stages_executed: List[str] = []

    if store is None:
        store = get_store()

    # Stage 1: Parse request
    stages_executed.append("parse_request")

    # Stage 2: Normalize intent
    intent = normalize_intent(intent)
    stages_executed.append("normalize_intent")

    # Stage 3: Extract constraints
    keywords = extract_keywords(intent)
    stages_executed.append("extract_constraints")

    # Stage 4: Retrieve candidates
    all_offerings = store.list_offerings()
    all_providers_list = store.list_providers()
    providers_map: Dict[str, ProviderDescriptor] = {
        p.provider_id: p for p in all_providers_list
    }
    stages_executed.append("retrieve_candidates")

    # Stage 5: Deterministic filtering
    filtered = apply_filters(intent, all_offerings)
    stages_executed.append("deterministic_filtering")

    # Stage 6: Semantic matching
    semantically_scored = rank_by_semantic(intent, filtered)
    stages_executed.append("semantic_matching")

    # Stage 7: Capability validation
    capability_validated: List[Tuple[OfferingDescriptor, float]] = []
    for offering, sem_score in semantically_scored:
        provider = providers_map.get(offering.provider_id)
        valid, _ = validate_capability(intent, offering, provider)
        if valid:
            capability_validated.append((offering, sem_score))
    stages_executed.append("capability_validation")

    # Stage 8: Policy filtering
    policy_engine = get_policy_engine()
    offerings_only = [o for o, _ in capability_validated]
    policy_allowed = policy_engine.filter(offerings_only, providers_map)
    allowed_ids = {o.offering_id for o, _ in policy_allowed}
    policy_filtered = [
        (o, s) for o, s in capability_validated if o.offering_id in allowed_ids
    ]
    stages_executed.append("policy_filtering")

    # Stage 9: Ranking
    ranked = rank_candidates(intent, policy_filtered, providers_map)
    stages_executed.append("ranking")

    # Stage 10: Explanation generation (embedded in rank_candidates)
    stages_executed.append("explanation_generation")

    # Stage 11: Federation merge
    if federated_results:
        for r in federated_results:
            r["_source"] = "federated"
        for r in ranked:
            r["_source"] = "local"
        ranked = ranked + federated_results
    stages_executed.append("federation_merge")

    # Stage 12: Deduplication
    seen_ids: set = set()
    deduplicated = []
    for r in ranked:
        oid = r.get("offering_id")
        if oid and oid not in seen_ids:
            seen_ids.add(oid)
            deduplicated.append(r)
        elif not oid:
            deduplicated.append(r)
    deduplicated = sorted(
        deduplicated, key=lambda x: x.get("total_score", 0), reverse=True
    )
    stages_executed.append("deduplication")

    # Apply max_results
    max_results = intent.preferences.max_results
    final_results = deduplicated[:max_results]

    # Stage 13: Audit logging
    duration_ms = round((time.time() - start_time) * 1000, 2)
    top_score = final_results[0]["total_score"] if final_results else None
    audit = DiscoveryAuditRecord(
        intent_id=intent.intent_id,
        intent_text=intent.intent_text,
        category=intent.category.value,
        candidates_found=len(filtered),
        results_returned=len(final_results),
        pipeline_stages=stages_executed,
        top_score=top_score,
        federation_used=bool(federated_results),
        duration_ms=duration_ms,
        metadata={"keywords": keywords},
    )
    log_audit(audit)
    stages_executed.append("audit_logging")

    # Stage 14: Response generation
    stages_executed.append("response_generation")

    return {
        "intent_id": intent.intent_id,
        "version": "0.1.0",
        "category": intent.category.value,
        "total_candidates": len(filtered),
        "total_results": len(final_results),
        "results": final_results,
        "pipeline": {
            "stages_executed": stages_executed,
            "duration_ms": duration_ms,
            "federation_used": bool(federated_results),
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
