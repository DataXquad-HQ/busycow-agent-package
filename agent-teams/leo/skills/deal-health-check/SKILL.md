---
name: deal-health-check
description: >
  Daily automated check of all active Opportunities. Detects opportunities that are stalled (no
  engagement logged in 7+ days) or overdue on next action. Updates opportunity status to
  AT_RISK where needed and creates follow-up tasks. Runs autonomously as a cron
  trigger or can be called manually. Use when: cron triggers at 07:00 Taiwan, or
  user asks "opportunity 健檢", "哪些 opportunity 卡住了", "pipeline 有沒有 at risk".
triggers:
  - "deal health check"
  - "deal 健檢"
  - "哪些 deal 卡住了"
  - "pipeline 有沒有 at risk"
  - "AT_RISK deals"
version: "1.1"
author: Leo (BD Director Agent)
---

# Opportunity Health Check

## Purpose
Scan all active Opportunities in Twenty CRM. For each opportunity, evaluate whether it is stalled
or at risk based on recency of engagement and next-action status. Update opportunity status
and create tasks where needed. This skill is the engine — the daily-briefing skill
reads its output.

## CRM Backend
- Endpoint: `http://localhost:3001/api` (data) and `http://localhost:3001/metadata` (schema)
- Auth: Bearer token from `/tmp/twenty_token.txt`
- Always use localhost — never the external Cloudflare URL

## Step 1 — Fetch All Active Opportunities

Query all opportunities where stage is NOT Closed Won or Closed Lost:

```graphql
query ActiveOpportunities {
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

## Step 2 — Evaluate Each Opportunity

For each opportunity, calculate days since last update:
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

## Step 3 — Update Opportunity Status

For opportunities flagged AT_RISK, update their `dealStatus` field:

```graphql
mutation UpdateOpportunityStatus($id: ID!, $status: String!) {
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

Before creating a task, check if an open task already exists for this opportunity within the last 7 days (to avoid duplicates):

```graphql
query ExistingTasks($opportunityId: ID!) {
  tasks(
    filter: {
      and: [
        { opportunity: { id: { eq: $opportunityId } } }
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
mutation CreateTask($opportunityId: ID!, $title: String!, $due: DateTime!) {
  createTask(
    data: {
      title: $title
      status: "TODO"
      dueAt: $due
      taskPriority: "HIGH"
      opportunity: { id: $opportunityId }
    }
  ) {
    id
    title
  }
}
```

Task title format: `"[Opportunity Health] {opportunity name} — 超過 {N} 天無更新，請跟進"`
Due date: today + 1 day

## Step 5 — Output Summary

Return a structured summary (used by daily-briefing):

```
## Opportunity Health Check — {DATE}

Total active opportunities: N
Healthy: N
At risk: N

### 🔴 AT_RISK Opportunities
| Opportunity | Stage | Days since update | Next Action | Task created |
|------|-------|-------------------|-------------|-------------|
| ... |

### ✅ Healthy Opportunities
(list opportunity names only — no table needed)
```

## Mode A — Manual (single opportunity)
User provides an opportunity name or ID → check only that opportunity, return detailed status.

## Mode B — Full scan (cron)
No input → scan all active opportunities, apply rules, update statuses, create tasks.
Silent if all opportunities are healthy (no output).
Only output/deliver if AT_RISK opportunities were found.

## Pitfalls
- `amount.amountMicros` ÷ 1,000,000 = USD value
- `lastUpdateDate` may be null — always fall back to `updatedAt`
- Don't create duplicate tasks — always check first with ExistingTasks query
- **Stage field confirmed values:** `NEW`, `SCREENING`, `MEETING`, `PROPOSAL`, `CUSTOMER` — NOT `NEW_LEAD`, `MEETING_SCHEDULED`, etc. The UPPER_SNAKE variants return a schema error.
- **dealStatus SELECT options (confirmed):** `HEALTHY`, `AT_RISK`, `NEEDS_FOLLOWUP`, `CANCELLED`
- Always localhost — never external URL
