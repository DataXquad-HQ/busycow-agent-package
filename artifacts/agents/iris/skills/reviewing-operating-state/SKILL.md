---
name: reviewing-operating-state
description: >
  Use when Iris needs to answer "what is true right now" about the company's
  operating state — current priorities, active objectives, stale structures,
  system health, or whether the task / memory / knowledge layers still match
  reality. Triggers on requests such as "current operating state", "what are we
  actually doing now", "what changed", or before rewriting OKRs and priorities.
triggers:
  - "current operating state"
  - "what are we actually doing now"
  - "what changed operationally"
  - "review operating state"
  - "before we change OKRs"
  - "what is true right now"
version: "1.0"
author: BusyCow / Iris
---

# Reviewing Operating State

## When to Use

Use this when Iris needs a current-state view of the company as an operating system.
The output should say what is active now, what is stale, and what downstream systems
must change because of that reality.

Do not use this for historical deep-dives. This is for **active truth**, not archive review.

---

## Steps

### 1. Read the current-state sources first

Check the latest active sources in this order:
1. company overview / strategy docs
2. current business-line strategy docs
3. active OKR / task layer
4. recent decision logs
5. hot-memory signals if founder preference or recent choice matters

### 2. Separate three buckets

Every item you find should land in one of these buckets:
- **Active truth** — should shape decisions today
- **Stale structure** — still present in the system, but no longer reflects reality
- **Open ambiguity** — not resolved enough to treat as truth

### 3. Produce the state summary

Default summary structure:
- what the company is prioritizing now
- what the operating bottlenecks are now
- what structures are stale now
- what should change next in OKR / task / memory / knowledge layers

### 4. Name the required system updates

If the operating state and the system differ, specify which layer must change:
- GBrain current-state docs
- decision log
- Hindsight
- OKR list
- execution tasks
- cron / infra

### 5. Stop when the answer is decision-useful

Do not dump every detail. The output is good when a founder can decide the next operating move from it.

---

## Quality Bar

Before returning output:
- Did I distinguish active truth from stale structure?
- Did I avoid presenting historical residue as current strategy?
- Are recommended updates tied to specific evidence from docs, tasks, or tool output?
- Is the summary short enough to drive a decision rather than bury it?

If any check fails, rewrite the summary.

---

## Fallback Behavior

- If the task layer is unavailable: still produce a current-state summary from docs and memory, but label execution visibility as incomplete.
- If hot memory is unavailable: rely on written strategy / decision docs and label founder-preference confidence as reduced.
- If current-state docs conflict with task reality: report the conflict explicitly instead of guessing which one is right.

---

## Pitfalls

- Confusing historical decisions with the current operating state
- Treating an old OKR or stale task structure as proof of current priorities
- Giving a long descriptive answer without naming what needs to be updated next
- Trying to be comprehensive instead of decision-useful
