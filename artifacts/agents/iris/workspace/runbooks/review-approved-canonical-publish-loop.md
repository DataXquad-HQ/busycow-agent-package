# Runbook — Review-Approved Canonical Publish Loop

Purpose: turn a governed candidate into a published canonical update without skipping review history.

## What this loop is for
Use this when a review item has enough evidence and the approver agrees the change should become official truth in `core/`.

## Current executable path in this runtime
- Review candidate state is managed by `contextual_layer/review_queue.py`
- Router-created candidates come from `contextual_router/router_cli.py --enqueue-review`
- Canonical publication lands in GBrain / knowledge-base repo
- Publication and queue transition should both be recorded; neither one alone is enough

## Publish loop

### 1. Confirm the candidate is ready
A candidate is ready only if it has:
- a clear approver
- evidence links
- a concrete canonical destination
- no unresolved source-of-truth conflict

### 2. Transition review status to `approved`
Command pattern:
```bash
python3 scripts/publish_review_candidate.py approve <candidate_id> \
  --store <store.json> \
  --actor Iris \
  --note "Approved for canonical publication"
```

### 3. Publish to canonical destination
Choose one:
- update an existing canonical page in `core/`
- create the missing canonical page

Publication rule:
- if it is still only proof of what happened, keep it in `evidence/`
- if it changes approved doctrine, publish to the named `core/` destination

### 4. Transition review status to `published`
Command pattern:
```bash
python3 scripts/publish_review_candidate.py publish <candidate_id> \
  --store <store.json> \
  --canonical-slug <core/.../page-slug> \
  --actor Iris \
  --note "Canonical publication completed"
```

### 4A. One-shot close loop helper
When the candidate is new and the target canonical file already exists, you can close the loop in one command:
```bash
python3 scripts/publish_review_candidate.py close-loop <candidate_id> \
  --store <store.json> \
  --canonical-slug <core/.../page-slug> \
  --actor Iris
```

### 5. Report both outcomes
A human-facing summary should include:
- what changed
- where it was published
- which candidate closed the loop

## Minimum quality bar
- review history exists
- canonical destination is explicit
- queue status does not remain `approved` after publication actually landed
- publication summary names the candidate id or source event

## Never do this
- publish to `core/` while the candidate is still unresolved
- mark a candidate `published` before the canonical write actually lands
- treat evidence notes as canonical publication
