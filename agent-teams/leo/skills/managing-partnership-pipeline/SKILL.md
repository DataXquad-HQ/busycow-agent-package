---
name: managing-partnership-pipeline
description: >
  Use when there is any update on a Partnership — new partner prospect, stage change,
  partner meeting, follow-up, or contract trigger. Handles both creating new Partnerships
  and updating existing ones. Use when user says "跟夥伴聊了", "partnership 有進展",
  "partner update", "有個新合作夥伴", or dumps a block of partner updates.
  For NEW contacts/companies → also run capturing-sales-intel.
triggers:
  - "partnership update"
  - "partner stage"
  - "跟夥伴聊了"
  - "partner progress"
  - "partnership 有進展"
  - "update partner"
  - "有個新合作夥伴"
  - "新的 partner"
version: "3.0"
author: Leo (BD Director Agent)
---

# Managing Partnership Pipeline

## CRM Backend
- Data endpoint: `http://localhost:3001/api`
- Metadata endpoint: `http://localhost:3001/metadata`
- Auth: Bearer token from `/tmp/twenty_token.txt`
- Always use localhost — never the external Cloudflare URL
- Partnership object: `partnership` (custom)

---

## Stage Flow
```
PROSPECT → QUALIFYING → AGREEMENT → ACTIVE
                                   → ON_HOLD / INACTIVE
```

| Stage | Meaning |
|-------|---------|
| PROSPECT | Initial identification, first contact |
| QUALIFYING | Both sides evaluating fit |
| AGREEMENT | Negotiating terms, contract being drafted |
| ACTIVE | Signed, collaboration in progress |
| ON_HOLD | Temporarily paused |
| INACTIVE | Relationship ended |

---

## Phase 1 — Triage the Update

1. Read the full message carefully
2. Identify every distinct partner mentioned
3. For each entity, classify:
   - Existing partnership (update) or new prospect (create)?
   - Did stage change?
   - Is there a concrete signal or commitment?
   - Is there a next action implied?
   - Did this partner bring a new Opportunity? → flag for `managing-sales-pipeline`

Present your parse:
> "我看到 2 個夥伴更新：[A] — [B]。我先處理這兩個，有沒有遺漏？"

---

## Phase 2 — Probe Gaps

Extract what's in the message, ask only for what's missing.

**Must have before logging an engagement:**
- Who was spoken to (contact name + company)
- How (電話 / WhatsApp/LINE / 線上會議 / 實體拜訪 / Demo / 訊息)
- What happened (1-line summary)
- Partner response / reaction

**Must have before updating stage:**
- What concrete signal triggered the stage change?

**Must have before creating a new Partnership:**
- Partner company name (must exist in Accounts — if not, run `capturing-sales-intel` first)
- Type: Reseller / Tech Partner / Referral / OEM / Other
- Country / region
- Initial stage (default: PROSPECT)

---

## Phase 3 — Log Engagement

For every interaction, create an Engagement record via `engagement-logging` skill.
Pass: type, company, contact, outcome, next action, partnership link.

---

## Phase 4 — Update / Create Partnership

### Update existing partnership:
```graphql
mutation UpdatePartnership($id: ID!, $stage: String, $overview: String, $nextAction: String, $lastUpdate: Date) {
  updatePartnership(
    id: $id
    data: {
      status: $stage
      partnershipOverview: $overview
      nextActionSummary: $nextAction
      lastUpdateDate: $lastUpdate
    }
  ) {
    id
    name
    status
  }
}
```

### Create new partnership:

1. Check if company exists in Twenty:
```graphql
query FindCompany($name: String!) {
  companies(filter: { name: { like: "%$name%" } }) {
    edges { node { id name } }
  }
}
```
If not found → run `capturing-sales-intel` first, then return here.

2. Create partnership record:
```graphql
mutation CreatePartnership(
  $name: String!
  $partnerType: String!
  $status: String!
  $overview: String
  $companyId: ID!
) {
  createPartnership(
    data: {
      name: $name
      partnerType: $partnerType
      status: $status
      partnershipOverview: $overview
      startDate: "TODAY_ISO"
    }
  ) {
    id
    name
    status
  }
}
```

Then link to company via relation update.

### GBrain sync:
After creating/updating, call `mcp_gbrain_add_timeline_entry` on the partner's page:
- slug: `companies/{partner-name-slug}`
- summary: stage change or key development
- detail: outcome + next action

---

## Phase 5 — Push Next Steps

After logging, ALWAYS push for concrete next actions:

1. **下一步是什麼？** 誰負責，什麼時候之前？→ create task:
```graphql
mutation CreatePartnershipTask($partnershipId: ID!, $title: String!, $due: DateTime!) {
  createTask(
    data: {
      title: $title
      status: "TODO"
      dueAt: $due
      taskPriority: "HIGH"
      partnership: { id: $partnershipId }
    }
  ) {
    id title
  }
}
```

2. **Stage 對嗎？** 要推進還是退回？
3. **有沒有要起草合約？** Stage → AGREEMENT 時觸發
4. **這個夥伴有帶來具體商機嗎？** → if yes, run `managing-sales-pipeline`

---

## Pitfalls
- Always check for existing company before creating partnership
- Never create duplicate — search by name first
- Stage field values: `PROSPECT`, `QUALIFYING`, `AGREEMENT`, `ACTIVE`, `ON_HOLD`, `INACTIVE`
- `partnerType` SELECT options: `RESELLER`, `TECH_PARTNER`, `REFERRAL`, `OEM`, `OTHER`
- `lastUpdateDate` is a DATE field (YYYY-MM-DD), not datetime
- Always localhost — never external URL
- GBrain sync is mandatory on every partnership create or stage change
