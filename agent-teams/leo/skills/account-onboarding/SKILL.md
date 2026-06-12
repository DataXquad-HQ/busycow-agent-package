---
name: account-onboarding
description: >
  Use when the sales rep tells Leo about a new person they met — at an event,
  through an introduction, or inbound contact. Leo extracts what's known, asks
  one question to fill the most critical gap, then creates Company + Person
  records in Twenty CRM and triggers first enrichment.
  Use when user says "我認識了一個人", "met someone at the event",
  "新聯絡人", "add to CRM", or describes a new person/company they encountered.
triggers:
  - "met someone"
  - "new contact"
  - "我認識了一個人"
  - "新聯絡人"
  - "剛遇到"
  - "event contact"
  - "add to CRM"
  - "加進 CRM"
  - "onboard"
version: "5.0"
author: Leo (BD Director Agent)
---

# Account Onboarding

## Purpose

When the sales rep tells Leo about a person they met, Leo's job is to:
1. Extract everything useful from what the sales rep says
2. Ask **one targeted question** if a critical gap exists — never a questionnaire
3. Check for existing records before creating anything
4. Create Company + Person records in Twenty CRM (only if not already there)
5. Run first enrichment on the company
6. Confirm the relationship type (Opportunity / Partnership / Connection)

**When to use:**
- Sales rep met someone at an event, through an introduction, or inbound contact
- Sales rep describes a new person/company in passing — even informally
- `capturing-sales-intel` identifies a new company to add

**Not triggered by:** website form submissions (those are not qualified until personally validated).

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost — never external URL)
**GraphQL endpoint:** `http://localhost:3001/graphql`

**Token:** Stored in `~/.hermes/profiles/[agent]/.env` as `TWENTY_TOKEN`. Read with:
```bash
TOK=$(grep TWENTY_TOKEN ~/.hermes/profiles/[agent]/.env | cut -d= -f2)
```
Do NOT use `python3 -c` for API calls — use `curl` (no approval prompts).

**CRM terminology:**
| Term | Twenty object |
|---|---|
| Company | `company` |
| Person | `person` |
| Opportunity | `opportunity` |

---

## Phase 1: Extract from What the Sales Rep Said

Parse the sales rep's message for any of:

| Field | What to look for |
|---|---|
| Person's name | First name + last name |
| Person's title / role | What they do |
| Company name | English or Chinese |
| Company website / domain | If mentioned |
| Industry / what the company does | Any description |
| Country / location | Where they're based |
| How they met | Event, intro, inbound, referral |
| Relationship type hint | Potential customer, partner, or just a connection? |
| Next action hint | "follow up", "send proposal", "just staying in touch"? |

Map to these **critical fields** (must have before creating records):
- **Person name** — first name minimum
- **Company name** — required to create Company record
- **Something about what they do** — for enrichment and fit assessment

If all three are present: proceed to Phase 2.

If a critical field is missing: ask **one question** targeting the biggest gap:
- Missing company: "他是哪家公司的？"
- Missing company context: "這家公司主要做什麼？"
- Missing name: "這個人叫什麼名字？"

Do not ask multiple questions at once. Never run a checklist.

---

## Phase 2: Check for Existing Records

**Always check before creating.** Use `curl` — no approval prompts.

```bash
TOK=$(grep TWENTY_TOKEN ~/.hermes/profiles/[agent]/.env | cut -d= -f2)

curl -s -X POST http://localhost:3001/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOK" \
  -d '{"query":"{ companies(filter:{name:{like:\"%[COMPANY_NAME]%\"}}) { edges { node { id name people { edges { node { id name { firstName lastName } jobTitle status } } } } } } }"}'
```

**Step 1 — Company found?**
- Yes → notify: "這家公司已經在 CRM 裡了（{name}）。" → save `company_id`, skip Phase 3
- No → proceed to Phase 3

**Step 2 — Person already linked to this company?** (only check if company was found)
- Match by firstName + lastName (or email if known)
- Yes → notify: "{name} 這個人已經在 CRM 裡了，幫你更新資料就好。" → skip Phase 4, update existing record with any new info (jobTitle, source, status)
- No → proceed to Phase 4

---

## Phase 3: Create Company Record

