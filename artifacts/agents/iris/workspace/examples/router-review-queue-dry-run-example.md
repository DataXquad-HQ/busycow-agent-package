# Example — Router to Review Queue Dry Run

This example uses the **real router CLI** and **real review queue code** but writes to a **temporary store** under `/tmp/iris-router-dry-run/` so the live queue stays clean.

## Step 1 — Event envelope used

```json
{
  "event_id": "dryrun-contextual-layer-runtime-architecture",
  "occurred_at": "2026-06-25T04:17:50+00:00",
  "agent_id": "iris",
  "business_line": "shared",
  "domain": "systems",
  "source_system": "hermes-chat",
  "source_ref": "feishu-dm-2026-06-25",
  "entities": [
    "core/systems/contextual-layer-operating-model"
  ],
  "claim_type": "canonical_candidate",
  "authoritative_system": "gbrain",
  "volatility": "low",
  "confidence": 0.93,
  "summary": "Document the current runtime contextual-layer architecture snapshot for [Org].",
  "evidence_refs": [
    "core/systems/contextual-layer-operating-model",
    "{{HERMES_INSTALL_ROOT}}/workspaces/iris/AGENTS.md"
  ],
  "needs_review": true,
  "is_draft": false,
  "repeated_pattern": true,
  "pattern_scope": "contextual-layer-governance"
}
```

## Step 2 — Command pattern

```bash
python3 contextual_router/router_cli.py write /tmp/iris-router-dry-run/event.json \
  --enqueue-review \
  --review-store /tmp/iris-router-dry-run/review_store.json
```

## Step 3 — Actual router result

- classification: `canonical_candidate`
- primary destination: `review-queue`
- secondary destination: `gbrain:canonical`
- governance required: `true`
- generated candidate id: `rq-20260625-document-the-current-runtime-contextual-layer-ar-b2b3d4`
- proposed destination: `gbrain:canonical`

## Step 4 — Actual exported queue view

```md
# Contextual Review Queue

| ID | Status | Type | Domain | Review Owner | Title | Destination |
|---|---|---|---|---|---|---|
| `rq-20260625-document-the-current-runtime-contextual-layer-ar-b2b3d4` | new | canonical_candidate | systems | Iris | Document the current runtime contextual-layer architecture snapshot for [Org] | gbrain:canonical |
```

## Why this example matters

- It proves the runtime path from event envelope -> router decision -> staged review candidate.
- It keeps the live governance queue clean by using a temporary review store.
- It gives Iris operators a safe pattern for future validation runs.
