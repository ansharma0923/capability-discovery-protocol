# Federation Model

## Overview

ADP federation allows a node to query other ADP nodes and merge their results into a single response.

## Architecture

```
Client → ADP Node A → ADP Node B
                    → ADP Node C
                    ← Merge results
         ← Combined response
```

## Federation Query

When `include_federation: true` is set in preferences, or when using the `/federate/discover` endpoint, the local node will:

1. Execute the local pipeline
2. Concurrently query all configured remote nodes
3. Merge and deduplicate results
4. Sort combined results by score

## Configuration

Configure federation nodes at startup:

```python
from adp.federation.client import configure_federation
configure_federation(["https://node2.adp.example.com", "https://node3.adp.example.com"])
```

## Deduplication

Results from multiple nodes are deduplicated by `offering_id`. The first occurrence (by score) wins.

## Failure Handling

Federation queries use per-node timeouts (default: 5 seconds). Node failures are silently ignored — local results are still returned.

## Security

- Always use TLS for federation connections
- Validate node identities before enabling federation
- Federated results are marked with `_source: "federated"`
