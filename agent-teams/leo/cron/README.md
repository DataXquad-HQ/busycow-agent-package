# Leo — Cron Jobs

Scheduled jobs that run autonomously. Each cron calls a skill — no business logic lives in the cron itself.

Replace all `{{PLACEHOLDER}}` values with your instance-specific IDs before enabling.

---

## Daily Pipeline Reminder

**Schedule:** `0 1 * * 1-5` (weekdays only)

**Skills:** `daily-reminder`

**Deliver to:** `lark:{{LARK_SALES_CHANNEL_ID}}`

**Toolsets:** web, terminal, file

**Prompt:**
```
Run the daily-reminder skill. Pull all TODO tasks from Twenty CRM for all active Sales Reps. Apply the priority logic: today's tasks first, then tomorrow's, then this week's — cap at 10 per rep. Always flag overdue [Log Interaction] tasks. Add a suggested approach for each task based on opportunity context recalled from {{HINDSIGHT_PIPELINE_BANK}}. Deliver the reminder to the Sales Daily Update Lark channel (chat_id: {{LARK_SALES_CHANNEL_ID}}).
```

---

