---
name: meeting-prep
description: >
  Use when preparing for a scheduled meeting with a prospect, client, or partner.
  Can be triggered manually ("幫我準備明天的會議") or automatically by daily cron.
  Scans Planned Engagements in Twenty CRM, pulls Opportunity + Company context, and
  generates a focused meeting brief.
triggers:
  - "幫我準備明天的會議"
  - "prep for meeting"
  - "meeting prep"
  - "明天的 meeting"
version: "3.1"
author: Leo (BD Director Agent)
---

# Meeting Prep

## Purpose

Generate a focused pre-meeting brief by pulling context from Twenty CRM — the company background, opportunity stage, recent engagement history, and open tasks.

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost)
**GraphQL endpoint:** `http://localhost:3001/graphql`

---

## Two Modes

### Mode A: Specific Meeting
User names an opportunity or company. Leo fetches that Engagement + Opportunity + Company and generates the brief.

### Mode B: Tomorrow Scan (cron or "幫我準備明天的")
Leo scans for all Planned Engagements scheduled for tomorrow. One brief per meeting. **Silent if no meetings found.**

---

## Workflow

### Step 1: Find Planned Engagement(s)

**Mode A — specific:**
```graphql
query {
  engagements(filter: {
    and: [
      { engagementStatus: { eq: "PLANNED" } }
      { opportunity: { name: { like: "%{opportunity_name}%" } } }
    ]
  }) {
    edges {
      node {
        id name engagementDate engagementType
        engagementNote { json }
        opportunity { id name stage amount { amountMicros } }
        company { id name companyOverview enrichmentOverview }
        clientAttendees { edges { node { id name { firstName lastName } jobTitle } } }
      }
    }
  }
}
```

**Mode B — tomorrow scan:**
```graphql
query {
  engagements(filter: {
    and: [
      { engagementStatus: { eq: "PLANNED" } }
      { engagementDate: { gte: "{tomorrow_start_iso}" } }
      { engagementDate: { lte: "{tomorrow_end_iso}" } }
    ]
  }) {
    edges { node { id name engagementDate engagementType opportunity { id name stage } company { id name } } }
  }
}
```

If no results in Mode B → **silent, return nothing**.

---

### Step 2: Pull Full Context

For each engagement found, fetch:

```graphql
query GetOpportunityContext($oppId: ID!) {
  opportunity(id: $oppId) {
    name stage
    currentStatusSummary nextActionSummary
    priority healthCheck
    amount { amountMicros currencyCode }
    closeDate
    company {
      name companyOverview enrichmentOverview country industry
    }
    engagements(
      filter: { engagementStatus: { eq: "COMPLETED" } }
      orderBy: { engagementDate: DescNullsLast }
      first: 3
    ) {
      edges {
        node {
          engagementDate engagementType outcome nextAction
          engagementNote { json }
        }
      }
    }
  }
}
```

---

### Step 3: Generate Brief

Output format (繁體中文):

```
📅 明日會議準備 — {Opportunity Name}

【會議資訊】
時間：{Date + Time}
類型：{Engagement Type}
對象：{Company Name}
出席：{Attendees if known}
Opportunity 階段：{Stage}

【背景】
{2–3 句：這個 opportunity 目前在哪裡、上次互動發生了什麼、客戶核心疑慮是什麼}

【這次目標】
{一句話：這次會議結束後，成功長什麼樣子}

【三個必打點】
① {最重要的 talking point + 為什麼}
② {第二點}
③ {第三點}

【預期異議 & 應對】
❓ {預期異議 1}
→ {應對話術}

❓ {預期異議 2（如有）}
→ {應對話術}

【會後立刻要做的事】
- {Next action 1}
- {Next action 2}

【成功標準】
- [ ] {Checkbox 1}
- [ ] {Checkbox 2}
```

---

## Output Delivery

- **Manual trigger:** Reply in conversation
- **Cron trigger:** Deliver to origin Feishu chat
- **Multiple meetings tomorrow:** One brief per meeting, separated by `---`
- **No meetings found (Mode B):** Silent — send nothing

---

## Pitfalls

1. **Always use localhost** — never external URL.

2. **Mode B silent if no meetings** — do not send "no meetings today". That's noise.

3. **Brief is not archived** — lifecycle ends after the meeting. Outcome goes into `engagementNote` (Completed), not back into the brief.

4. **One goal per meeting** — don't list three objectives. Pick the single most important ask.

5. **Check attendees carefully** — if a decision-maker is attending (not just the daily person), adjust talking points accordingly.

6. **Don't repeat last meeting's points** — scan the 3 most recent Completed engagements first to avoid suggesting things already said.
