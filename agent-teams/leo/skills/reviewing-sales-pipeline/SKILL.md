---
name: reviewing-sales-pipeline
description: >
  Pull live data from Twenty CRM and deliver a structured sales status briefing —
  pipeline health, deal stages, outstanding tasks, recent engagements, and revenue
  snapshot. Use when user asks about sales status, pipeline overview, "我們現在業務怎樣",
  "有什麼 deal 在跑", "收款狀況", or wants to understand where the business stands.
triggers:
  - "業務狀態"
  - "pipeline"
  - "sales status"
  - "有什麼 deal"
  - "收款狀況"
  - "我們的 pipeline"
  - "銷售概況"
  - "現在業務怎樣"
  - "有沒有 deal 在跑"
  - "revenue 狀況"
  - "跟進狀態"
version: "2.0"
author: Leo (BD Director Agent)
---

# Reviewing Sales Pipeline

## Purpose
Give a comprehensive, data-driven sales briefing. Interpret the data — identify
what's hot, what's stale, what needs attention, and what's at risk.

## CRM Backend
- Data endpoint: `http://localhost:3001/api`
- Auth: Bearer token from `/tmp/twenty_token.txt`
- Always use localhost — never the external Cloudflare URL

---

## Data Pull Sequence (run in parallel)

```graphql
# 1. Active Deals
query ActiveDeals {
  opportunities(
    filter: { stage: { notIn: ["CLOSED_WON", "CLOSED_LOST"] } }
    first: 100
    orderBy: { updatedAt: DescNullsLast }
  ) {
    edges {
      node {
        id name stage dealStatus
        nextActionSummary lastUpdateDate updatedAt
        amount { amountMicros currencyCode }
        pointOfContact { edges { node { name { firstName lastName } } } }
        company { edges { node { name } } }
      }
    }
  }
}

# 2. Recent Engagements (last 14 days)
query RecentEngagements {
  engagements(
    filter: { engagementDate: { gte: "FOURTEEN_DAYS_AGO" } }
    orderBy: { engagementDate: DescNullsLast }
    first: 50
  ) {
    edges {
      node {
        id engagementType engagementStatus engagementDate
        outcome nextAction
        opportunity { edges { node { id name } } }
        clientAttendees { edges { node { name { firstName lastName } } } }
      }
    }
  }
}

# 3. Open Tasks (due or overdue)
query OpenTasks {
  tasks(
    filter: {
      and: [
        { status: { notEq: "DONE" } }
        { dueAt: { lte: "TODAY_END_ISO" } }
      ]
    }
    orderBy: { dueAt: AscNullsLast }
    first: 50
  ) {
    edges {
      node {
        id title status dueAt taskPriority
        opportunity { edges { node { id name } } }
      }
    }
  }
}
```

---

## Analysis Framework — 5 Sections

### 🔥 Section 1 — Hot Pipeline
Deals in active stages (stage NOT in CLOSED_WON / CLOSED_LOST):
- List each: Account | Deal name | Stage | dealStatus | Est. Value | Next Action
- Flag `dealStatus = AT_RISK` → ⚠️
- Flag `dealStatus = NEEDS_FOLLOWUP` → 🔴
- Flag deals with no `nextActionSummary` → 📋 incomplete
- Flag deals where `lastUpdateDate` > 14 days ago → ⚠️ stale
- Summarise: total active pipeline value

### 📋 Section 2 — Deal Stage Summary
Group all opportunities by stage:
```
NEW_LEAD:          N deals
MEETING_SCHEDULED: N deals  ($X)
PROPOSAL_SENT:     N deals  ($X)
NEGOTIATION:       N deals  ($X)
CLOSED_WON:        N deals  ($X)  ← this period
CLOSED_LOST:       N deals
```

### 💰 Section 3 — Open Tasks & Actions
From open tasks (due or overdue):
- Group by linked deal
- Show: Task title | Due date | Priority | Status
- 🔴 Overdue tasks (dueAt < today)
- 🟡 Due within 3 days
- Deals with NO open task and no recent engagement → missing follow-through

### 📅 Section 4 — Recent Engagements (14 days)
From engagements table:
- List: Date | Account | Type | Outcome | Next Action
- Deals with engagement this period vs deals with no touch
- Note: "X deals touched | Y deals silent"

### 📊 Section 5 — Revenue Snapshot
From CLOSED_WON deals:
- This month closed value (sum of `amountMicros` ÷ 1M where `updatedAt` is this month)
- Total pipeline value (all active deals)
- Keep brief — headline numbers only

---

## Output Format

Deliver in **繁體中文** unless user asks for English.
Use tables and bullets, not paragraphs.
Always end with **「需要關注的3件事」**.

```
## 📊 DataXquad 業務概況  [DATE]

### 🔥 熱門 Pipeline
[table: Account | Deal | Stage | 狀態 | 估值 | 下一步]
⚠️ At Risk: [list]
🔴 Needs Followup: [list]

### 📋 Pipeline 漏斗
[stage breakdown]

### 💰 任務 & 待辦
[table: Deal | Task | 到期日 | Priority]
🔴 逾期: [list]

### 📅 近期 Engagements (14天)
[list]
有跟進: X 個 | 無動靜: Y 個

### 📊 Revenue
本月成交: $X | 總 Pipeline: $X

---
### 🎯 需要關注的3件事
1. 
2. 
3. 
```

---

## Interpretation Rules

| Situation | Flag | Action |
|-----------|------|--------|
| dealStatus = AT_RISK | ⚠️ | 列入 Section 1 重點 |
| NEGOTIATION stage > 21 days no update | 🔴 | 立即跟進 |
| PROPOSAL_SENT stage > 14 days no engagement | ⚠️ | Follow-up call |
| No open task AND no engagement in 14 days | 📋 | 補建 task |
| Multiple deals same account | ℹ️ | Cross-sell opportunity |

---

## Scope Customisation

| User asks | What to do |
|-----------|------------|
| "GeoKernel 的 pipeline" | Filter opportunities by product/businessLine context |
| "Hunter 的 deals" | Filter by pointOfContact owner |
| "HKRFID 的狀況" | Filter by company name |
| "收款/任務狀況" | Focus on Section 3 only |
| "這週的跟進" | Focus on Section 4, last 7 days |
| "整體" / no scope | Full 5-section briefing |

---

## Pitfalls
- `amount.amountMicros` ÷ 1,000,000 = USD value
- `lastUpdateDate` may be null — fall back to `updatedAt`
- Stage uses UPPER_SNAKE_CASE: `NEW_LEAD`, `MEETING_SCHEDULED`, `PROPOSAL_SENT`, `NEGOTIATION`, `CLOSED_WON`, `CLOSED_LOST`
- dealStatus SELECT: `HEALTHY`, `AT_RISK`, `NEEDS_FOLLOWUP`, `CANCELLED`
- Engagement date filter: replace "FOURTEEN_DAYS_AGO" with actual ISO datetime in code
- Always localhost — never external URL
- If `pointOfContact` is empty, show "—" not error
