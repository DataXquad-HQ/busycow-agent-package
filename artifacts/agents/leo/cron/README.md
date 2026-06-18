# Cron Jobs — BD Lead Agent (Leo)

Scheduled jobs that run autonomously. Each job calls a skill — the skill owns the business logic, while the cron template owns scheduling and delivery behavior.

---

## Before You Install

Replace every `{{PLACEHOLDER}}` in `jobs.json` before enabling any job.

| Placeholder | What it is |
|---|---|
| `{{SYSTEM_BACKEND_CHANNEL_ID}}` | Channel ID for ops logs and backend receipts |
| `{{SALES_DAILY_UPDATE_CHANNEL_ID}}` | Sales team's daily update channel |
| `{{OUTREACH_REVIEW_CHANNEL_ID}}` | Draft review channel for outreach approval |
| `{{PIPELINE_STRATEGY_CHANNEL_ID}}` | Weekly / monthly reporting channel for pipeline and strategy reports |
| `{{CRM_EXTERNAL_URL}}` | Public-facing CRM URL shown in human-facing messages |
| `{{AGENT_EMAIL}}` | Leo's mailbox address |
| `{{ORG_PREFIX}}` | Organisation prefix for Hindsight banks |
| `{{COMPANY_BLOG_URL}}` | Company blog or news URL |

---

## Installing

`jobs.json` is a reference template — it is **not** directly importable into Hermes. Create each job manually via the Hermes cron CLI.

```bash
hermes cron create \
  --profile <your-agent> \
  --name "Daily Pipeline Reminder" \
  --schedule "0 1 * * 1-5" \
  --skill sending-daily-pipeline-reminder \
  --prompt "..." \
  --deliver "feishu:{{SYSTEM_BACKEND_CHANNEL_ID}}"
```

Test each workflow interactively before scheduling it if the integration stack is new.

---

## Jobs

| Job | Schedule | Skill | What it does |
|---|---|---|---|
| **Daily Pipeline Reminder** | `0 1 * * 1-5` | `sending-daily-pipeline-reminder` | Sends the human-facing daily reminder to the sales team and returns only a backend receipt to ops. |
| **Lead Nurturing Scanner** | `0 1 * * *` | `nurturing-leads` | Finds overdue nurture-stage contacts, drafts personalised outreach, stores DRAFT OutreachMessages, and notifies the review channel. |
| **Outreach Message Sender** | `0 4 * * *` | `nurturing-leads` | Sends approved outreach, re-alerts overdue drafts, updates CRM, and logs Engagements. |
| **Inbox Monitor** | `0 2 * * *` | `monitoring-inbox-replies` | Checks the mailbox for inbound replies, logs them, and stays silent when there is no activity. |
| **Weekly Pipeline Health Check** | `0 1 * * 1` | `checking-pipeline-health` | Generates the full weekly report for the pipeline / strategy channel and returns only a short backend receipt. |
| **Monthly Pipeline Strategy Check** | `0 1 1 * *` | `checking-pipeline-strategy` | Generates the full monthly strategy report for the pipeline / strategy channel and returns only a short backend receipt. |
| **Monthly Account Intelligence Update** | `0 2 1 * *` | `enriching-accounts` | Refreshes active-account intelligence, delivers the human summary to the sales daily channel, and returns a short backend receipt. |

---

## Delivery Architecture

Use the shared `routing-report-delivery` rule:
- the **full human report** goes to the business-facing channel
- the **final cron response** stays short and goes to the backend/system channel
- do not duplicate the full report in the backend receipt

This especially applies to:
- Weekly Pipeline Health Check
- Monthly Pipeline Strategy Check
- Monthly Account Intelligence Update

---

## Recovery / Resume Handling

If a cron workflow pauses, fails, or needs replay:

1. **List first** — never guess the `job_id`
2. Use **`resume`** to restore a paused recurring schedule
3. Use **`run`** for an immediate retry / verification run
4. If the prompt, delivery target, or attached skills are wrong, **`update` first, then `run`**
5. Use **`remove`** only when the recurring job is no longer wanted

A recovery is only complete when:
- the schedule state is correct again, and
- the delivery path behaves correctly again

See the shared skill reference for the detailed decision tree:
- `artifacts/shared-skills/routing-report-delivery/references/cron-recovery.md`

---

## Notes

- Human-facing links must use `{{CRM_EXTERNAL_URL}}`, never localhost.
- Review-channel notifications should stay short; ops logs belong in the backend channel.
- If a report delivery fails, report the failure in the backend receipt — do not dump the full report there as a workaround.
