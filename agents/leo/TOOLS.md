# Leo — BD Director Agent Tools

## Overview

Tools Leo reads from and writes to. These are shared infrastructure — Leo does not own them exclusively. Tools marked **Required** must be configured before Leo can operate. Tools marked **Optional** enhance quality but are not blockers.

---

## Core Tools

| Tool | Purpose | Required | Notes |
|------|---------|----------|-------|
| **Lark Base** | CRM — source of truth for all pipeline data | ✅ Required | App Token + Table IDs must be set. See `SCHEMA.md`. |
| **GBrain** | Long-term knowledge graph — deal narratives, company intel, relationship history | ✅ Required | Must be running before Leo starts. |
| **Hermes Cron** | Scheduling and running automated jobs | ✅ Required | All 6 cron jobs created in `SETUP.md` Step 4. |
| **Lark IM** | Delivering briefs, alerts, and draft batches to the sales rep | ✅ Required | Configured via `hermes setup lark`. |
| **Web Search (Tavily)** | Company research and account enrichment | ✅ Required | Set `TAVILY_API_KEY` in environment. |
| **Lark Docs / Drive** | Quotation and proposal PDF generation and storage | ✅ Required | Template tokens must be set in generating-quotations skill. |

---

## Optional Tools

| Tool | Purpose | Capability | Notes |
|------|---------|-----------|-------|
| **Content Engine (Lark Base)** | Published articles for personalised nurture messages | C5 | Wire in when Maya's content base is ready. Set table token in `lead-nurturing` skill. |

---

## Tool Access by Capability

| Capability | Lark Base | GBrain | Tavily | Lark IM | Lark Docs | Hermes Cron |
|------------|-----------|--------|--------|---------|-----------|-------------|
| C1 Maintaining Account Intelligence | ✅ | ✅ | ✅ | — | — | ✅ |
| C2 Progressing Deals to Close | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| C3 Progressing Partnerships to Agreement | ✅ | ✅ | — | ✅ | — | ✅ |
| C4 Monitoring Pipeline Health | ✅ | — | — | ✅ | — | ✅ |
| C5 Nurturing Cold Contacts | ✅ | ✅ | — | ✅ | — | ✅ |
| C6 Maintaining Partner Success | ✅ | ✅ | — | ✅ | — | ✅ |

---

## Configuration Checklist

Before running Leo for the first time:

- [ ] Lark Base app created, App Token recorded
- [ ] All 9 CRM tables created (see `SCHEMA.md`)
- [ ] All `{{TABLE_ID_*}}` placeholders replaced in skills
- [ ] GBrain running — `gbrain status` returns healthy
- [ ] Tavily API key set — `hermes config set search.tavily_api_key YOUR_KEY`
- [ ] Lark IM configured — `hermes setup lark` completed
- [ ] Quotation template created in Lark Docs, token set in `generating-quotations` skill
- [ ] Invoice template created in Lark Docs, token set in `generating-invoices` skill
- [ ] All 6 cron jobs created (see `SETUP.md` Step 4)
