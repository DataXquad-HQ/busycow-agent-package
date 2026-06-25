# Runbook — First Real Operating Loop

Purpose: give Iris one concrete V1 operating loop that can run daily without pretending to be fully autonomous.

## V1 success condition
A good V1 run should be able to:
1. identify the few operating items that matter now
2. verify the right authority layer before making a claim
3. route real work to an owner with enough context to act
4. stage governed knowledge changes instead of writing directly into canonical truth
5. end with a short human-readable operating brief

## Input systems
- structured current state: task system / CRM / approvals
- canonical knowledge: `core/`
- evidence/history: `evidence/`
- recent context: Hindsight
- runtime instructions: workspace runbooks + schemas + examples

## Loop steps

### 1. Scan for signal
Use `reviewing-tasks` or the best available structured-state surface first.
Look only for:
- blocked work
- missing owners
- missing deadlines
- pending approvals
- stale handoffs
- review items that block execution

### 2. Check authority before trusting a claim
If a status, decision, or instruction appears to come from memory, chat, or draft context, run `source-of-truth-check`.
Rule:
- current status -> system of record
- approved guidance -> `core/`
- historical proof -> `evidence/`
- recent learned context -> Hindsight
- draft/in-progress wording -> workspace

### 3. Resolve conflicts only when material
If two sources disagree on a material item, run `context-conflict-check`.
Escalate instead of smoothing over the conflict when:
- owner is unclear
- approval state is unclear
- canonical guidance conflicts with live state
- an external-facing action depends on the answer

### 4. Route work when action is needed
When a real work item exists, use `task-routing`.
Minimum routing structure:
- title
- owner
- status
- why it matters
- deadline or review time
- evidence links

### 5. Create the handoff packet
When routing work to another human or agent, use `handoff-briefing` plus:
- `templates/handoff-packet-template.md`
- `examples/handoff-packet-filled-example.md`

### 6. Stage governed changes conservatively
If the work reveals a candidate policy / doctrine / canonical update:
- do not write directly to `core/`
- use `review-queue-staging`
- use `templates/review-item-template.md` or `templates/governed-gbrain-write-request-template.md`
- use `examples/router-review-queue-dry-run-example.md` if you need a safe validation pattern

### 7. Finish with the operating brief
Use `operating-briefing`.
The final output should contain only:
- the main takeaway
- 2–5 short bullets
- one next step only if action is needed

## What V1 is not
V1 does not require:
- autonomous mutation of every system
- perfect graph coverage in GBrain
- zero manual governance
- broad self-directed planning beyond the current operating loop

V1 does require disciplined routing, concise output, and safe handling of authority boundaries.
