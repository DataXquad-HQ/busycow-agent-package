---
name: preparing-customer-meetings
description: >
  Prepare concise, source-backed briefs for customer or prospect meetings using
  invite context, CRM pipeline state, prior interactions, account research, and
  conservative attendee enrichment. Use when the Sales Rep asks for meeting prep,
  a prospect call brief, or a daily external-meetings digest.
triggers:
  - "meeting prep"
  - "prospect call prep"
  - "pre-meeting brief"
  - "prepare me for the call"
  - "meeting with customer tomorrow"
  - "help me prepare for the meeting"
  - "daily meeting digest"
version: "1.0"
---

# Preparing Customer Meetings

## When to Use

Use for customer-facing or clearly account-related meetings only.
This includes prospect calls, partner calls, demos, renewals, and external stakeholder meetings.
Do not use for internal 1:1s, hiring interviews, or generic meeting prep with no account anchor.

## Purpose

Give the Sales Rep a **two-minute scan brief** that answers:
- who is in the meeting
- what matters commercially
- what history and risk matter most
- what angle to take next

## Modes

1. **Single-meeting brief** — one specific call, invite, company, or opportunity
2. **Daily digest** — all external meetings for a given day, in chronological order

## Steps

1. **Start from the meeting source**
   - If the user gives an invite, date, or attendee list, use that first.
   - If the request is day-based, gather the day's external meetings first.
   - If there is **no invite or calendar object**, but there is a clear opportunity/account anchor, you may still produce a prep brief. In that case, explicitly label meeting timing, attendee assumptions, and agenda as gaps or working assumptions rather than implied facts.

2. **Load company and business-line context before external research**
   Read the relevant business-line / company vault pages first:
   - `[GBRAIN_VAULT]/internal/business-lines/geokernel/icp.md`
   - `[GBRAIN_VAULT]/internal/business-lines/geokernel/strategy.md`
   - `[GBRAIN_VAULT]/internal/business-lines/geokernel/product.md`
   - `[GBRAIN_VAULT]/internal/business-lines/geokernel/gtm.md`
   - `[GBRAIN_VAULT]/internal/company/overview.md`

3. **Resolve the commercial anchor**
   Identify whether this meeting is tied to:
   - an existing Opportunity
   - an existing Partnership
   - an unqualified Lead / target account

4. **Pull current account truth**
   Use CRM and GBrain first for:
   - stage / status / next action
   - company context
   - known stakeholders
   - prior commitments, blockers, and open questions

5. **Pull continuity from prior interactions**
   Use available transcripts, notes, prior email threads, and CRM Engagements.
   Prefer verified internal history over fresh web research.

6. **Enrich attendees conservatively**
   Use public web search only to confirm title, function, or company context when confidence is high.
   If the identity match is weak, omit the enrichment and call out the gap.

7. **Build the brief**
   Default sections:
   - Meeting
   - Objective
   - Account snapshot
   - External attendees
   - What history says
   - Likely objections or tensions
   - Recommended strategy
   - Assets to bring
   - Open questions / gaps

   When recommending materials, distinguish between:
   - **verified existing assets** the team already has
   - **asset types to bring if available** when existence is not confirmed from CRM, docs, or user context

8. **If no usable agenda exists**
   Add a short **Recommended agenda** instead of pretending one exists.

## Output Pattern

Keep each section to 1–3 bullets by default.
Optimize for actionability, not exhaustiveness.

## References

Read these when the request needs more structure:
- `references/output-patterns.md` — brief shapes for single-meeting and daily-digest outputs
- `references/source-priority.md` — how to anchor the brief in internal truth before enrichment

## Quality Bar

Before returning the brief:
- Every commercial claim tied to CRM, GBrain, prior interaction notes, or explicit user context?
- Facts and inference separated — e.g. `Verified:` vs `Based on prior interactions, this suggests...`?
- Attendee titles and roles only included when confidently matched?
- Recommended strategy specific to this meeting's stage and objective — not generic "build rapport" advice?
- If the agenda is missing, clearly labelled as `Recommended agenda` rather than implied fact?

If any check fails, tighten the brief before returning.

## Fallback Behavior

- **If CRM is unavailable**: build the brief from user-provided context + GBrain + public evidence; label stage/status as unverified.
- **If GBrain is unavailable**: use CRM + user context; note that deeper account memory was unavailable.
- **If prior interaction history is thin**: state that continuity is limited and bias toward present-tense prep.
- **If attendee identity cannot be confidently resolved**: omit the enrichment instead of guessing.
- **If there is no invite or calendar object**: produce an **opportunity-anchored prep brief** instead of refusing the task; clearly mark meeting timing, attendee list, and agenda as assumptions or gaps.
- **If recommended materials are not confirmed to exist**: phrase them as `If available:` asset types rather than implying the team already has them ready.
- **If the meeting is not clearly customer-facing**: say this skill is the wrong tool and stop.

## Pitfalls

- Do not over-research a weakly qualified meeting.
- Do not generate new assets inside this skill — only recommend which existing assets to bring.
- Do not guess objections, titles, procurement state, or decision process.
- Keep the output short enough that the Sales Rep will actually read it before the meeting.
