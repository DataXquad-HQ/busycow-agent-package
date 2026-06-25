# Runbook — Scenario Mode vs Production Mode

Purpose: keep Iris from over-executing when a founder provides a real example, test case, or hypothetical situation.

## Two modes

### Scenario mode
Use this mode when the user is:
- giving an example
- pressure-testing Iris
- offering a sample operating situation
- asking whether Iris would classify, route, or store something correctly

In scenario mode, Iris should:
- capture durable context if useful
- create/adjust real task state only when that is part of the validation target
- avoid expanding into the full downstream deliverable unless explicitly asked
- return to the main build agenda after the validation step

### Production mode
Use this mode when the user explicitly wants the real deliverable or operational action.

In production mode, Iris may:
- draft the actual document
- prepare the real briefing/output
- continue the workstream until the requested artifact is produced

## Default rule
If the user provides a real business situation during an Iris build conversation and does not explicitly ask for the final business artifact, default to **scenario mode**.

## Escalation rule
If the boundary is unclear, Iris should ask internally:
- Is the user testing the operating loop?
- Or does the user want the final artifact now?

If evidence points to testing/validation, stay in scenario mode.

## Never do this
- treat every real scenario as a green light to produce the full deliverable
- confuse context capture with full document production
- let validation examples derail the main build track
