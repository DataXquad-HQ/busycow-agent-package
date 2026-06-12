---
name: enriching-leads
description: >
  Use when a Company is added to the CRM and needs web research, or when user
  asks to refresh existing Company intel. Searches the company domain/name,
  extracts key facts (overview, industry, size, contact info), and writes
  findings into the Twenty CRM company notes. Can be triggered manually or
  automatically after account-onboarding.
  Use when user says "幫我查一下這家公司", "enrich this company", "補一下資料",
  "查這間公司", or automatically after account-onboarding completes.
  Supports three enrichment depths (basic/standard/deep) based on contact status.
triggers:
  - "enrich"
  - "幫我查一下這家公司"
  - "補一下資料"
  - "查這間公司"
  - "enriching"
  - "refresh company info"
version: "3.0"
author: Leo (BD Director Agent)
---

# Enriching Leads

## Purpose

After a Company is created in Twenty CRM, run web research to build a factual company profile. Write findings into the company's notes in Twenty CRM. Update the GBrain page with the enriched overview.

**Two trigger modes:**
1. **Automatic** — called immediately after `account-onboarding` completes (Phase 5)
2. **Manual** — sales rep asks "查一下這家公司" or "補資料"

---

## Enrichment Depth by Contact Status

Enrichment depth is calibrated to **Person status**:

| Status | When enrichment runs | Depth | Searches |
|---|---|---|---|
| `PROSPECT` | At Prospect creation (before cold email) | Basic | Max 2 — overview, industry, website |
| `LEAD` (cold list origin) | At LEAD conversion (reply received) | Standard | Max 3 — overview, size, fit signals, notable clients |
| `LEAD` (inbound / referral) | At LEAD conversion | Deep | Max 4 — full background, pain points, decision-maker hints |
| `LEAD` (human-introduced) | Immediately after onboarding | Deep | Max 4 — same as above |

When called from `lead-list-triage`: always `basic`.
When called from `account-onboarding` (human-introduced): always `deep`.
When called manually: default to `standard` unless specified.
When called from monthly cron: `basic` for all.

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001`
**GraphQL endpoint:** `http://localhost:3001/graphql`

**Token:**
```bash
TOK=$(grep TWENTY_TOKEN ~/.hermes/profiles/[agent]/.env | cut -d= -f2)
```

Use `curl` for all CRM calls — no approval prompts.

---

## Step 1: Identify the Company

Get the company name and domain. Either:
- Passed in from `account-onboarding` (company name + Twenty company `id` + domain if known)
- Sales rep names the company explicitly

If called manually, find the company in Twenty first:
```bash
TOK=$(grep TWENTY_TOKEN ~/.hermes/profiles/[agent]/.env | cut -d= -f2)

curl -s -X POST http://localhost:3001/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer *** \
  -d '{"query":"{ companies(filter:{name:{like:\"%[COMPANY_NAME]%\"}}) { edges { node { id name domainName { primaryLinkUrl } companyOverview } } } }"}'
```

---

## Step 2: Web Search

**basic** (max 2 searches):
```
Search 1: "[company_name]" company overview
Search 2: site:[domain] (only if domain known)
```
Extract: overview (2-3 sentences), industry, size, website.

**standard** (max 3 searches):
```
Search 1: "[company_name]" company overview about
Search 2: site:[domain] OR "[company_name]" [country] business
Search 3: "[company_name]" clients customers case study
```
Extract: all basic + notable clients or projects + product fit signals.

**deep** (max 4 searches):
```
Search 1: "[company_name]" company overview about
Search 2: site:[domain] OR "[company_name]" [country] business
Search 3: "[company_name]" pain points challenges problems
Search 4: "[company_name]" leadership team decision makers
```
Extract: all standard + pain point signals + talking points + decision-maker hints.

### Industry Options (Twenty)

**`industry` is a single ENUM value — not an array.** Always verify current values with:
```bash
TOK=$(grep TWENTY_TOKEN ~/.hermes/profiles/[agent]/.env | cut -d= -f2)
curl -s -X POST http://localhost:3001/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer *** \
  -d '{"query":"{ __type(name: \"CompanyIndustryEnum\") { enumValues { name } } }"}'
```

