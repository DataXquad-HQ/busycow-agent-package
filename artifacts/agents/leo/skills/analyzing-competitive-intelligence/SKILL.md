---
name: analyzing-competitive-intelligence
description: >
  Build competitor analysis, comparison matrices, and objection-handling briefs
  from user-provided materials, public evidence, and account context. Use when the
  Sales Rep asks for competitive intelligence, battlecards, competitor comparison,
  or how to position against a named rival in a live opportunity.
triggers:
  - "competitive intelligence"
  - "battlecard"
  - "compare us with"
  - "objection handling"
  - "competitor analysis"
  - "compare with competitors"
version: "1.0"
---

# Analyzing Competitive Intelligence

## When to Use

Use when a live opportunity or target account needs sharper competitor positioning.
This skill is for commercial positioning, not generic market landscape essays.

## Purpose

Produce a grounded competitor view the BD team can actually use in conversation:
- how the competitor is likely positioned
- where our edge is real
- what objections or traps to anticipate
- what not to claim

## Steps

1. **Start from our product truth**
   Read the relevant internal product, strategy, ICP, and GTM files first.
   Do not evaluate a competitor before grounding in what [Business Line] or the relevant business line actually is.

2. **Gather seller context**
   Resolve:
   - which opportunity / account this is for
   - which competitor(s) matter
   - what decision the analysis is supposed to support

3. **Build competitor dossiers**
   For each competitor, collect verified evidence on:
   - product scope
   - target segment
   - deployment model
   - procurement shape
   - differentiators they likely claim

4. **Build the comparison matrix**
   Compare only dimensions that matter to the live situation:
   - offline capability / field constraints
   - implementation model
   - data sovereignty / deployment control
   - workflow fit
   - pricing or commercial shape if verified

5. **Translate into selling guidance**
   Produce:
   - likely objections we will hear
   - strongest truthful counters
   - situations where the competitor may actually be stronger
   - what message angle to use with this account

## Output Pattern

- Situation context
- Competitor summary
- Comparison matrix
- Likely objections and counters
- Recommended positioning angle
- Red lines / claims to avoid

## References

Read as needed:
- `references/comparison-matrix.md` — matrix dimensions, evidence-quality labels, and objection-handling pattern

## Quality Bar

Before returning the analysis:
- Every comparison row tied to verified evidence or clearly labelled inference?
- No unsupported claims about competitor pricing, deployments, customers, or product gaps?
- Our own strengths phrased in account-relevant language, not generic brand claims?
- Any area where the competitor may be stronger surfaced honestly?
- Recommended positioning angle specific to this account and its likely priorities?

If any check fails, narrow the scope and ground the output harder.

## Fallback Behavior

- **If external competitor evidence is thin**: say so and return a partial matrix rather than inventing detail.
- **If our own product context is missing**: stop and load internal product context first.
- **If no live account context is provided**: deliver a generic competitor brief, but explicitly label it as non-account-specific.

## Pitfalls

- Do not write a giant market report when the user really needs two conversation angles.
- Do not use feature-checklist thinking without tying it to customer priorities.
- Do not turn inference into fact.
- Do not assume a competitor is relevant just because it shares a category label.