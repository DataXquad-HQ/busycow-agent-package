# Schema — Review Item

## Required fields
- `title` — short human-readable label
- `type` — conflict | promotion_candidate | policy_change | stale_context | approval_needed
- `current_source` — where the item currently lives
- `why_it_matters` — business consequence in one sentence
- `recommended_action` — review_now | hold | reject | gather_more_evidence | escalate
- `owner_or_approver` — who should decide or review
- `evidence_links` — links or references to source material

## Optional fields
- `destination_if_approved`
- `deadline_or_review_time`
- `blocking_impact`

## Rule
A review item is incomplete if it lacks owner/approver, rationale, or source evidence.
