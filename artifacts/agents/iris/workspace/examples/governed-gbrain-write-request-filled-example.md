# Example — Filled Governed GBrain Write Request

## Good output

**Main takeaway: this shows when Iris should ask for canonical publication instead of writing directly into `core/`.**

```md
# Governed GBrain Write Request

- proposed_title: Current Runtime Architecture Snapshot for the Contextual Layer
- proposed_destination: core/systems/contextual-layer-operating-model
- current_source: feishu-dm-2026-06-25 + Iris workspace runtime docs
- information_class: policy
- why_candidate: The runtime split between SOUL, workspace, skills, router, Hindsight, GBrain, and systems of record was clarified and should be visible in the canonical operating model.
- why_not_direct_write: It affects shared understanding of authority boundaries and therefore belongs behind governance, not ad hoc chat memory.
- evidence_links:
  - core/systems/contextual-layer-operating-model
  - {{HERMES_INSTALL_ROOT}}/workspaces/iris/AGENTS.md
- owner_or_approver: Iris
- recommended_path: review_queue_first

Optional:
- related_entities:
  - core/systems/contextual-layer-operating-model
- source_event_id: dryrun-contextual-layer-runtime-architecture
- destination_if_approved: core/systems/contextual-layer-operating-model
- review_deadline: next governance pass
```

## Why this is good
- Distinguishes evidence/source from publication target.
- States exactly why direct write would be too loose.
- Keeps the governance path conservative.
