---
name: reviewing-partnership-pipeline
description: >
  Review all active partnerships for health in Twenty CRM — detect silence
  (14+ days no engagement), flag dormant partners, and create re-engagement tasks.
  Triggered manually ("幫我看一下 partnership 狀況") or by daily cron.
triggers:
  - "幫我看一下 partnership 狀況"
  - "有哪些 partner 沒動靜了"
  - "partnership health"
  - "partner review"
version: "3.0"
author: Leo (BD Director Agent)
---

# Reviewing Partnership Pipeline

## Purpose

Scan all active partnerships in Twenty CRM, flag any that have gone quiet (14+ days), and create re-engagement tasks. Silent if all partnerships are healthy.

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost)
**GraphQL endpoint:** `http://localhost:3001/graphql`

---

## Two Modes

### Mode A: Specific Partnership
Check health of one named partner. Pull last engagement, status, open tasks.

### Mode B: Full Scan (cron or on-demand)
Scan all non-Inactive partnerships. Flag any with 14+ days no update. Create tasks. Report summary.

---

## Workflow

### Step 1: Fetch Active Partnerships

```graphql
query {
  partnerships(
    filter: {
      and: [
        { stage: { neq: "INACTIVE" } }
      ]
    }
    orderBy: { lastUpdateDate: AscNullsFirst }
  ) {
    edges {
      node {
        id name stage status
        currentStatusSummary lastUpdateDate
        primaryContact { id name { firstName lastName } }
        company { id name }
        engagements(
          orderBy: { engagementDate: DescNullsLast }
          first: 1
        ) {
          edges {
            node { engagementDate engagementType outcome }
          }
        }
      }
    }
  }
}
```

---

### Step 2: Evaluate Each Partnership

```
for each partnership:
  days_since_update = (today - lastUpdateDate).days

  if days_since_update > 14:
    → flag as NEEDS_FOLLOWUP
    → check if re-engagement task already exists (open task within last 7 days)
    → if no existing task: create re-engagement task
    → update partnership status to NEEDS_FOLLOWUP
```

Check for existing task:
```graphql
query {
  tasks(filter: {
    and: [
      { title: { text: { like: "%{partner_name}%" } } }
      { status: { neq: "DONE" } }
      { createdAt: { gte: "{7_days_ago_iso}" } }
    ]
  }) {
    edges { node { id title { text } } }
  }
}
```

Create task if needed:
```graphql
mutation {
  createTask(input: {
    task: {
      title: { text: "[PARTNER] {Partner Name} — {N} days no activity" }
      status: "TODO"
      dueAt: "{today_iso}"
      taskPriority: "MEDIUM"
      agentAdvice: "Last engagement: {date} ({type}). Outcome: {outcome}. Suggested: check in with {contact_name} to ask about their pipeline activity, any questions on our product, or blockers to moving to next stage."
      partnership: { connect: { id: "{partnership_id}" } }
    }
  }) { id }
}
```

Update partnership status:
```graphql
mutation {
  updatePartnership(id: "{id}", input: {
    partnership: { status: "NEEDS_FOLLOWUP" }
  }) { id status }
}
```

---

### Step 3: Output

**Mode A:**
```
🤝 Partnership Health — {Partner Name}

Stage: {stage} | Status: {status}
Last update: {N} days ago ({type} — {outcome})
Open tasks: {N}

Assessment: {Healthy | Needs Follow-up | Dormant}
Recommended action: {one sentence}
```

**Mode B (cron / full scan):**
- **If all healthy → silent.** Send nothing.
- If dormant partnerships found:
```
🤝 Partnership Health Check — {DATE}

Dormant (14+ days): {N}
Tasks created: {N}

{Partner Name} — {N} days
→ {recommended action}
```

---

## Pitfalls

1. **Always use localhost** — never external URL.

2. **Silent when healthy** — Mode B sends nothing if all partnerships are on track. Do not send "all good" messages.

3. **Don't duplicate tasks** — check for existing open task before creating. Only create if none exists within last 7 days.

4. **New partnerships get a grace period** — partners onboarded in the last 14 days should not be flagged.

5. **`lastUpdateDate` may be null** — fall back to `updatedAt` for recency check. If both null, treat as "no recent activity" and flag.
