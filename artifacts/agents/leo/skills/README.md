# Skills — BD Lead Agent (Leo)

Each skill is a self-contained folder. Copy the entire folder when installing — not just `SKILL.md`.

```bash
cp -r artifacts/agents/leo/skills/* ~/.hermes/profiles/<your-agent>/skills/
```

After copying, restart your Hermes session. Replace any `{{PLACEHOLDER}}` values before first use.

---

## BD Capabilities

Skills that implement Leo's active BD operating model.

| Skill | What it does | Capability |
|---|---|---|
| `capturing-leads` | Capture new contacts from networking / events / referrals into CRM as Leads | C1 |
| `prospect-scouting` | Analyse a raw prospect list, prioritise targets, and suppress accounts already in motion | C1 |
| `enriching-accounts` | Foundational and monthly account intelligence enrichment | C3 |
| `monitoring-account-signals` | Watch named accounts for fresh why-now, momentum, or risk signals | C3 |
| `nurturing-leads` | Draft and send monthly personalised outreach for nurture-stage contacts | C4 |
| `monitoring-inbox-replies` | Poll inbox for inbound replies; log engagement and notify the team | C4 |
| `drafting-call-followups` | Turn a meeting or transcript into recap, follow-up draft, and CRM-ready internal summary | C4 |
| `log-engagement` | Convert a raw interaction into structured CRM Engagement + follow-up tasks | C5 |
| `handling-pipeline-interactions` | Process opportunity / partnership updates from the human operator | C5 |
| `creating-report-back-tasks` | Create report-back tasks for future meetings, demos, and promised follow-ups | C5 |
| `advising-on-tasks` | Give context-driven advice for how to execute a specific CRM task | C5 |
| `sending-daily-pipeline-reminder` | Morning task reminder with due-soon and overdue emphasis | C5 |
| `planning-deal-strategy` | Build a grounded opportunity strategy pack with stakeholder map, risks, and next moves | C5 |
| `preparing-customer-meetings` | Build concise meeting briefs and daily external-meeting digests | C5 |
| `analyzing-competitive-intelligence` | Build competitor comparisons, objection handling, and account-specific positioning guidance | C5 |
| `creating-sales-assets` | Create one-pagers, executive summaries, workflow narratives, and other customer-facing assets | C5 |
| `checking-pipeline-health` | Weekly pipeline coverage, hygiene, stalled-motion, and swing-opportunity review | C6 |
| `checking-pipeline-strategy` | Monthly strategy and memory-layer review | C6 |
| `reviewing-sales-forecast` | Review commit posture, slip risk, and in-period forecast confidence | C6 |
| `ingesting-sales-strategy` | Load strategy documents into long-term memory so health checks can reason against them | C6 |

---

## Infrastructure / Shared-Core Skills

These are packaged here because Leo actively uses them, even when they also exist in the shared-skills layer.

| Skill | What it enables |
|---|---|
| `twenty-crm` | Query and mutate CRM objects via GraphQL |
| `openmail` | Send and receive email through the agent mailbox |
| `capturing-to-gbrain` | Write durable knowledge into GBrain |
| `routing-report-delivery` | Keep full reports and short cron receipts on one contract; includes cron recovery guidance |
| `managing-skills` | Create, patch, and maintain Hermes skills |
| `managing-shared-skills` | Apply shared-skill governance and rollout rules |
| `skill-creator` | Build and refine skills with explicit Quality Bar and Fallback Behavior sections |
| `packaging-to-github` | Publish generalized reusable assets into the package repo |

---

## Notes

- Lark / Feishu-specific skills are intentionally **not** packaged in Leo's agent artifact here.
- Shared-core skills may also exist under `artifacts/shared-skills/`; they are duplicated here for agent completeness.
- Cron templates live in `../cron/` and should be installed separately.
