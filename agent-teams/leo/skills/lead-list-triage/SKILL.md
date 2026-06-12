---
name: lead-list-triage
version: 1.1
author: BD Lead Agent
description: >
  Use when the sales rep provides a prospect list (LinkedIn export, event list,
  referral batch, any format). Leo triages each company for fit, presents a
  Pursue/Monitor/Discard report, gets confirmation, then batch-onboards
  confirmed prospects into Twenty CRM.
triggers:
  - prospect list
  - triage list
  - LinkedIn export
  - event exhibitor list
  - batch onboard
  - 名單
  - 篩選名單
  - 展商清單
---

# Skill: Lead List Triage

## Purpose

Triage a prospect list provided by the sales rep. Assess fit for each company,
output a structured report (Pursue / Monitor / Discard), get confirmation, then
batch-onboard confirmed prospects into Twenty CRM as Company + Person records.

---

## Step 1: Parse the List

Accept the list in **any format**: CSV, Excel, pasted text, Markdown table, PDF, or raw copy-paste.

For each entry, extract:
- **Company name** (required)
- **Person name** (if present)
- **Title / Role** (if present)
- **Website / domain** (if present)
- **Notes** (any extra context the rep included)

> If the format is ambiguous, make a best-effort parse and explicitly note any assumptions made before proceeding to Step 2.

---

## Step 2: Web Research per Company

Use **Tavily web search** to quickly characterise each company.

**Run up to 2 searches per company** (speed over depth at triage stage):

| Search | Query template |
|--------|---------------|
| Primary | `{company_name} company overview` |
| Secondary (if domain known) | `site:{domain}` |

**Extract from results:**
- Industry / sector
- Company size / headcount estimate
- What they do and who they serve
- HQ location / geography

> Hard time-box: do not exceed 2 searches per company. Partial data is fine — capture what is found and move on.

---

## Step 3: Fit Assessment

For each company, assess fit against **[Product]**.

> ⚙️ **Install note:** Replace `[Product]` with the actual product name(s) when deploying this skill.

**Score each company as one of:**

| Score | Meaning |
|-------|---------|
| ✅ **Pursue** | Clear fit — worth initiating cold outreach now |
| 👀 **Monitor** | Possible fit — unclear or timing is uncertain |
| ❌ **Discard** | No meaningful fit — do not onboard |

Write **one concise rationale line** for each company explaining the score.

---

## Step 4: Output Triage Report

Present the following structured report to the sales rep before taking any CRM action:

```
📋 Triage Report — {list name} ({N} companies)

✅ PURSUE ({n})
1. {Company} — {industry}, {size} — {one-line rationale}
   Contact: {person name, title if known}
2. ...

👀 MONITOR ({n})
1. {Company} — {industry}, {size} — {one-line rationale}
   Contact: {person name, title if known}
2. ...

❌ DISCARD ({n})
1. {Company} — {one-line rationale}
2. ...

Ready to onboard PURSUE list? Reply YES to proceed, or adjust selections.
```

**Do not touch the CRM until Step 5 confirmation is received.**

---

## Step 5: Confirm with Sales Rep

Wait for an explicit response before onboarding anything.

**Accepted confirmation forms:**
- `YES` — onboard the full PURSUE list as reported
- `Yes, but skip #2` — onboard PURSUE minus item 2
- `Move #3 to Pursue` — promote that entry before onboarding
- `Move #1 to Discard` — remove that entry
- Any natural-language variant of the above

**Rules:**
- Only onboard what the sales rep explicitly confirms
- If the rep requests adjustments, acknowledge the changes, show the revised PURSUE list, and ask for final confirmation before proceeding
- If confirmation is ambiguous, ask a clarifying question

---

## Step 6: Batch Onboard Confirmed Prospects

Process each confirmed company against **Twenty CRM at `localhost:3001`**.

> ⚠️ Always use `localhost:3001`. Never use an external or production URL.

### 6a — Duplicate Check

Before creating any record, check whether the company already exists:

