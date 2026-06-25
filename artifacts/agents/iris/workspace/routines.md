# Iris Routines

## Primary routine
### Daily operating check
Objective: surface only the few operating items that deserve attention.
Reference runbook: `runbooks/first-real-operating-loop.md`
Reference example: `examples/first-real-operating-loop-example.md`
Structured-state note: `runbooks/structured-task-state-loop.md`
Publish-loop note: `runbooks/review-approved-canonical-publish-loop.md`

Default sequence:
1. Review active tasks, blockers, stale handoffs, and pending approvals.
2. Run `source-of-truth-check` when status appears to come from the wrong authority layer.
3. Run `context-conflict-check` when two sources materially disagree.
4. Run `review-queue-triage` if review items, policy candidates, or unresolved conflicts are waiting.
5. End with `operating-briefing` to produce the compact human-facing output.
6. Before sending, validate the result against `schemas/operating-brief-schema.md` and `evaluators/coo-briefing-rubric.md`.
7. Stay silent or return a short all-clear if nothing material changed.

Escalate instead of continuing when:
- the approval boundary is unclear
- the owner is missing
- canonical truth and current state disagree on a material item
- an external-facing action depends on unresolved context

## Secondary routines
### Decision-to-execution routine
Use `decision-recording` → `task-routing` → `handoff-briefing`.
Before handing off, check `schemas/handoff-briefing-schema.md`.

### Weekly memory hygiene
Use `memory-audit` first, then `knowledge-promotion-review` on only the meaningful candidates.
Do not promote directly from memory to canonical knowledge without review.
Before sending, validate governance outputs against `schemas/review-item-schema.md` and `evaluators/governance-review-rubric.md`.

### Agent quality incident review
Use `agent-behavior-review` when another agent becomes low-quality, unresponsive, unsafe, or operationally confusing.

### Real-scenario validation
Use `runbooks/human-in-the-loop-scenario-validation.md` when a founder provides a live situation as a test case for Iris.
Boundary rule: if the user is testing Iris with a real scenario, default to scenario mode unless they explicitly ask for the final deliverable.
Reference example: `examples/portfolio-company-scenario-validation-example.md`
Reference boundary: `runbooks/scenario-mode-vs-production-mode.md`

### Monthly governance hygiene
Review authority boundaries, recurring review queue items, and stale workspace instructions.
