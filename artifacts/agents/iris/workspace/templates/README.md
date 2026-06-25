# Iris Templates

These templates turn the side-effect loop into reusable runtime artifacts.

Use them when Iris needs to create:
- a governed review candidate
- a handoff packet
- a governed GBrain write request

Rule:
- current-state updates belong in the system of record
- evidence belongs in `evidence/`
- canonical changes go through review before `core/`