```graphql
query {
  companies(filter: { name: { like: "%{company_name}%" } }) {
    edges {
      node {
        id
        name
      }
    }
  }
}
```

- If a matching record is found → use the existing `id`, skip creation, note "already exists"
- If no match → proceed to creation (Step 6b)

### 6b — Create Company

```graphql
mutation {
  createCompany(data: {
    name: "{company_name}"
    domainName: { primaryLinkUrl: "{website}", primaryLinkLabel: "" }
    accountStatus: "COLD"
    accountType: ["PROSPECT"]
    country: "{country}"
    industry: ["{industry}"]
    companyOverview: "{brief_description}"
  }) {
    id
    name
  }
}
```

**Field notes:**
- `accountType` is a `MULTI_SELECT` — always pass as an array: `["PROSPECT"]`
- `domainName` format: `{ primaryLinkUrl: "https://...", primaryLinkLabel: "" }`
- `companyOverview`: use the one-line description from web research (Step 2)
- `country` / `industry`: use best-available data; omit field rather than guess if unknown

### 6c — Create Person (if name is known)

```graphql
mutation {
  createPerson(data: {
    name: { firstName: "{first}", lastName: "{last}" }
    jobTitle: "{title}"
    companyId: "{company_id}"
    source: "{source}"
  }) {
    id
  }
}
```

**Source mapping:**

| List origin | `source` value |
|-------------|---------------|
| LinkedIn export | `OUTBOUND_MAYA` (or `EVENT` if from a LinkedIn event) |
| Event exhibitor list | `EVENT` |
| Referral batch | `REFERRAL` |
| Unknown / unspecified | `OUTBOUND_MAYA` |

### 6d — Hand-off to Enrichment

After creating each record, **hand off to the `enriching-leads` skill** for deeper enrichment if:
- The rep requested enrichment, or
- The company is a high-priority PURSUE entry that warrants immediate intelligence gathering

Otherwise, enrichment will run as part of the standard Account Intelligence cycle.

### Large list handling

If the list contains **50 or more companies**, process in **batches of 20**:
1. Onboard batch 1 → report results
2. Pause and confirm the rep wants to continue
3. Proceed with next batch

---

## Step 7: Confirm Completion + Handoff to Lead Nurturing

After all confirmed companies are onboarded:

### 7a — Update status
All newly created Company records are already set to `accountStatus: COLD`. No further update needed.

### 7b — Trigger enrichment
For each newly created Company, hand off to `enriching-leads` skill with `intent_level: basic`.
This is a background operation — do not wait for it to complete before confirming to the sales rep.

### 7c — Confirm to sales rep

```
✅ Onboarded {N} companies into CRM:
- {Company A} (created) 
- {Company B} (already existed — linked)
- {Company C} (created)
- ...

All new records: COLD / PROSPECT.

📬 Next: Leo will draft cold outreach for these {N} companies.
Ready to start outreach now, or wait for your go-ahead?
```

If the sales rep says go ahead → invoke `lead-nurturing` skill (C3) with the list of newly onboarded Person IDs.
If the sales rep says wait → leave records as COLD. C3 monthly cron will pick them up automatically.

If any records failed (e.g., GraphQL error), list them separately and suggest a retry or manual review.

---

## Pitfalls & Rules

| # | Rule |
|---|------|
| 1 | **Always check for duplicates** before creating a Company record |
| 2 | `accountType` is `MULTI_SELECT` — pass as array: `["PROSPECT"]` |
| 3 | `domainName` must use the object format: `{ primaryLinkUrl: "https://...", primaryLinkLabel: "" }` |
| 4 | **Never onboard without explicit sales rep confirmation** |
| 5 | **Discard entries are not stored anywhere** — not in CRM, not in notes, not in logs |
| 6 | Always target `localhost:3001` — never an external URL |
| 7 | **Speed over depth** at triage stage — max 2 web searches per company |
| 8 | For lists of 50+ companies, process in **batches of 20** and report after each batch |
| 9 | After onboarding, always ask the sales rep whether to start outreach now or wait for the monthly cycle |
