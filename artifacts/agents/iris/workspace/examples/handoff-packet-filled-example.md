# Example — Filled Handoff Packet

## Good output

**Main takeaway: the receiver can act immediately because the packet includes status, timing, evidence, and the approval boundary.**

```md
# Handoff Packet

- task_title: Patch stale SOUL routing references to match core/evidence/review topology
- receiver: [Founder 1]
- why_receiver: [Founder 1] owns runtime/architecture decisions that affect the default Hermes profile.
- current_status: Canonical docs and GBrain layout are already updated; runtime guidance still has stale references in some places.
- timing_expectation: Review and approve the patch direction this week before broader router enforcement.
- why_it_matters: If stale runtime guidance remains, agents may keep reading or writing against the wrong authority layer.
- relevant_decision_or_policy: core/decisions/2026-06-24-normalize-hindsight-and-gbrain-before-router-enforcement
- evidence_links:
  - core/systems/contextual-layer-operating-model
  - {{HERMES_INSTALL_ROOT}}/workspaces/iris/AGENTS.md
- expected_output: Confirm the target routing language and approve patching the remaining runtime references.
- approval_boundary: Do not mutate default-profile identity/routing rules without explicit approval.
- escalation_trigger: Escalate immediately if runtime guidance is found to conflict with canonical docs during a live agent workflow.

Optional:
- recall_query: stale SOUL routing references contextual layer topology
- known_risks:
  - agents may trust stale path names
- dependency_list:
  - updated canonical doc in GBrain
```

## Why this is good
- Gives the receiver enough context without reopening the whole architecture debate.
- Uses evidence and decision links instead of relying on chat memory.
- Makes the approval line explicit.
