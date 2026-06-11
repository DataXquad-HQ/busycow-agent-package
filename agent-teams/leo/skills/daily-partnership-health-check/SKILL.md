---
name: daily-partnership-health-check
description: Daily automated check of all active partnerships. Identifies dormant partners (>14 days no engagement) and creates follow-up tasks.
version: 1.0.0
author: Leo (BD Director Agent)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sales, partnership, automation, crm, lark-base]
    related_skills: [managing-partnership-pipeline, engagement-logging]
---

# Daily Partnership Health Check

## ⚠️ SUPERSEDED — Use `reviewing-partnership-pipeline` Instead

This skill was an early design doc. The **authoritative, battle-tested workflow** is in:
→ `reviewing-partnership-pipeline` (Mode B — full scan)

Key discrepancies in THIS file vs. reality:
- Table ID `{{TABLE_ID}}` is WRONG — actual Partnerships table: `{{TABLE_ID}}`
- "Last Engagement Date" field **does not exist** — must infer from Activities table + Description
- Python SDK patterns below are NOT how Leo actually runs this — use `lark-cli base +record-upsert`

This file is kept for historical reference. Do NOT follow the algorithm or table IDs below.

---

## Overview (historical)

This skill runs daily at 03:00 Taiwan time (via cron job) to monitor all active partnerships. It identifies partners who haven't engaged in 14+ days and creates follow-up tasks to re-engage.

**Execution**: Completely automated via daily cron; no manual intervention required. Results are CRM state changes + task creation.

## When to Use

- **Scheduled**: Daily cron job (03:00 Taiwan time) — autonomous
- **Manual**: Run ad-hoc when you want to force a partnership health scan

## Data Model

### Input: Partnerships Table

Read from 🤝 Partnerships table ({{TABLE_ID}}):

| Field | Field ID | Purpose |
|---|---|---|
| Partner Name | {{FIELD_ID}} | Partner org name |
| Status | {{FIELD_ID}} | Current status (Active, Dormant, etc.) |
| Last Engagement Date | {{FIELD_ID}} | Date of most recent interaction |
| Engagement Type | {{FIELD_ID}} | Type of last interaction (Call, Email, Meeting, etc.) |
| Owner | {{FIELD_ID}} | Leo or assigned partner manager |

### Output: Actions

1. **Update Partner Status** (if applicable):
   - If days_since_engagement > 14 and status ≠ "Dormant" → Set status to "Dormant" or "Needs Follow-up"

2. **Create Re-engagement Task**:
   - Task name: `[PARTNER] {Partner Name} — Re-engagement check`
   - Description: Last engagement was {N} days ago on {date}. Schedule call or email to confirm status.
   - Due date: Today or Tomorrow (forces immediate action)
   - Assigned to: Partner owner (Leo if unassigned)
   - Tags: `partner-outreach`, `re-engagement`

## Algorithm

```python
# 1. Fetch all active partnerships
partners = fetch_from_lark(
    table_id="{{TABLE_ID}}",
    filter="Status in ('Active', 'Needs Follow-up')"  # Skip Dormant and Won
)

for partner in partners:
    last_engagement = partner.get("Last Engagement Date")
    days_since = (now - last_engagement).days
    
    # 2. Identify dormant partners
    if days_since > 14:
        
        # Update status
        update_partner(partner.id, {
            "Status": "Needs Follow-up",
            "Last Health Check": now
        })
        
        # Create re-engagement task
        create_task(
            title=f"[PARTNER] {partner['Partner Name']} — Re-engagement check",
            description=f"Last engagement: {last_engagement.format('MMM DD')} ({days_since} days ago). "
                       f"Engagement type: {partner.get('Engagement Type')}. "
                       f"Action: Call or email to confirm partnership status, discuss pipeline, and next steps.",
            due_date=today,
            assigned_to=partner.get("Owner") or "Leo",
            links={"partnership_record": partner.id}
        )
```

## Verification Checklist

- [ ] Connected to Lark Base (TAVILY_API_KEY not needed for this skill)
- [ ] All active partnerships fetched
- [ ] Days since last engagement calculated correctly
- [ ] Partners with >14 days flagged
- [ ] Status updated to "Needs Follow-up" (or similar)
- [ ] Re-engagement Task created with correct due date and owner
- [ ] Lark Task API response validated (got 200 OK)

## Daily Monitoring Report

When cron runs at 03:00, it logs summary:

```
🤝 Partnership Health Check — 2026-06-11 03:05

Total Active Partnerships: 12
Needs Follow-up (>14 days): 3
Tasks Created: 3

Flagged Partners:
  • Acme Reseller Group (16 days)
  • TechStart SI (18 days)
  • Global Logistics (15 days)

Check Tasks for re-engagement schedule.
```

No Lark notification is sent (that's handled by daily-briefing at 08:00).

## Implementation Notes

### Lark Base Connection

Use the standard Lark oapi SDK:

```python
from lark_oapi import Client

client = Client.builder() \
    .app_id(LARK_APP_ID) \
    .app_secret(LARK_APP_SECRET) \
    .build()

# Query partnerships
request = GetAppTableRecordRequest.builder() \
    .app_token("MtvNbgCHXaRAaUsWXsCjnekep2g") \
    .table_id("{{TABLE_ID}}") \
    .filter('fields."Status" = "Active"') \
    .build()

response = client.bitable.v1.appTableRecord.search(request)
```

### Task Creation via Lark Task API

Use the Lark Task API to create follow-up tasks:

```python
from lark_oapi.service.task.v1 import *

create_request = CreateTaskRequest.builder() \
    .title(f"[PARTNER] {partner_name} — Re-engagement check") \
    .description("...") \
    .due_date(today) \
    .assignees([owner_id]) \
    .custom_fields({"partnership_id": partner_id}) \
    .build()

response = client.task.v1.task.create(create_request)
```

## Common Pitfalls

1. **Using >21 days instead of >14 days**
   - Partnership cycles move faster than deal cycles
   - 14 days is the right threshold for "dormant"
   - Adjust if your partners are slower to engage

2. **Flagging recently-acquired partners as dormant**
   - Add filter: Only check partners with status = "Active" (not "New" or "Onboarding")
   - New partners get grace period (set Last Engagement Date to today on acquisition)

3. **Creating tasks but not assigning them**
   - Always assign to partner owner or default to Leo
   - Unassigned tasks get lost

4. **Over-creating tasks**
   - Don't create a new task if one already exists for this partner this week
   - Check: Is there an open task with tag "partner-outreach" for this partner created in past 7 days?
   - If yes, skip task creation (already flagged)

## Cron Integration

**Schedule**: Every day at 03:00 Taiwan time
**Frequency**: `0 3 * * *` (cron expression)

This runs before deal-health-check (if both are at 03:00, stagger by 5 min to avoid API throttling):
- 03:00 — daily-partnership-health-check
- 03:05 — daily-deal-health-check (offset by 5 minutes)

**Next scheduled run**: [auto-filled by cron system]
**Delivery**: CRM state changes + task creation (no Lark notification — briefing handles that)