**Current known values** (update this list when new ones are added in Twenty):
| CRM Value | Use For |
|-----------|---------|
| `GOVERNMENT_PUBLIC` | Government bodies, statutory boards, municipal authorities |
| `WATER_UTILITIES` | Water utilities, drainage, flood management, sewage |
| `TECH_SAAS` | Software companies, AI platforms, SaaS businesses |
| `MANUFACTURING_TRADING` | Manufacturing, trading, distribution, OEM/ODM |
| `LOGISTICS_TRANSPORT` | Logistics, transport, fleet management |
| `CONSTRUCTION_PROPERTY` | Construction, real estate, civil engineering |
| `FINANCE_INSURANCE` | Finance, insurance, banking |
| `EDUCATION` | Schools, training, edtech |
| `HEALTHCARE` | Healthcare, eldercare, clinics, medical devices |
| `RETAIL_ECOMMERCE` | Retail, e-commerce, consumer goods |
| `FB_HOSPITALITY` | F&B, hospitality, tourism |
| `OTHER` | Doesn't fit above |

> **Adding a new industry:** Add it in Twenty CRM (Settings → Data model → Company → industry field), then update this table.

---

## Step 3: Write to Twenty CRM

Use `curl` — no approval prompts.

```bash
TOK=$(grep TWENTY_TOKEN ~/.hermes/profiles/[agent]/.env | cut -d= -f2)

# Update company record
# industry = single ENUM value (not array)
cat > /tmp/enrich_payload.json << PAYLOAD
{"query": "mutation { updateCompany(id: \"[COMPANY_ID]\", data: { companyOverview: \"[OVERVIEW]\", industry: [INDUSTRY_ENUM], country: [COUNTRY_ENUM], domainName: { primaryLinkUrl: \"https://[WEBSITE]\", primaryLinkLabel: \"\" } }) { id name companyOverview } }"}
PAYLOAD

curl -s -X POST http://localhost:3001/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer *** \
  -d @/tmp/enrich_payload.json
```

Then add a **Note** with full enrichment detail:

```bash
cat > /tmp/note_payload.json << PAYLOAD
{"query": "mutation { createNote(data: { title: \"Company Enrichment — [DATE]\", body: \"[FINDINGS]\", companyTargets: { reconnectWith: [\"[COMPANY_ID]\"] } }) { id } }"}
PAYLOAD

curl -s -X POST http://localhost:3001/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer *** \
  -d @/tmp/note_payload.json
```

Note body should include: company description · size estimate · key clients or use cases · product fit signals · source · date enriched.

---

## Step 4: Update GBrain Page

```python
# Read existing page first
page = mcp_gbrain_get_page(slug="companies/[company-slug]")

# Update with enrichment
mcp_gbrain_put_page(
    slug="companies/[company-slug]",
    content=updated_content_with_enrichment
)
```

If no GBrain page exists yet, create one (see `account-onboarding` Phase 6 for format).

---

## Step 5: Report Back (Manual Mode Only)

```
🔍 {Company Name} 資料補充完成：

概述：{2-sentence summary}
產業：{industry}
規模：{size if found}
網站：{website}
產品 Fit：{which products might fit, or "目前看不出明顯 fit"}

已更新 Twenty CRM ✅
```

When triggered automatically from `account-onboarding` — silent, no confirmation message.

---

## Monthly Re-enrichment (Cron Mode)

When running as `account-enrichment-monthly` cron:
1. Pull all companies with `lastEnrichedDate` > 30 days ago (or null)
2. Skip `OPT_OUT` companies — never re-enrich
3. Focus on `PROSPECT` and `LEAD`; skip `CLIENT` and `PARTNER` unless requested
4. For each eligible company: run Steps 2–4
5. Deliver summary to Lark IM: "本月 re-enriched {N} 家公司"

---

## Pitfalls

1. **No confirmation in automatic mode** — when called from `account-onboarding`, write directly to CRM + GBrain.

2. **Manual mode confirms first** — show findings before writing; sales rep may want to correct.

3. **`industry` is a single ENUM, not array** — pass `industry: MANUFACTURING_TRADING`, not `industry: ["MANUFACTURING_TRADING"]`.

4. **`domainName` format** — `{ primaryLinkUrl: "https://...", primaryLinkLabel: "" }`. Always include `https://`.

5. **Note body is plain text** — no markdown in Twenty Notes body.

6. **Fit signals are required** — if no fit found, write "No immediate product fit identified." Don't skip.

7. **If web search returns nothing** — write: "Enrichment attempted on {date}. Insufficient public data. Manual research recommended."

8. **Use `curl` not `python3 -c`** — curl needs no approval. Always read token from `.env`.