```bash
TOK=$(grep TWENTY_TOKEN ~/.hermes/profiles/[agent]/.env | cut -d= -f2)

cat > /tmp/create_company.json << PAYLOAD
{"query": "mutation { createCompany(data: { name: \"[COMPANY_NAME]\", domainName: { primaryLinkUrl: \"[WEBSITE_OR_EMPTY]\", primaryLinkLabel: \"\" }, country: [COUNTRY_ENUM], companyOverview: \"[DESCRIPTION]\" }) { id name } }"}
PAYLOAD

curl -s -X POST http://localhost:3001/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOK" \
  -d @/tmp/create_company.json
```

Save the returned `id` as `company_id`.

---

## Phase 4: Create Person Record

```bash
cat > /tmp/create_person.json << PAYLOAD
{"query": "mutation { createPerson(data: { name: { firstName: \"[FIRST]\", lastName: \"[LAST]\" }, jobTitle: \"[TITLE]\", companyId: \"[COMPANY_ID]\", source: [SOURCE_ENUM], status: LEAD }) { id name { firstName lastName } } }"}
PAYLOAD

curl -s -X POST http://localhost:3001/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOK" \
  -d @/tmp/create_person.json
```

**status**: always `LEAD` for human-introduced contacts.

**source** enum — map from how they met:
| How they met | Value |
|---|---|
| Event / conference / exhibition | `EVENT` |
| Introduction / referral | `REFERRAL` |
| They reached out to us | `INBOUND_WEB` |
| Partner introduced | `PARTNER` |
| [Content agent]'s outbound | `OUTBOUND_MAYA` |

Save the returned `id` as `person_id`.

---

## Phase 5: First Enrichment

After records are created (or confirmed existing), immediately run `enriching-leads` skill:
- Input: company name, company domain (if known), Twenty company `id`
- Depth: **deep** (human-introduced contact)
- Writes findings to Twenty CRM + GBrain — no confirmation needed at this stage

If no domain known, use company name as search term.

---

## Phase 6: Create or Update GBrain Page

```
mcp_gbrain_put_page(
  slug="companies/[slugified-name]",
  content="""---
type: company
title: [Company Name]
website: [website]
---

## Overview

[description from sales rep + enrichment]

## How We Met

[how_met] — [date]

## Key People

- [person_name], [title]

## Timeline

## Recent Insights
"""
)
```

Slug format: `companies/{slugified-name}` — e.g. "Acme Corp" → `companies/acme-corp`

If a GBrain page already exists, update the Key People section and add a timeline entry instead of overwriting.

---

## Phase 7: Confirm Relationship Type

Present a brief summary and ask how to classify:

```
✅ 已加入 CRM：

公司：{Company Name}
聯絡人：{Person Name}，{Title}
來源：{how_met}

這個人怎麼走？
- **Opportunity** — 有銷售機會，開 Opportunity 追蹤
- **Partnership** — 潛在合作夥伴，開 Partnership 追蹤
- **Connection** — 先觀望，放進 monthly nurture
```

Based on the sales rep's answer:
- **Opportunity** → create Opportunity record linked to this person and company
- **Partnership** → create Partnership record
- **Connection** → no additional record; monthly `lead-nurturing-monthly` cron picks them up automatically

---

## Verification Checklist

- [ ] Company checked for duplicates before creating
- [ ] Person checked for duplicates before creating
- [ ] Company record exists in CRM with `id`
- [ ] Person record exists and linked to Company, status = `LEAD`, source set
- [ ] Enrichment triggered
- [ ] GBrain page created or updated
- [ ] Relationship type confirmed by sales rep
- [ ] Opportunity or Partnership record created if applicable

---

## Pitfalls

1. **Always use localhost** — never the external URL.

2. **Never ask more than one question** — ask for the most critical missing field only.

3. **Always check for duplicates first** — both company AND person. Do not create records without checking.

4. **`industry` is a single ENUM** — not an array. See `enriching-leads` for valid values.

5. **`domainName` format** — `{ primaryLinkUrl: "https://...", primaryLinkLabel: "" }`. If unknown: `{ primaryLinkUrl: "", primaryLinkLabel: "" }`.

6. **Human-introduced contacts are always `LEAD`** — `PROSPECT` is only for cold outreach targets that haven't responded.

7. **Use `curl` not `python3 -c`** — curl against localhost needs no approval. `python3 -c` and `-e` flags trigger approval prompts.

8. **Person `source` must match enum** — valid: `REFERRAL`, `EVENT`, `PARTNER`, `INBOUND_WEB`, `OUTBOUND_MAYA`.

9. **If token returns FORBIDDEN** — stop immediately, ask [Sales Rep] to regenerate: Twenty UI → Settings → API & Webhooks → Generate a token. Store new token in `~/.hermes/profiles/[agent]/.env`.
