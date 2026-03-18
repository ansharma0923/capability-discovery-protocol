# Ranking Model

## Weighted Scoring

Each candidate receives a composite score based on 6 dimensions:

| Dimension | Default Weight | Description |
|-----------|---------------|-------------|
| relevance | 0.30 | Semantic keyword match score |
| price | 0.20 | How well price fits the budget |
| latency | 0.15 | How well latency fits the constraint |
| availability | 0.15 | Raw availability score |
| trust | 0.15 | Provider trust level score |
| freshness | 0.05 | How recently the offering was updated |

## Ranking Profiles

Profiles adjust weights for different optimization goals:

| Profile | relevance | price | latency | availability | trust | freshness |
|---------|-----------|-------|---------|--------------|-------|-----------|
| default | 0.30 | 0.20 | 0.15 | 0.15 | 0.15 | 0.05 |
| cost_optimized | 0.20 | 0.40 | 0.10 | 0.10 | 0.10 | 0.10 |
| latency_optimized | 0.20 | 0.10 | 0.40 | 0.15 | 0.10 | 0.05 |
| trust_optimized | 0.25 | 0.10 | 0.10 | 0.15 | 0.35 | 0.05 |

## Score Computation

```
total_score = sum(weight_i * score_i for i in dimensions)
total_score = clamp(total_score, 0.0, 1.0)
```

All dimension scores are normalized to [0.0, 1.0].
