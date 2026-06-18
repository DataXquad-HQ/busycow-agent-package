# Account Signal Taxonomy

Use only these signal types:
- `momentum`
- `expansion_opportunity`
- `churn/risk`
- `blocker/dependency`
- `stakeholder_movement`
- `upcoming_commitment_or_deadline`
- `evidence_gap`

## Required fields
For every retained signal include:
- signal_type
- summary
- source
- recency
- confidence
- recommended_next_step

## Confidence guidance
- `high` — strong source or multiple corroborating sources
- `medium` — useful, plausible, partially corroborated
- `low` — weak or stale; keep only if it frames uncertainty clearly

## Recency guidance
- `fresh` — within the current working window and action-relevant now
- `recent` — slightly older but still operationally relevant
- `stale` — context only; should not drive prioritization by itself

## Noise filter
Do not retain a signal unless it could change:
- outreach timing
- meeting prep
- opportunity strategy
- account priority
