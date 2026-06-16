---
name: capturing-sales-intel
description: >
  Use when a piece of intel about a company or person arrives in conversation —
  a new lead, a referral, a business card, a name drop. Creates Account and Contact
  records in Twenty CRM and GBrain in one flow, then hands off to enriching-leads.
  Use when user says "新的 lead", "有人介紹", "認識了一個人", "這間公司", or dumps
  contact/company info in the chat.
triggers:
  - "新的 lead"
  - "有人介紹"
  - "認識了一個人"
  - "這間公司"
  - "new lead"
  - "new contact"
  - "I met someone"
  - "I heard about"
version: "1.0"
author: Leo (BD Director Agent)
---

# Capturing Sales Intel

## Purpose

When a lead, referral, or contact surfaces in conversation, immediately capture it into Twenty CRM and GBrain before anything is forgotten. This is the **entry gate** for all new accounts and contacts into the pipeline.

After capturing, automatically trigger `enriching-leads` for background intel.

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost)
**GraphQL endpoint:** `http://localhost:3001/graphql`

---

## When to Use

- User mentions a company or person they just met
- Someone sends a business card, email intro, or LinkedIn profile
- User says "there's a new lead from [event/referral/inbound]"
- User dumps a block of contact info in chat

---

## Workflow

### Step 1: Extract the Intel

From whatever the user provides, extract:

**Company info:**
- Name (English) — required
- Name (Chinese) — optional
- Website — optional
- Industry — optional
- Country — optional

**Contact info:**
- Full name — required
- Email — optional
- Phone / WhatsApp — optional
- Job title — optional
- Source (how we met: Referral / Event / Inbound Web / Partner / Network)

**Context:**
- How did we discover them?
- Any notes from the conversation?

If any required field is missing, ask for it before proceeding.

---

### Step 2: Check for Duplicates

Check if account already exists:
```graphql
query {
  companies(filter: { name: { like: "%{company_name}%" } }) {
    edges { node { id name } }
  }
}
```

Check if contact already exists:
```graphql
query {
  people(filter: { emails: { primaryEmail: { eq: "{email}" } } }) {
    edges { node { id name { firstName lastName } } }
  }
}
```

If duplicates found → ask user: "This account/contact already exists. Update the existing record or create new?"

---

### Step 3: Create Account (if new)

```graphql
mutation {
  createCompany(data: {
    name: "{company_name}"
    domainName: { primaryLinkUrl: "{website}", primaryLinkLabel: "" }
    accountStatus: "WARM"
    accountType: ["PROSPECT"]
    country: "{country}"
    industry: ["{industry}"]
    companyOverview: "{user_notes}"
    registeredNameCh: "{chinese_name}"
  }) {
    id name
  }
}
```

> **Note:** mutation syntax is `createCompany(data: {...})` — NOT `createCompany(input: { company: {...} })`. The `input`/`company` wrapper returns an error.

---

### Step 4: Create Contact (if new)

```graphql
mutation {
  createPerson(data: {
    name: { firstName: "{first}", lastName: "{last}" }
    emails: { primaryEmail: "{email}" }
    phones: { primaryPhoneNumber: "{phone}", primaryPhoneCountryCode: "{cc}" }
    jobTitle: "{title}"
    source: "{source_value}"
    companyId: "{company_id}"
  }) {
    id name { firstName lastName }
  }
}
```

> **Note:** mutation syntax is `createPerson(data: {...})` — NOT `createPerson(input: { person: {...} })`.

**`source` valid values (confirmed):** `REFERRAL` / `EVENT` / `PARTNER` / `INBOUND_WEB` / `OUTBOUND_MAYA`
⚠️ `NETWORK` is NOT a valid value — use `REFERRAL` for network contacts.

---

### Step 5: Create GBrain Pages

**Company page:**
```python
mcp_gbrain_put_page(
    slug=f"companies/{company_slug}",
    content="""---
type: company
title: {Company Name}
---

## Overview

{user_notes or placeholder}

## Timeline

## Recent Insights
"""
)
```

**Person page (if new contact):**
```python
mcp_gbrain_put_page(
    slug=f"people/{person_slug}",
    content="""---
type: person
title: {Full Name}
company: {Company Name}
---

## Background

{role, context of how we met}

## Timeline
"""
)
```

---

### Step 6: Trigger Enrichment

Immediately invoke `enriching-leads` with the new company record ID.

---

### Step 7: Recommend First Action

Based on the source and context, suggest the first action:

| Source | Suggested first action |
|--------|----------------------|
| Referral | Send intro email within 24h |
| Event | Follow up with context from conversation |
| Inbound | Qualify immediately — they came to us |
| Partner | Understand the referral context first |
| Network | Low urgency — schedule for next week |

Output:
```
✅ Captured:
  Account: {Company Name} (ID: {id})
  Contact: {Full Name} ({title}) (ID: {id})

GBrain pages created:
  companies/{slug}
  people/{slug}

Enrichment triggered for {Company Name}.

Recommended next action: {suggestion}
```

---

## Pitfalls

1. **Always use localhost** — never external URL.

2. **Don't create duplicate records** — always check before creating. A duplicate Account corrupts the pipeline.

3. **`source` on Contact, not Account** — source tracks how we met the person, not the company.

4. **`accountStatus` = WARM by default for new leads** — Cold is for dormant/unknown. A lead you're actively capturing is at least Warm.

5. **`accountType` valid values: `CLIENT` / `PARTNER` / `PROSPECT` / `VENDOR` / `DIRECT`** — `LEAD` is NOT a valid value. Use `PROSPECT` for net-new contacts. Change to `CLIENT` only when a opportunity closes.

6. **Mutation syntax: `createCompany(data: {...})`** — NOT `createCompany(input: { company: {...} })`. The wrapper format returns a schema error.

7. **`source` valid values: `REFERRAL` / `EVENT` / `PARTNER` / `INBOUND_WEB` / `OUTBOUND_MAYA`** — `NETWORK` is NOT valid. Map network contacts to `REFERRAL`.

8. **GBrain slug format** — lowercase, spaces → hyphens, strip special characters. `Acme Corp.` → `acme-corp`.

9. **New data completeness check** — Before creating a Opportunity, assess: does this contact have confirmed budget, authority, and a specific ask? If not → Company + Contact + Note only (pre-qualified holding state). Upgrade to Opportunity when they confirm intent.
