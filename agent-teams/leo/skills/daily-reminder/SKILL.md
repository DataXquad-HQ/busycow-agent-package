---
name: daily-reminder
description: >
  Generate and deliver a daily action reminder to all active Sales Reps.
  Surfaces tasks due today and tomorrow first, expands to this week if total
  is under 10. Covers all reps, not just Hunter. Each task includes who owns
  it and a suggested approach. Designed to be run by cron every morning.
triggers:
  - "daily reminder"
  - "what do I need to do today"
  - "today's tasks"
  - "send daily reminder"
  - "今天要做什麼"
  - "daily briefing"
version: "1.0"
author: {{COMPANY_NAME}}/Leo
---

# Daily Reminder

> The goal is simple: every active Sales Rep starts their day knowing exactly
> what they must do — and how to do it. Nothing lives only in Leo's memory.

---

## Purpose

Every morning, Leo:
1. Pulls all TODO tasks from Twenty CRM across all active reps
2. Prioritises by deadline (today → tomorrow → this week)
3. Caps at 10 tasks total per rep — closest deadlines first
4. Adds a suggested approach for each task
5. Delivers to the Sales Daily Update channel

---

## Who Gets Reminded

All people with active assigned tasks in CRM. Currently:
- **Hunter** — primary Sales Rep
- *(add new reps here as they join)*

Run the same logic for each rep. Deliver one consolidated message per rep,
or a single team message if preferred.

---

## Task Priority Logic

```
Layer 1 — Due TODAY (deadline = today)
Layer 2 — Due TOMORROW (deadline = tomorrow)

Count tasks from Layer 1 + Layer 2.

If total < 10:
  Layer 3 — Due THIS WEEK (deadline within 7 days, not already included)
  Add from Layer 3 until total reaches 10 or list is exhausted.

If total >= 10 at any layer: stop. Do not add more.
Cap = 10 tasks per rep.
```

**Special priority — always include regardless of cap:**
- Any task with title starting `[Log Interaction]` that is overdue
  → This means a meeting happened but was never reported back. Flag it clearly.
- Any task linked to an `AT_RISK` opportunity or partnership

---

## Task Output Format

For each task:
```
[Priority emoji] [Task title]
👤 Owner: [Rep name]
📅 Due: [date] ([today/tomorrow/this week])
🔗 Opportunity: [Opportunity or Partnership name] — [Stage] — [healthCheck]
💡 Suggested: [1-2 sentence recommended approach]
```

Priority emoji:
- 🔴 Overdue or AT_RISK opportunity
- 🟡 Due today or tomorrow
- 🔵 Due this week

**Special flag for unreported meetings:**
```
⚠️ [Log Interaction] — [Company] meeting on [date] not yet reported
👤 Owner: [Rep]
💡 Just message Leo with a quick update — even one line is enough to start.
```

---

## Full Delivery Format

```
📋 Daily Pipeline Reminder — [Date]

**[Rep Name]'s Tasks ([N] items)**

🔴 [task 1]
🟡 [task 2]
🔵 [task 3]
...

---
💬 To log a completed interaction, just message Leo.
📊 To see full pipeline status, ask Leo for a pipeline review.
```

If multiple reps: repeat the block per rep in the same message.

---

## Step-by-Step

### Step 1 — Pull tasks from CRM

```graphql
{
  tasks(filter: {
    status: { eq: TODO }
    dueAt: { lte: "[end-of-week-ISO]" }
  }) {
    edges { node {
      id
      title
      dueAt
      assignee { id name }
      taskTargets {
        edges { node {
          targetOpportunity { id name stage healthCheck }
          targetPartnership { id name stage healthCheck }
        }}
      }
    }}
  }
}
```

Also pull overdue tasks (dueAt < today, status still TODO):
```graphql
{
  tasks(filter: {
    status: { eq: TODO }
    dueAt: { lt: "[today-ISO]" }
  }) {
    edges { node { id title dueAt assignee { id name } } }
  }
}
```

### Step 2 — Group by rep, apply priority logic

For each rep:
1. Collect all their TODO tasks
2. Sort: overdue first, then by dueAt ascending
3. Apply layer logic (today → tomorrow → this week), cap at 10
4. Always include `[Log Interaction]` overdue tasks even if over cap

### Step 3 — Recall context for AT_RISK opportunities

For any task linked to an AT_RISK opportunity, recall from {{HINDSIGHT_PIPELINE_BANK}}:
```
POST /v1/default/banks/{{HINDSIGHT_PIPELINE_BANK}}/memories/recall
{"query": "[Company] opportunity — current blocker and last interaction", "top_k": 3}
```
Use this to write a better suggested approach.

### Step 4 — Generate and deliver

Compose the message and deliver to the Sales Daily Update channel:

```
Lark group: {{SALES_CHANNEL_NAME}}
chat_id: {{LARK_SALES_CHANNEL_ID}}
```

---

## Pitfalls

- **Don't include completed tasks.** Filter `status: { eq: TODO }` only.
- **Don't exceed 10 per rep.** Closest deadlines always win.
- **Always flag unreported meetings.** `[Log Interaction]` overdue = silent opportunity risk.
- **Suggested approach must be specific.** "Follow up" is not enough. Say how, say what angle.
- **If a task has no linked opportunity**, still include it — just omit the opportunity line.

---

## Cron Schedule

Run every weekday morning at 09:00 Taiwan time (01:00 UTC).

```
cron: 0 1 * * 1-5
deliver to: {{LARK_SALES_CHANNEL_ID}}
```
