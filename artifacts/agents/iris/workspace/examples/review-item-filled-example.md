# Example — Filled Review Item

## Good output

**Main takeaway: this is the right shape for a governed promotion candidate because it names the consequence, the approver, and the publication destination.**

```md
# Review Item

- title: Document the current runtime contextual-layer architecture snapshot for [Org]
- type: promotion_candidate
- current_source: feishu-dm-2026-06-25 + {{HERMES_INSTALL_ROOT}}/workspaces/iris/AGENTS.md
- why_it_matters: Without a canonical runtime snapshot, agents and humans can keep mixing SOUL, workspace, memory, and system-of-record roles.
- recommended_action: review_now
- owner_or_approver: Iris
- evidence_links:
  - core/systems/contextual-layer-operating-model
  - {{HERMES_INSTALL_ROOT}}/workspaces/iris/AGENTS.md

Optional:
- destination_if_approved: core/systems/contextual-layer-operating-model
- candidate_id: rq-20260625-document-the-current-runtime-contextual-layer-ar-b2b3d4
- source_event_id: dryrun-contextual-layer-runtime-architecture
```

## Why this is good
- Uses a real candidate pattern from the router dry run.
- Makes the publication destination explicit.
- Explains why the review matters operationally, not just structurally.
