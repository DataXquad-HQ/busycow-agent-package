---
name: deal-health-check
description: >
  Daily automated check of all active Deals. Detects deals that are stalled (no
  engagement logged in 7+ days) or overdue on next action. Updates deal status to
  AT_RISK where needed and creates follow-up tasks. Runs autonomously as a cron
  trigger or can be called manually. Use when: cron triggers at 07:00 Taiwan, or
  user asks "deal 健檢", "哪些 deal 卡住了", "pipeline 有沒有 at risk".
triggers:
  - "deal health check"
  - "deal 健檢"
  - "哪些 deal 卡住了"
  - "pipeline 有沒有 at risk"
  - "AT_RISK deals"
version: "1.0"
author: Leo (BD Director Agent)
---

# Deal Health Check

## Purpose
Scan all active Deals in Twenty CRM. For each deal, evaluate whether it is stalled
or at risk based on recency of engagement and next-action status. Update deal status
and create tasks where needed. This skill is the engine — the daily-briefing skill
reads its output.

## CRM Backend
- Endpoint: `http://localhost:3001/api` (data) and `http://localhost:3001/metadata` (schema)
- Auth: Bearer token from `/tmp/twenty_token.txt`
- Always use localhost — never the external Cloudflare URL

## Step 1 — Fetch All Active Deals

Query all opportunities where stage is NOT Closed Won or Closed Lost:

```graphql
query ActiveDeals {
  opportunities(
    filter: {
      and: [
        { stage: { notIn: ["CLOSED_WON", "CLOSED_LOST"] } }
        { dealStatus: { notEq: "CANCELLED" } }
      ]
    }
    first: 100
  ) {
    edges {
      node {
        id
        name
        stage
        dealStatus
        nextActionSummary
        lastUpdateDate
        updatedAt
        amount { amountMicros currencyCode }
        pointOfContact { edges { node { id name { firstName lastName } } } }
      }
    }
  }
}
```

## Step 2 — Evaluate Each Deal

For each deal, calculate days since last update:
- Use `lastUpdateDate` if set; fall back to `updatedAt`
- `lastUpdateDate` is a DATE string (YYYY-MM-DD); `updatedAt` is ISO datetime

Apply these rules:

| Condition | Action |
|-----------|--------|
| Days since update > 7 AND `nextActionSummary` is empty | Mark `AT_RISK`, create task |
| Days since update > 14 (any stage) | Mark `AT_RISK`, create task |
| Stage = CUSTOMER and days > 21 | Mark `AT_RISK` + flag urgency HIGH |
| Stage = PROPOSAL and days > 14 | Mark `AT_RISK` |
| `nextActionSummary` is set and days < 7 | Healthy — no action |

## Step 3 — Update Deal Status

For deals flagged AT_RISK, update their `dealStatus` field:

```graphql
mutation UpdateDealStatus($id: ID!, $status: String!) {
  updateOpportunity(
    id: $id
    data: { dealStatus: $status }
  ) {
    id
    dealStatus
  }
}
```

Status values: `HEALTHY` / `AT_RISK` / `NEEDS_FOLLOWUP` / `CANCELLED`

## Step 4 — Create Follow-up Tasks (dedup)

Before creating a task, check if an open task already exists for this deal within the last 7 days (to avoid duplicates):

```graphql
query ExistingTasks($dealId: ID!) {
  tasks(
    filter: {
      and: [
        { opportunity: { id: { eq: $dealId } } }
        { status: { notEq: "DONE" } }
        { dueAt: { gte: "7_DAYS_AGO_ISO" } }
      ]
    }
  ) {
    edges { node { id title } }
  }
}
```

If no existing open task, create one:

```graphql
mutation CreateTask($dealId: ID!, $title: String!, $due: DateTime!) {
  createTask(
    data: {
      title: $title
      status: "TODO"
      dueAt: $due
      taskPriority: "HIGH"
      opportunity: { id: $dealId }
    }
  ) {
    id
    title
  }
}
```

Task title format: `"[Deal Health] {deal name} — 超過 {N} 天無更新，請跟進"`
Due date: today + 1 day

## Step 5 — Output Summary

Return a structured summary (used by daily-briefing):

```
## Deal Health Check — {DATE}

Total active deals: N
Healthy: N
At risk: N

### 🔴 AT_RISK Deals
| Deal | Stage | Days since update | Next Action | Task created |
|------|-------|-------------------|-------------|-------------|
| ... |

### ✅ Healthy Deals
(list deal names only — no table needed)
```

## Mode A — Manual (single deal)
User provides a deal name or ID → check only that deal, return detailed status.

## Mode B — Full scan (cron)
No input → scan all active deals, apply rules, update statuses, create tasks.
Silent if all deals are healthy (no output).
Only output/deliver if AT_RISK deals were found.

## Pitfalls
- `amount.amountMicros` ÷ 1,000,000 = USD value
- `lastUpdateDate` may be null — always fall back to `updatedAt`
- Don't create duplicate tasks — always check first with ExistingTasks query
- **Stage field confirmed values:** `NEW`, `SCREENING`, `MEETING`, `PROPOSAL`, `CUSTOMER` — NOT `NEW_LEAD`, `MEETING_SCHEDULED`, etc. The UPPER_SNAKE variants return a schema error.
- **dealStatus SELECT options (confirmed):** `HEALTHY`, `AT_RISK`, `NEEDS_FOLLOWUP`, `CANCELLED`
- Always localhost — never external URL
