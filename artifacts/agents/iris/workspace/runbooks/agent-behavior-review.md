# Runbook — Agent Behavior Review

Purpose: diagnose low-quality, unsafe, or off-pattern agent behavior as an operating issue before proposing a fix.

Execution pattern:
1. Describe the problematic behavior concretely.
2. Separate observed behavior from inferred cause.
3. Classify the likely cause area: stale context, wrong source of truth, unclear authority, profile/runtime drift, tool issue, bad handoff, or skill gap.
4. Rank impact: quality only, blocked work, governance risk, or external-facing risk.
5. Recommend the narrowest useful fix first.
6. Escalate if the fix changes another agent's authority, role, or high-impact behavior.

Use when:
- an agent feels weird, low-quality, or inconsistent
- output degradation may be a systems issue rather than a capability issue
