---
name: drafting-call-followups
description: >
  Turn a customer or prospect meeting, transcript, or grounded notes into a
  follow-up package with recap, next steps, external follow-up draft, and CRM-ready
  internal summary. Use when the Sales Rep needs help after a meeting before logging
  or sending the next message.
triggers:
  - "call follow-up"
  - "meeting follow-up"
  - "draft the recap"
  - "write the follow-up email"
  - "post-meeting follow-up"
  - "help me organize meeting follow-up"
version: "1.0"
---

# Drafting Call Follow-Ups

## When to Use

Use after an external meeting, call, demo, or substantive email exchange.
This skill is for **drafting and synthesis**. It does not send outreach or write CRM by itself.

## Purpose

Convert messy post-meeting evidence into a seller-ready package:
- what happened
- what the other side committed to
- what we committed to
- what should be sent next
- what should be logged internally

## Steps

1. **Choose the best verified source**
   Prefer transcript or grounded notes over memory.
   If only rough notes exist, use them but label uncertainty.

2. **Pull current opportunity context**
   Load the relevant opportunity / partnership state so the follow-up reinforces the actual motion.

3. **Extract meeting outputs**
   Capture:
   - decisions
   - open questions
   - customer asks
   - our promises
   - next-step owner and timing

4. **Draft the external follow-up**
   Write a concise, professional recap email or message draft.
   Keep it action-oriented and specific.

5. **Draft the internal summary**
   Produce a CRM-ready note summarizing what changed commercially.

## Output Pattern

- Meeting recap
- Confirmed next steps
- External follow-up draft
- Internal CRM summary draft
- Evidence gaps or ambiguities

## References

Read as needed:
- `references/output-pattern.md` — meeting recap, external follow-up, and internal CRM summary structure

## Quality Bar

Before returning the package:
- Every stated commitment or decision grounded in transcript, notes, or explicit user correction?
- External follow-up draft concise and commercially useful — not a transcript dump?
- Internal summary highlights what changed in the opportunity, not just what was discussed?
- Ambiguities or unresolved items clearly marked instead of flattened into certainty?
- No sending language that implies the message was already delivered?

If any check fails, tighten the package.

## Fallback Behavior

- **If transcript or notes are weak**: draft from available evidence but label it as a best-effort summary.
- **If opportunity context is missing**: produce the follow-up package, but say the commercial summary could not be tied to a CRM record.
- **If there is no clear next step**: say so explicitly and propose a candidate next step instead of pretending one was agreed.

## Pitfalls

- Do not confuse recap with strategy; keep the package close to what actually happened.
- Do not fabricate commitments from polite language.
- Do not write CRM as if this skill already updated it.
- Short, accurate follow-up beats comprehensive but blurry notes.