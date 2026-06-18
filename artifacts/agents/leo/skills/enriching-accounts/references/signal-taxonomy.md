# Enrichment Signal Taxonomy

Normalize non-trivial Level 2 findings into these signal types:
- `momentum`
- `expansion_opportunity`
- `churn/risk`
- `blocker/dependency`
- `stakeholder_movement`
- `upcoming_commitment_or_deadline`
- `evidence_gap`

## Keep / skip rule
Keep only findings that could change how the BD team:
- prioritizes the account
- frames outreach
- prepares for the next meeting
- judges opportunity timing or risk

## Per-signal fields
- signal_type
- summary
- source
- recency
- confidence
- recommended_next_step

## Example translations
- funding round → `momentum` or `expansion_opportunity`
- new country office → `expansion_opportunity`
- executive departure → `stakeholder_movement` or `churn/risk`
- public delay / outage / complaint → `churn/risk`
- missing reliable recent evidence → `evidence_gap`
