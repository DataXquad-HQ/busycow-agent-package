# Runbook — Review Queue Staging

Purpose: stage governed candidates into the contextual review queue instead of publishing directly.

## Runtime artifacts
- Queue service: `{{HERMES_INSTALL_ROOT}}/contextual_layer/review_queue.py`
- Queue store: `{{HERMES_INSTALL_ROOT}}/contextual_layer/review_queue_store.json`
- Router CLI: `{{HERMES_INSTALL_ROOT}}/contextual_router/router_cli.py`

## Candidate types currently supported
- `canonical_candidate`
- `shared_memory_candidate`

## When to stage into review
- canonical knowledge candidate
- shared-memory candidate that needs governance
- policy-change candidate
- conflict-resolution candidate
- stale-context cleanup candidate

## Preferred path
1. Build an event envelope JSON with at least:
   - `event_id`
   - `occurred_at`
   - `agent_id`
2. Add useful fields when available:
   - `business_line`
   - `domain`
   - `source_system`
   - `source_ref`
   - `entities`
   - `summary`
   - `evidence_refs`
   - `needs_review`
   - `is_draft`
   - `repeated_pattern`
3. Run the router with review enqueue:
   - `python3 {{HERMES_INSTALL_ROOT}}/contextual_router/router_cli.py write /path/to/event.json --enqueue-review`
4. Confirm the router decision and review candidate both exist.
5. Use `templates/review-item-template.md` when writing the human-readable review packet.
6. Reference the candidate ID in the human-facing summary if action is needed.

## Minimal operator expectations
A staged review item should make clear:
- what the candidate is
- why it matters
- who should review it
- where it would go if approved
- what evidence supports it

## Never do this
- publish directly to canonical knowledge when review is required
- treat repeated chat or memory as approved truth
- create a vague review item with no source, owner, or destination
