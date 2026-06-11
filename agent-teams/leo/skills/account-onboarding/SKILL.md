---
name: account-onboarding
description: >
  Complete workflow for adding a new Account to CRM. Collects company details,
  creates the Account record in Twenty CRM, builds GBrain page, and triggers
  first enrichment. Use when user says "新客戶", "add account", "加一家公司",
  or when capturing-sales-intel identifies a new company to track.
triggers:
  - "new account"
  - "add account"
  - "新客戶"
  - "加一家公司"
  - "onboard account"
version: "3.0"
author: Leo (BD Director Agent)
---

# Account Onboarding

## Purpose

Add a new company to Twenty CRM as an Account (object: `company`), create its GBrain page, and trigger first enrichment. Ensures all required fields are captured and the record is ready for deal or partnership tracking.

**When to use:**
- User met with a company and wants to track it
- User received an inbound lead and needs to create an Account record
- `capturing-sales-intel` identifies a new company to add

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost — never external URL)
**GraphQL endpoint:** `http://localhost:3001/graphql`
**API token:** from environment (`TWENTY_TOKEN`)

**Account object:** `company` (Twenty internal name)

### Required Custom Fields
| Field | Twenty field name | Type |
|---|---|---|
| Status | `accountStatus` | SELECT |
| Type | `accountType` | MULTI_SELECT |
| Country | `country` | SELECT |
| Industry | `industry` | MULTI_SELECT |
| Company Overview | `companyOverview` | TEXT |
| Registered Name (EN) | `registeredNameEn` | TEXT |
| Registered Name (CH) | `registeredNameCh` | TEXT |
| Company Email | `companyEmail` | EMAILS |
| Company Phone | `companyPhone` | PHONES |

---

## Workflow

### Phase 1: Information Gathering

Ask the user for:
```
1. Company Name (English) — required
2. Company Name (Chinese) — optional
3. Website — required
4. Industry — required (Government / Water & Utilities / Tech SaaS / etc.)
5. Country — required (Taiwan / Malaysia / Singapore / etc.)
6. Type — required (Client / Partner / Lead / Vendor)
7. How did we discover them? — for GBrain notes
8. Key Contact(s) — optional (Name, Email, Title)
9. Brief notes on what they do — optional
```

**Before proceeding:** check if company already exists in Twenty:
```graphql
query {
  companies(filter: { name: { like: "%{company_name}%" } }) {
    edges { node { id name } }
  }
}
```
If found → ask user whether to update or create new.

---

### Phase 2: Create Account in Twenty

```graphql
mutation CreateCompany($input: CreateOneCompanyInput!) {
  createCompany(input: $input) {
    id
    name
    domainName { primaryLinkUrl }
  }
}
```

Variables:
```json
{
  "input": {
    "company": {
      "name": "{company_name}",
      "domainName": { "primaryLinkUrl": "{website}", "primaryLinkLabel": "" },
      "accountStatus": "COLD",
      "accountType": ["{type}"],
      "country": "{country}",
      "industry": ["{industry}"],
      "companyOverview": "{user_notes}",
      "registeredNameEn": "{registered_name_en}",
      "registeredNameCh": "{registered_name_ch}"
    }
  }
}
```

Save the returned `id` — needed for subsequent steps.

---

### Phase 3: Create GBrain Page

**Slug format:** `companies/{slugified-name}`
Example: "Acme Corp" → `companies/acme-corp`

```python
mcp_gbrain_put_page(
    slug=f"companies/{company_slug}",
    content="""---
type: company
title: {Company Name}
website: {website}
---

## Overview

{user_notes or placeholder}

## Timeline

## Recent Insights
"""
)
```

---

### Phase 4: Trigger Enrichment

After record is created, run `enriching-leads` skill:
- Input: company name, Twenty record ID, GBrain slug
- Enrichment populates `enrichmentOverview` and GBrain Recent Insights

---

### Phase 5: Add Primary Contact (if provided)

If user gave contact details, create a Person record:

```graphql
mutation CreatePerson($input: CreateOnePersonInput!) {
  createPerson(input: $input) {
    id
    name { firstName lastName }
  }
}
```

Variables:
```json
{
  "input": {
    "person": {
      "name": { "firstName": "{first}", "lastName": "{last}" },
      "emails": { "primaryEmail": "{email}" },
      "jobTitle": "{title}",
      "companyId": "{company_id_from_phase_2}"
    }
  }
}
```

---

## Verification Checklist

- [ ] Company not already in Twenty before creating
- [ ] Account record created — got `id` back from mutation
- [ ] `accountStatus` = COLD (default for new accounts)
- [ ] GBrain page exists at `companies/{slug}`
- [ ] Enrichment triggered (`lastEnrichedDate` set)
- [ ] Primary contact created and linked (if provided)

---

## Pitfalls

1. **Always use localhost** — never the external Cloudflare URL. All agents run on the VM.

2. **Slug collision** — if two companies slugify to the same string, append `-2`. Unlikely but check.

3. **`accountStatus` options** — only `HOT`, `WARM`, `COLD` are valid. Default to `COLD` for new accounts.

4. **`accountType` is MULTI_SELECT** — must be an array even for one value: `["CLIENT"]`.

5. **`industry` is MULTI_SELECT** — same: `["GOVERNMENT"]`.

6. **`domainName` format** — Twenty uses `{ primaryLinkUrl: "...", primaryLinkLabel: "" }` for LINKS type fields.
