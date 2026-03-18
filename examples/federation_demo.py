"""Federation demo example."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adp.intent.models import DiscoveryIntent, Category
from adp.federation.client import configure_federation, get_federation_client
from adp.service.discovery import run_discovery_pipeline
from adp.registry.store import RegistryStore


def main():
    print("=== Federation Demo ===\n")

    # Configure federation nodes (these would be remote ADP instances)
    # In this demo, no nodes are reachable, so federation returns []
    configure_federation([
        "https://node1.adp.example.com",
        "https://node2.adp.example.com",
    ])

    client = get_federation_client()
    print(f"Configured {len(client.nodes)} federation nodes")
    print(f"Nodes: {client.nodes}\n")

    store = RegistryStore()
    intent = DiscoveryIntent(
        intent_text="I need noise-canceling headphones",
        category=Category.PRODUCT,
    )

    # Run with federation enabled (will timeout gracefully on unreachable nodes)
    import asyncio
    federated_results = asyncio.run(client.federate(intent))
    print(f"Federated results from remote nodes: {len(federated_results)}")

    result = run_discovery_pipeline(intent, store=store, federated_results=federated_results)
    print(f"Total results (local + federated): {result['total_results']}")
    print(f"Federation used: {result['pipeline']['federation_used']}")


if __name__ == "__main__":
    main()
