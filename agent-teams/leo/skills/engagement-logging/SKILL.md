---
name: engagement-logging
description: >
  Use when a customer or partner interaction update is provided. Multi-turn
  conversation to extract engagement details, log to Twenty CRM (engagement object),
  mark completed Tasks, and trigger deal-progressing. Use when user says "跟客戶聊了",
  "有個 meeting", "剛打了電話", "partner 有動靜", or dumps a block of interaction notes.
triggers:
  - "跟客戶聊了"
  - "有個 meeting"
  - "剛打了電話"
  - "partner 有動靜"
  - "log engagement"
  - "記錄互動"
version: "3.0"
author: Leo (BD Director Agent)
---

# Engagement Logging

## Purpose

Capture every customer or partner interaction into Twenty CRM as an Engagement record. After logging, trigger `deal-progressing` to recalculate deal health.

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost)
**GraphQL endpoint:** `http://localhost:3001/graphql`

**Engagement object:** `engagement` (custom object)

### Engagement Fields
| Field | Twenty field name | Type |
|---|---|---|
| Name (primary) | `name` | TEXT |
| Type | `engagementType` | SELECT |
| Status | `engagementStatus` | SELECT |
| Channel | `channel` | SELECT |
| Date | `engagementDate` | DATE_TIME |
| Notes | `engagementNote` | RICH_TEXT |
| Next Action | `nextAction` | TEXT |
| Outcome | `outcome` | TEXT |
| Company | `company` | RELATION → company |
| Opportunity | `opportunity` | RELATION → opportunity (optional) |
| Partnership | `partnership` | RELATION → partnership (optional) |
| Client Attendees | `clientAttendees` | RELATION → person |

### `engagementType` options
`PHONE` / `INPERSON` / `ONLINE` / `MESSAGING` / `DEMO` / `EMAIL` / `EVENT`

### `engagementStatus` options
`PLANNED` / `COMPLETED`

### `channel` options
`EMAIL` / `WHATSAPP` / `LINE` / `PHONE` / `IN_PERSON` / `ZOOM` / `TEAMS`

---

## Planned vs Completed

- **Planned** — future meeting already booked. Used by `meeting-prep` cron.
- **Completed** — interaction already happened. Triggers `deal-progressing`.

When creating a Planned Engagement, `outcome` and `nextAction` can be left blank — fill them after the meeting.

---

## Nurture Engagements (no Deal/Partnership)

When logging a nurture outreach (check-in to a cold contact):
- Set `company` and `clientAttendees` (person) as normal
- **Leave `opportunity` empty** — do not link to any Deal
- **Leave `partnership` empty**
- This keeps nurture activity out of pipeline views

---

## Workflow

### Step 1: Multi-Turn Extraction

Ask in order:
```
Q1: What type of interaction? (Call / Meeting / Email / Message / Demo / Event)
Q2: Which company / deal / partnership is this for?
Q3: Who attended? (contacts present)
Q4: What happened? Key outcomes, decisions, new information?
Q5: What is the next action?
Q6: Did you complete any existing tasks today?
```

Confirm before writing: "This is a [type] with [company] on [date] for [deal/partnership]. Correct?"

---

### Step 2: Create Engagement Record

```graphql
mutation CreateEngagement($input: CreateOneEngagementInput!) {
  createEngagement(input: $input) {
    id
    name
    engagementDate
  }
}
```

Variables:
```json
{
  "input": {
    "engagement": {
      "name": "{YYYY-MM-DD} — {company_name} ({context})",
      "engagementType": "{type}",
      "engagementStatus": "COMPLETED",
      "channel": "{channel}",
      "engagementDate": "{datetime_iso}",
      "engagementNote": "{notes}",
      "nextAction": "{next_action}",
      "outcome": "{outcome_summary}",
      "companyId": "{company_id}",
      "opportunityId": "{opportunity_id_or_null}",
      "partnershipId": "{partnership_id_or_null}"
    }
  }
}
```

After creating the engagement, link client attendees via relation if known:
```graphql
mutation {
  updateEngagement(id: "{engagement_id}", input: {
    engagement: {
      clientAttendees: { connect: [{ id: "{person_id}" }] }
    }
  }) { id }
}
```

---

### Step 3: Mark Completed Tasks

If user mentions completing existing tasks, find and update them:

```graphql
query {
  tasks(filter: {
    and: [
      { taskTargets: { opportunity: { id: { eq: "{opportunity_id}" } } } }
      { status: { neq: "DONE" } }
    ]
  }) {
    edges { node { id title { text } } }
  }
}
```

Update each completed task:
```graphql
mutation {
  updateTask(id: "{task_id}", input: {
    task: { status: "DONE" }
  }) { id status }
}
```

---

### Step 4: Auto-Create Follow-up Task (if next action is clear)

If `nextAction` is specific and actionable, create a Task:

```graphql
mutation {
  createTask(input: {
    task: {
      title: { text: "{next_action}" }
      status: "TODO"
      dueAt: "{due_date_iso}"
      taskPriority: "MEDIUM"
      agentAdvice: "{leo_advice_for_this_task}"
    }
  }) { id title { text } }
}
```

Then link to deal or partnership via taskTargets:
```graphql
mutation {
  updateTask(id: "{task_id}", input: {
    task: {
      taskTargets: {
        connect: { opportunityId: "{opportunity_id}" }
      }
    }
  }) { id }
}
```

---

### Step 5: Trigger deal-progressing

After engagement is saved, invoke `deal-progressing` with the opportunity ID. Skip if this is a nurture engagement (no opportunity linked).

---

### Step 6: GBrain Sync

```python
# Add timeline entry to company page
mcp_gbrain_add_timeline_entry(
    slug=f"companies/{company_slug}",
    date=engagement_date,
    summary=f"{engagement_type} — {outcome_summary}",
    detail=f"{notes}\n\nNext Action: {next_action}",
    source="twenty-crm"
)

# Extract facts from notes
mcp_gbrain_extract_facts(
    turn_text=f"{notes}\n{outcome_summary}",
    entity_hints=[f"companies/{company_slug}"]
)
```

---

## Verification Checklist

- [ ] Engagement type, date, and company confirmed with user
- [ ] Engagement record created — got `id` back
- [ ] Client attendees linked (if known)
- [ ] Completed tasks marked DONE (if any mentioned)
- [ ] Follow-up task created (if next action is clear)
- [ ] `deal-progressing` triggered (if opportunity linked)
- [ ] GBrain timeline entry added
- [ ] User received confirmation

---

## Pitfalls

1. **Always use localhost** — never external URL.

2. **Nurture engagements — leave opportunity/partnership null** — keeping them out of pipeline views is intentional.

3. **Planned engagements don't trigger deal-progressing** — only Completed ones do.

4. **`engagementDate` format** — ISO 8601: `"2026-06-11T14:30:00.000Z"`.

5. **`engagementNote` is RICH_TEXT** — Twenty stores it as JSON. For plain text input, wrap: `{ "root": { "children": [{ "children": [{ "text": "...", "type": "text" }], "type": "paragraph" }], "type": "root" } }`. Or check Twenty's current RICH_TEXT format via a test query.

6. **Don't create vague tasks** — "follow up soon" is not a task. If the next action isn't specific, ask: "What exactly needs to happen, by when, and by whom?"
