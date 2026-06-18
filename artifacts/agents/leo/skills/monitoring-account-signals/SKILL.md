---
name: monitoring-account-signals
description: >
  Monitor named accounts or owner portfolios for fresh commercial signals and
  turn them into evidence-backed account intelligence with explicit signal type,
  recency, confidence, and recommended next step. Use when the Sales Rep asks to
  watch a target account list, scan for why-now changes, or review recent account momentum.
triggers:
  - "monitor these accounts"
  - "account signals"
  - "why now"
  - "watchlist"
  - "help me monitor these companies"
  - "what recent account signals are there"
version: "1.0"
---

# Monitoring Account Signals

## When to Use

Use when the Sales Rep already has a named account set and wants **fresh movement signals**, not a one-time foundational enrich.
This is especially useful for watchlists, owner portfolios, and high-value targets.

## Purpose

Convert noisy updates into actionable signal cards that answer:
- what changed
- why it matters
- how fresh it is
- what we should do next

## Signal Taxonomy

Normalize retained findings into one of these types only:
- `momentum`
- `expansion_opportunity`
- `churn/risk`
- `blocker/dependency`
- `stakeholder_movement`
- `upcoming_commitment_or_deadline`
- `evidence_gap`

Each retained signal should include:
- summary
- source
- recency: fresh / recent / stale
- confidence: high / medium / low
- recommended next step

## Steps

1. **Resolve the account scope**
   Work from explicit named accounts, CRM owner portfolio, or a watchlist.

2. **Load internal context first**
   Read relevant product / GTM / strategy context before judging whether a signal matters.

3. **Pull current CRM and GBrain baseline**
   Understand existing stage, current motion, and prior relationship history first.

4. **Collect fresh evidence**
   Use official company sources, news, public signals, and any user-provided artifacts.
   External research should sharpen the account view, not replace CRM truth.

5. **Normalize and suppress noise**
   Keep only signals that could realistically change outreach timing, meeting prep, opportunity strategy, or account priority.

6. **Recommend next step**
   Every meaningful signal should point to a next move: monitor, reach out, prep, escalate, or hold.

## Output Pattern

- Account
- Signal type
- What changed
- Why it matters
- Recency / confidence
- Recommended next step

## References

Read as needed:
- `references/signal-taxonomy.md` — allowed signal types, recency, confidence, and noise filter

## Quality Bar

Before returning account signals:
- Every retained signal specific enough to change behavior, not just interesting trivia?
- Recency and confidence explicitly labelled?
- Recommended next step traceable to the signal itself?
- Noise, PR fluff, and low-value updates suppressed?
- Existing in-flight opportunity motion checked before suggesting brand-new outreach?

If any check fails, reduce the signal set and sharpen it.

## Fallback Behavior

- **If CRM is unavailable**: you may still return external signals, but label internal motion status as unverified.
- **If GBrain is unavailable**: use CRM + public evidence only; note the missing historical context.
- **If no fresh evidence is found**: say so directly; `no change` is a valid result.

## Pitfalls

- Do not confuse account monitoring with foundational enrichment.
- Do not surface weak signals with strong language.
- Do not recommend outreach when there is already live motion unless the signal clearly changes the situation.