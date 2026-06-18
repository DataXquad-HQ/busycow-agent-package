---
name: governing-okr-and-task-state
description: >
  Use when Iris needs to keep the OKR layer and execution-task layer aligned —
  rewriting objectives, archiving stale initiatives, mapping tasks to KRs,
  checking whether active work still matches company reality, or preparing an
  operating review. Triggers on requests such as "clean up the OKRs", "re-map
  tasks", "what no longer belongs", or "does execution still match strategy".
triggers:
  - "clean up the OKRs"
  - "re-map tasks"
  - "what no longer belongs"
  - "does execution still match strategy"
  - "update objectives and tasks"
  - "okr and task state"
version: "1.0"
author: BusyCow / Iris
---

# Governing OKR and Task State

## When to Use

Use this when Iris needs to maintain alignment between:
- current company priorities
- the OKR layer
- the execution-task layer

This is a governance workflow, not a one-off task edit.

---

## Steps

### 1. Start from company reality, not from the old OKR list

Read the current company strategy / operating state first.
The OKR layer is downstream of reality; it is not the source of truth by itself.

### 2. Classify every existing item

For each objective, KR, or legacy initiative, classify it as:
- **active** — still reflects current priorities
- **stale** — no longer reflects current priorities
- **archive** — useful historically but should not drive current execution
- **ambiguous** — needs clarification before it can stay active

### 3. Rewrite the OKR layer only after classification

The correct order is:
1. decide what is true now
2. rewrite objectives and KRs
3. archive / hide stale items
4. re-map execution tasks to the surviving structure

### 4. Re-map execution tasks

For each active execution task, answer:
- which objective does it support?
- which KR does it support?
- if it supports none, should it be archived, rewritten, or promoted into a new KR?

### 5. Identify gaps in both directions

Check for:
- KRs with no execution tasks
- execution tasks with no clear KR
- stale tasks still consuming attention
- active work concentrated on the wrong objective set

### 6. Return the governance result

Default output should say:
- what was kept active
- what was archived / hidden
- how execution was re-mapped
- what gaps still remain

---

## Quality Bar

Before returning output:
- Did I start from current company reality instead of preserving old structures by inertia?
- Did I separate active / stale / archive clearly?
- Is every suggested task mapping traceable to a specific objective or KR?
- Did I identify both missing-task gaps and orphan-task gaps?

If any check fails, the governance pass is incomplete.

---

## Fallback Behavior

- If the task layer is unavailable: still clean the OKR layer conceptually and report that execution remapping is pending.
- If the strategy layer is thin or contradictory: state that the OKR rewrite has reduced confidence.
- If historical items cannot be safely deleted: mark them archive / hidden rather than pretending they are active.

---

## Pitfalls

- Starting from the existing OKR list instead of current strategy
- Preserving dead initiatives because they already exist in the tool
- Re-mapping tasks mechanically without checking whether the task still matters
- Treating archive items as if they are still part of the current execution cycle
