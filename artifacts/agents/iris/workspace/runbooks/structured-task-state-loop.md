# Runbook — Structured Task State Loop

Purpose: turn a routed work item into real task state without confusing memory, chat, or review notes for execution truth.

## System of record
- Target primary execution system: **Lark default Tasks**
- Current executable fallback in this runtime: **[Org] legacy Lark Base task tracker via app identity**
- Use the legacy Base tracker when the runtime needs a real write path and default Lark Tasks are not exposed through tools.
- Chat, memory, and workspace notes are not task truth.

## When to use
- a task now needs an owner, deadline, or status
- a blocker should become visible execution state
- a handoff needs to land in a real task system

## Loop
1. Confirm the work item belongs in structured task state rather than review or evidence.
2. Check whether the item is executable now or still waiting on approval.
3. If approval is still missing, create a review/approval item first instead of assigning execution directly.
4. If executable, create or update the task with:
   - title
   - owner
   - status
   - deadline or review time
   - why it matters
   - evidence or decision link
5. If the receiver needs context, attach a handoff briefing in parallel.
6. If the task system write cannot be completed, report the write as pending rather than pretending the task exists.

## Output check
A task-state update is complete only if a human could answer:
- who owns it?
- what is the status?
- by when should it move?
- what source or decision justifies the work?

## Escalate instead of writing when
- ownership is genuinely unclear
- approval is missing
- the task would create an external commitment
- the request is actually a policy or canonical knowledge change
