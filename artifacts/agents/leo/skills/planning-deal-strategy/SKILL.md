---
name: planning-deal-strategy
description: >
  Build a post-discovery opportunity strategy pack with a deal map, stakeholder
  map, procurement and delivery risks, and prioritized next actions from grounded
  evidence. Use when the Sales Rep asks for deal strategy, wants to think through
  a specific opportunity, or needs a recovery plan for a stuck opportunity.
triggers:
  - "deal strategy"
  - "opportunity strategy"
  - "how do we win this"
  - "stuck opportunity"
  - "help me think about how to approach this case"
  - "how to push this opportunity"
version: "1.0"
---

# Planning Deal Strategy

## When to Use

Use after discovery has started and there is enough evidence to reason about a real opportunity.
Do not use for first-touch prospecting or generic account research.

## Purpose

Turn scattered account evidence into a **winning plan**:
- what the opportunity really is
- who matters in the buying group
- what blockers could kill it
- what the next moves should be this week

## Steps

1. **Load product and GTM context first**
   Read the relevant internal [Business Line] and company context files before judging fit or strategy.

2. **Resolve the opportunity anchor**
   Identify the exact Opportunity in CRM.
   If multiple matches exist, stop and disambiguate rather than guessing.

3. **Pull evidence lanes**
   Use CRM, GBrain, prior emails/notes, and any transcript or call summary available.
   Separate:
   - verified stage/status facts
   - stakeholder evidence
   - procurement/commercial evidence
   - technical validation evidence

4. **Build the opportunity map**
   Summarize:
   - current stage and why
   - desired end state this quarter
   - key milestones still needed
   - strongest reason this opportunity could advance

5. **Build the stakeholder map**
   For each important stakeholder, capture:
   - role
   - likely motivation
   - current stance: supportive / neutral / unknown / blocker
   - evidence source

6. **Build the risk register**
   Include only risks that could materially change the outcome:
   - timing credibility
   - stakeholder coverage gaps
   - procurement / budget / security / legal blockers
   - product-fit or deployment risk
   - partner dependency risk

7. **Generate prioritized next actions**
   Recommend 3–5 actions max.
   Each action must specify:
   - owner
   - why this action matters now
   - what signal would tell us it worked

## Output Pattern

- Opportunity snapshot
- Stakeholder map
- Risks and blockers
- Win path
- This week's recommended actions
- Evidence gaps

## References

Read as needed:
- `references/risk-map.md` — material-risk categories and recommended strategy posture

## Quality Bar

Before returning the strategy pack:
- Every key risk tied to a specific piece of evidence, not generic sales caution?
- Stakeholder map distinguishes verified influence from inferred influence?
- Next actions are few, prioritized, and tied to the opportunity's current stage?
- Missing evidence called out explicitly instead of papered over with confidence?
- Recommendations framed as **Based on CRM activity, this suggests…** when interpretive?

If any check fails, simplify and ground the strategy pack.

## Fallback Behavior

- **If CRM is unavailable**: do not pretend stage or field values are current; build a partial strategy from notes and user context only.
- **If GBrain is unavailable**: proceed from CRM and user-provided artifacts; note the missing external entity context.
- **If there is not enough evidence for stakeholder mapping**: mark stakeholders as unknown rather than inventing motivations.
- **If the opportunity is still too early-stage**: say so and recommend switching to scouting, account intelligence, or meeting prep instead.

## Pitfalls

- Do not confuse account research with opportunity strategy.
- Do not invent a buying committee because enterprise deals often have one.
- Do not produce ten actions; fewer, sharper actions are better.
- Do not treat stale notes as fresh evidence without labelling them.