---
name: reviewing-sales-forecast
description: >
  Review forecasted opportunities with hygiene-first checks, risk analysis,
  and recommendation posture using CRM truth plus the freshest supporting evidence.
  Use when the Sales Rep asks for forecast review, commit risk, swing opportunities,
  or whether a set of opportunities really belongs in this period.
triggers:
  - "forecast review"
  - "sales forecast"
  - "which opportunities will close"
  - "commit risk"
  - "how does this quarter's forecast look"
  - "which opportunities are risky"
version: "1.0"
---

# Reviewing Sales Forecast

## When to Use

Use for forecast conversations about a defined period, owner, or set of late-stage opportunities.
This is not a top-of-funnel pipeline report; it is a **close-confidence review**.

## Purpose

Judge whether forecasted opportunities belong in the current period, what is fragile, and what should move up or down.

## Steps

1. **Define the forecast scope**
   Resolve the period, business line, owner, or explicit opportunity set.

2. **Pull CRM truth first**
   For each scoped opportunity, collect:
   - stage
   - amount
   - close date
   - probability
   - next action
   - latest status summary
   - latest update timestamp

3. **Inspect hygiene before conviction**
   Check whether:
   - close date is current and believable
   - next step exists and is concrete
   - stage matches the actual state described in notes
   - latest evidence is recent enough to trust

4. **Assess forecast risk**
   For each opportunity, review:
   - timing credibility
   - stakeholder coverage
   - decision-process visibility
   - technical validation
   - procurement / commercial blockers

5. **Separate posture categories**
   Classify each opportunity into one of:
   - keep / commit
   - watch closely
   - downgrade confidence
   - remove from this period

6. **Identify swing opportunities**
   Highlight the few opportunities where movement would materially change the forecast.

## Output Pattern

- Forecast snapshot
- Commit / keep
- Watch list
- Downgrade or slip candidates
- Swing opportunities
- Recommended manager actions

## References

Read as needed:
- `references/forecast-rubric.md` — commit / watch / downgrade / remove posture rules

## Quality Bar

Before returning the review:
- Every confidence judgment tied to a specific evidence lane, not a vibe?
- Hygiene problems surfaced before strategic interpretation?
- `Commit` style language used only when timing and next-step evidence are both credible?
- Slip/downgrade recommendations explain what is missing or weak?
- Coverage or weighted-forecast figures labelled as estimates when benchmark probabilities are used?

If any check fails, reduce certainty and say why.

## Fallback Behavior

- **If CRM is unavailable**: do not perform a forecast review from memory.
- **If notes/transcripts are missing**: do a field-level hygiene review only and say that deeper evidence was unavailable.
- **If the period is not specified**: default to the current period but label the assumption.
- **If opportunities lack amount or close date**: keep them in a data-gap section instead of forcing them into forecast posture.

## Pitfalls

- Do not let big opportunity amount alone imply close confidence.
- Do not accept stale close dates at face value.
- Do not bury data quality problems under narrative commentary.
- Forecast review is about what belongs in period, not a generic opportunity summary.
