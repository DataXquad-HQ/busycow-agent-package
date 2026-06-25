# Runbook — Governed GBrain Write

Purpose: decide when Iris can write directly, when Iris should write evidence only, and when Iris must stage a governed change instead of mutating canonical knowledge.

Template: `templates/governed-gbrain-write-request-template.md`

## Physical structure
- Canonical knowledge: `core/`
- Evidence trail: `evidence/`
- Governance staging: `review/`

## Direct write allowed
Use direct write behavior for:
- workspace notes
- sourced evidence notes
- low-risk task-adjacent context
- internal handoff context
- evidence pages that describe what happened

## Review-first write required
Use review-first behavior for:
- canonical knowledge updates
- authority or policy changes
- cross-agent behavior changes
- memory-to-canonical promotion
- deletion or overwrite of important context

## Decision path
1. Ask: is this current state, evidence, memory, draft context, or canonical truth?
2. If it is evidence, write to `evidence/` or retain as traceable source material.
3. If it is canonical candidate knowledge, route through the review queue first.
4. If approved later, publish into the correct `core/` destination.
5. If uncertain, use `routing-context` logic and choose the more conservative path.

## Canonical destinations
- company-level truth → `core/company/`
- business-line truth → `core/business-lines/[bl]/`
- entity truth → `core/people/` or `core/companies/`
- approved decisions → `core/decisions/`
- system doctrine / runbooks / architecture → `core/systems/`
- market intelligence → `core/market-intel/`

## Rule
Evidence can justify belief, but evidence is not policy. Review is the boundary between the two.
