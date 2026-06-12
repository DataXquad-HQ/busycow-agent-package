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
  Supports three enrichment depths (basic/standard/deep) based on prospect intent level.
triggers:
  - "enrich"
  - "幫我查一下這家公司"
  - "補一下資料"
  - "查這間公司"
  - "enriching"
  - "refresh company info"
version: "2.1"
author: Leo (BD Director Agent)
---

# Enriching Leads

## Purpose

After a Company is created in Twenty CRM, run web research to build a factual company profile. Write findings into the company's notes in Twenty CRM. Update the GBrain page with the enriched overview.

**Two trigger modes:**
1. **Automatic** — called immediately after `account-onboarding` completes (Phase 5)
2. **Manual** — sales rep asks "查一下這家公司" or "補資料"

---

## Enrichment Depth by Intent Level

The depth of enrichment depends on how the prospect entered the pipeline:

| Intent level | Entry path | What to extract |
|---|---|---|
| `basic` | Cold list (LinkedIn export, event exhibitor list) | Company overview (2-3 sentences), industry, size estimate, website. No more than 2 web searches. |
| `standard` | Newsletter subscriber, inbound referral | All basic fields + notable clients or projects + any product fit signals |
| `deep` | Website enquiry / form fill, Human-introduced contact | All standard fields + pain point signals + talking points for first outreach + decision-maker hints if findable |

When called from `lead-list-triage`: always use `basic`.
When called from `account-onboarding` (human-introduced): always use `deep`.
When called manually by sales rep: default to `standard` unless they specify.
When called from monthly cron: use `basic` for all companies.

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001`
**GraphQL endpoint:** `http://localhost:3001/graphql`

---

## Step 1: Identify the Company

Get the company name and domain. Either:
- Passed in from `account-onboarding` (company name + Twenty company `id` + domain if known)
- Sales rep names the company explicitly

If called manually, find the company in Twenty first:
```graphql
query {
  companies(filter: { name: { like: "%{company_name}%" } }) {
    edges {
      node {
        id
        name
        domainName { primaryLinkUrl }
        companyOverview
      }
    }
  }
}
```

---

## Step 2: Web Search

Search depth depends on `intent_level`:

**basic** (max 2 searches):
```
Search 1: "{company_name}" company overview
Search 2: site:{domain} (only if domain known)
```
Extract: company overview (2-3 sentences), industry, size, website. Stop here.

**standard** (max 3 searches):
```
Search 1: "{company_name}" company overview about
Search 2: site:{domain} OR "{company_name}" {country} business
Search 3: "{company_name}" clients customers case study
```
Extract: all basic fields + notable clients or projects + product fit signals.

**deep** (max 4 searches):
```
Search 1: "{company_name}" company overview about
Search 2: site:{domain} OR "{company_name}" {country} business  
Search 3: "{company_name}" pain points challenges problems
Search 4: "{company_name}" leadership team decision makers
```
Extract: all standard fields + pain point signals + talking points + decision-maker hints if findable.

### Industry Options (Twenty)
| Option | Use For |
|--------|---------|
| GOVERNMENT | Government bodies, statutory boards, municipal authorities |
| WATER_UTILITIES | Water utilities, drainage, flood management, sewage |
| TECH_SAAS | Software companies, AI platforms, SaaS businesses |
| MANUFACTURING | Manufacturing, trading, distribution, OEM |
| LOGISTICS | Logistics, transport, fleet management |
| CONSTRUCTION | Construction, real estate, civil engineering |
| FINANCE | Finance, insurance, banking |
| EDUCATION | Schools, training, edtech |
| HEALTHCARE | Healthcare, eldercare, clinics, medical devices |
| RETAIL | Retail, e-commerce, consumer goods |
| HOSPITALITY | F&B, hospitality, tourism |
| OTHER | Doesn't fit above |

---

## Step 3: Write to Twenty CRM

Update the company record with enriched data:

```graphql
mutation {
  updateCompany(
    id: "{company_id}"
    data: {
      companyOverview: "{enriched_description}"
      industry: ["{industry}"]
      country: "{country}"
      domainName: { primaryLinkUrl: "{website}", primaryLinkLabel: "" }
      companyEmail: { primaryEmail: "{contact_email_if_found}" }
    }
  ) {
    id
    name
    companyOverview
  }
}
```

Then add a **Note** to the company with full enrichment detail:

```graphql
mutation {
  createNote(data: {
    title: "Company Enrichment — {date}"
    body: "{full_enrichment_findings}"
    companyTargets: { reconnectWith: ["{company_id}"] }
  }) {
    id
  }
}
```

Note body should include:
- Company description
- Size / headcount estimate
- Key clients or use cases (if found)
- Product fit signals (which of your products might fit this company's needs)
- Source of information (web search, LinkedIn, etc.)
- Date enriched

---

## Step 4: Update GBrain Page

If a GBrain page exists for this company, update the Recent Insights section:

```python
# Read existing page
page = mcp_gbrain_get_page(slug=f"companies/{company_slug}")

# Add enrichment to Recent Insights section
mcp_gbrain_put_page(
    slug=f"companies/{company_slug}",
    content=updated_content_with_enrichment
)
```

If no GBrain page exists yet, create one (see `account-onboarding` Phase 6 for format).

---

## Step 5: Report Back (Manual Mode Only)

When triggered manually by the sales rep, confirm what was found:

```
🔍 {Company Name} 資料補充完成：

概述：{2-sentence summary}
產業：{industry}
規模：{size if found}
網站：{website}
產品 Fit：{which products might fit, or "目前看不出明顯 fit"}

已更新 Twenty CRM ✅
```

When triggered automatically from `account-onboarding`, no confirmation message — silent completion.

---

## Monthly Re-enrichment (Cron Mode)

When running as `account-enrichment-monthly` cron:
1. Pull all companies from Twenty with `lastEnrichedDate` > 30 days ago (or no enrichment date)
2. For each: run Steps 2–4
3. Deliver a summary to Lark IM: "本月 re-enriched {N} 家公司"

---

## Pitfalls

1. **No user confirmation needed for automatic mode** — when called from `account-onboarding`, write directly. Speed of capture matters more than review.

2. **Manual mode still confirms** — if the sales rep triggered enrichment manually, show findings before writing (they may want to correct something).

3. **Industry is MULTI_SELECT** — pass as array: `["WATER_UTILITIES"]`.

4. **`domainName` format** — `{ primaryLinkUrl: "https://...", primaryLinkLabel: "" }`. Always include `https://`.

5. **Note body is plain text** — Twenty Notes body is text, not markdown. Keep it readable without formatting.

6. **Fit signals are optional** — if no clear fit is found, write "No immediate product fit identified based on current description." Don't skip this field.

7. **If web search returns no useful results** — write a note: "Enrichment attempted on {date}. Insufficient public data found. Manual research recommended." Don't leave enrichment blank.
