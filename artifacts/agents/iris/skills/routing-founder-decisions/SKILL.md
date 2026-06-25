---
name: routing-founder-decisions
description: >
  Use when a founder gives direction and Iris must decide where it belongs in
  the operating system — decision log, current-state docs, hot memory, OKRs,
  tasks, or nowhere. Triggers on requests such as "we decided", "from now on",
  "remember this rule", "change the way we do this", or anytime founder
  direction needs to be converted into operational routing.
triggers:
  - "we decided"
  - "from now on"
  - "remember this rule"
  - "change the way we do this"
  - "update the way we operate"
  - "founder decision"
version: "1.0"
author: BusyCow / Iris
---

# Routing Founder Decisions

## When to Use

Use this when a founder says something that should change future behavior.
The core job is not just to remember it — the core job is to route it into the right system.

---

## Routing Table

| Decision type | Primary destination |
|---|---|
| company-wide operating rule | decision log + current-state doc + `[org]-global` equivalent |
| founder-specific preference | founder hot-memory bank |
| strategic direction change | decision log + relevant strategy doc |
| execution reprioritization | OKR / task layer |
| temporary task instruction | task layer only |
| unresolved discussion | nowhere durable yet |

---

## Steps

### 1. Classify the founder statement

Ask:
- Is this a **preference**, a **decision**, a **priority shift**, or just a thought?
- Is it **durable** enough to affect future sessions?
- Does it change **system behavior**, **execution behavior**, or just this conversation?

### 2. Choose the destination layer

Route based on function, not convenience:
- preference → hot memory
- structural decision → decision log + active state
- execution direction → OKR / tasks
- unresolved thought → do not freeze it into truth yet

### 3. Check whether multiple layers must change

Many founder decisions need more than one write.
Typical example:
- decision log for history
- current-state doc for active truth
- task changes for execution
- hot memory if it also reveals preference or decision style

### 4. State the routing result

Default output should say:
- what this founder statement is
- where it belongs
- what was updated
- what still needs follow-through

### 5. Preserve the distinction between style and strategy

A founder saying "be more concise" is not the same as a company strategy change.
Do not route preference into the wrong system.

---

## Quality Bar

Before returning output:
- Did I classify the founder statement correctly?
- Did I route preference vs strategic decision to different places?
- Did I avoid writing unresolved discussion as durable truth?
- If execution changed, did I name the task / OKR consequence explicitly?

If any check fails, the routing is incomplete.

---

## Fallback Behavior

- If the correct destination system is unavailable: state the intended routing and complete the other durable writes first.
- If the founder statement is ambiguous: label the ambiguity and do not over-route it.
- If multiple systems conflict after the update: report the conflict explicitly instead of silently picking one.

---

## Pitfalls

- Treating every founder sentence as a decision
- Writing founder preference into company-wide knowledge
- Updating tasks without preserving the reason anywhere
- Logging the decision historically but forgetting to update the active state
