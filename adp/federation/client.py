"""Federation client for querying remote ADP nodes."""
import asyncio
from typing import List, Dict, Any, Optional
import httpx

from ..intent.models import DiscoveryIntent


class FederationClient:
    def __init__(self, nodes: List[str], timeout: float = 5.0):
        self.nodes = nodes
        self.timeout = timeout

    async def query_node(self, node_url: str, intent: DiscoveryIntent) -> Optional[Dict[str, Any]]:
        """Query a single remote node."""
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
