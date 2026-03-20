"""Federation client for querying remote ADP nodes."""
import asyncio
from typing import Any, Dict, List, Optional

import httpx

from ..intent.models import DiscoveryIntent
from ..registry.models import OfferingDescriptor, ProviderDescriptor


class LocalFederationSimulator:
    """
    Simulates a remote ADP federation node for local testing and demos.

    Each simulated node has its own in-memory registry of providers and
    offerings.  When queried, the node runs the same deterministic
    filtering + semantic scoring logic as the real pipeline so that the
    returned results are meaningful and reproducible.
    """

    def __init__(self, node_url: str, offerings: List[OfferingDescriptor], providers: List[ProviderDescriptor]):
        self.node_url = node_url
        self._offerings = offerings
        self._providers = {p.provider_id: p for p in providers}

    def query(self, intent: DiscoveryIntent) -> Dict[str, Any]:
        """Return a federation-response-shaped dict for the given intent."""
        import time
        from datetime import datetime, timezone

        from ..matching.filter import apply_filters
        from ..matching.semantic import rank_by_semantic
        from ..ranking.scorer import rank_candidates

        start = time.time()

        filtered = apply_filters(intent, self._offerings)
        scored = rank_by_semantic(intent, filtered)
        ranked = rank_candidates(intent, scored, self._providers)

        max_results = intent.preferences.max_results
        results = ranked[:max_results]
        for r in results:
            r["_source"] = "federated"
            r["_node"] = self.node_url

        duration_ms = round((time.time() - start) * 1000, 2)
        return {
            "results": results,
            "total_results": len(results),
            "responding_node": self.node_url,
            "duration_ms": duration_ms,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class FederationClient:
    def __init__(self, nodes: List[str], timeout: float = 5.0):
        self.nodes = nodes
        self.timeout = timeout
        # Simulator nodes registered at runtime (used when the real node URL
        # matches a registered simulator).
        self._simulators: Dict[str, LocalFederationSimulator] = {}

    def register_simulator(self, simulator: LocalFederationSimulator) -> None:
        """Register a local simulator for a node URL (used in tests/demos)."""
        self._simulators[simulator.node_url] = simulator

    async def query_node(self, node_url: str, intent: DiscoveryIntent) -> Optional[Dict[str, Any]]:
        """Query a single remote node, falling back to simulator if registered."""
        if node_url in self._simulators:
            return self._simulators[node_url].query(intent)
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{node_url}/discover",
                    json=intent.model_dump(mode="json"),
                )
                if response.status_code == 200:
                    return response.json()
        except Exception:
            pass
        return None

    async def federate(self, intent: DiscoveryIntent) -> List[Dict[str, Any]]:
        """Query all nodes and merge results."""
        if not self.nodes:
            return []

        tasks = [self.query_node(node, intent) for node in self.nodes]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        merged = []
        for result in results:
            if isinstance(result, dict) and "results" in result:
                for r in result["results"]:
                    r["_federated"] = True
                    merged.append(r)

        return merged

    def deduplicate(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate by offering_id."""
        seen: set = set()
        unique = []
        for r in results:
            oid = r.get("offering_id")
            if oid and oid not in seen:
                seen.add(oid)
                unique.append(r)
        return unique


# Default client (no nodes configured)
_client = FederationClient(nodes=[])


def get_federation_client() -> FederationClient:
    return _client


def configure_federation(nodes: List[str]) -> None:
    global _client
    _client = FederationClient(nodes=nodes)
