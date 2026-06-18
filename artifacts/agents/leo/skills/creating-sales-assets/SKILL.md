---
name: creating-sales-assets
description: >
  Create tailored sales assets — one-pagers, executive summaries, follow-up docs,
  lightweight landing-page copy, or workflow narratives — from opportunity context,
  audience, and product truth. Use when the Sales Rep asks for a customer-facing
  asset to support an active opportunity or meeting.
triggers:
  - "create an asset"
  - "one-pager"
  - "customer-facing doc"
  - "executive summary"
  - "help me create a one-page summary"
  - "make some materials for the customer"
version: "1.0"
---

# Creating Sales Assets

## When to Use

Use when the BD team needs a **customer-facing artifact** tied to a live situation:
meeting follow-up, executive summary, partner explainer, one-pager, or workflow narrative.

## Purpose

Turn deal context into a polished asset that is:
- specific to the audience
- grounded in actual product truth
- commercially useful right now

## Steps

1. **Define the asset request**
   Resolve:
   - audience
   - purpose
   - format
   - live opportunity or account context

2. **Load {{COMPANY_NAME}} and product truth first**
   Read the relevant internal strategy, product, GTM, and company overview files.
   If the asset is for [Business Line], use the [Business Line] pages as the primary source of truth.

3. **Pull account-specific context**
   Use CRM, GBrain, prior meeting notes, and any user-provided brief.
   Prefer known customer pain and opportunity context over generic marketing language.

4. **Select the output shape**
   Examples:
   - executive summary
   - one-pager
   - partner explainer
   - workflow story
   - lightweight landing-page copy

5. **Draft the asset**
   Write in a customer-ready tone.
   Keep claims tight, relevant, and supportable.

6. **If visual production is requested**
   Produce the copy/structure first.
   Only generate files or visuals if the user explicitly wants the asset materialized in that format.

## Output Pattern

Return:
- the asset itself
- a short note explaining intended use and audience
- any unsupported claim or missing fact that still needs human confirmation

## References

Read as needed:
- `references/asset-shapes.md` — choose the right customer-facing asset structure for the audience and goal

## Quality Bar

Before returning the asset:
- Every product claim traceable to internal product truth or explicit user context?
- Asset tailored to the audience, not a generic company brochure?
- Tone appropriate to the format — executive summary vs technical workflow are not written the same way?
- Any customer-specific metric or outcome only included when verified?
- No invented logos, case studies, certifications, integrations, or deployment claims?

If any check fails, simplify and remove unsupported specificity.

## Fallback Behavior

- **If account context is thin**: create a reusable but clearly non-account-specific draft and label it that way.
- **If product truth is missing or ambiguous**: stop and ask for the missing product source instead of improvising.
- **If the user wants a visual file but no format is specified**: default to copy-first and say what format would be best next.

## Pitfalls

- Do not confuse a sales asset with a strategy memo.
- Do not force heavy personalization when evidence is weak.
- Do not write marketing fluff that the Sales Rep cannot defend live.
- Copy-first is safer than over-promising design output.