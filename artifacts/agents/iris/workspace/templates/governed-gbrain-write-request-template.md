# Governed GBrain Write Request Template

Use when Iris believes something may deserve canonical publication but should not be written into `core/` directly.

## Copyable skeleton

```md
# Governed GBrain Write Request

- proposed_title:
- proposed_destination:
- current_source:
- information_class: evidence | policy | decision | playbook_guidance | recurring_pattern | operating_note
- why_candidate:
- why_not_direct_write:
- evidence_links:
- owner_or_approver:
- recommended_path: review_queue_first | hold_pending_more_evidence | reject

Optional:
- related_entities:
- source_event_id:
- destination_if_approved:
- review_deadline:
```

## Decision rule
- If it only proves what happened -> write or keep it in `evidence/`.
- If it changes shared truth or doctrine -> send through review first.
- If evidence is thin -> hold instead of promoting.
