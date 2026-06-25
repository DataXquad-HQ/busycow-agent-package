# Runbook — Context Conflict Check

Purpose: identify conflicting sources, classify authority, and stop material action before stale or low-authority context causes damage.

Execution pattern:
1. Quote the conflicting statements explicitly.
2. Label the source class for each statement.
3. Rank authority using the context router.
4. Decide whether the conflict is harmless, operationally material, or governance material.
5. If material, stop action and create a review or escalation path.

Use when:
- memory conflicts with current state
- draft or evidence conflicts with canonical knowledge
- two systems imply different owners, approvals, or statuses

Default companion skills:
- `source-of-truth-check`
- `review-queue-triage`
