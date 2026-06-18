# Agent Design Spec — Leo

> **Status:** ✅ Deployed (C2 Outbound Prospecting pending)
> **Last Updated:** 2026-06-18
> **Build artifacts:** `~/.hermes/profiles/leo/SOUL.md`, `~/.hermes/profiles/leo/skills/`

---

## Part 1 — Core Need & Positioning

### 1a. Why This Agent Exists

The company needs to grow revenue across multiple business lines simultaneously. Humans cannot personally manage every prospect, follow up on every lead, and monitor every deal — the cognitive load is too high and the speed too slow.

Leo exists to be the attention the sales rep buys back. Every prospect gets contacted. Every lead gets followed up. Every deal gets monitored. The human focuses on relationships and decisions; Leo handles the engine underneath. Without Leo, deals go quiet, leads go cold, and pipeline visibility is zero.

---

### 1b. Role & Goal

| Field | Value |
|---|---|
| **Name** | Leo |
| **Title** | BD Lead Agent |
| **One-line goal** | No prospect left un-emailed. No lead going quiet. No deal stalling without a recovery plan. |
| **The number it owns** | Partner count × Pipeline value × Conversion rate |
| **Primary human contact** | Human (BD decisions, outreach approval) |

---

### 1c. Team Positioning

| | Role | What flows |
|---|---|---|
| **Receives from** | Human | Source lists, outreach approval, deal context, strategy direction |
| **Receives from** | Growth Agent | Inbound leads (enter CRM as LEAD) |
| **Hands off to** | Human | Drafted outreach (for approval before send), deal recommendations, daily reminders |
| **Does NOT own** | Inbound lead gen (Growth Agent), post-sign customer success (Customer Success Agent), final deal sign-off (Human) |

---

## Part 2 — Context & Data Layer

### 2a. What Leo Needs to Know

| What Leo needs to know | Source | How it reads it |
|---|---|---|
| ICP for each BL | GBrain vault | Direct file: `internal/business-lines/[bl]/icp.md` |
| Sales strategy per BL | GBrain vault | Direct file: `internal/business-lines/[bl]/strategy.md` |
| Product overview per BL | GBrain vault | Direct file: `internal/business-lines/[bl]/product.md` |
| GTM motion per BL | GBrain vault | Direct file: `internal/business-lines/[bl]/gtm.md` |
| Company background | GBrain vault | Direct file: `internal/company/overview.md` |
| External company facts + relationships | GBrain MCP | `mcp_gbrain_get_page("external/entities/companies/[slug]")` |
| People at target company | GBrain MCP | `mcp_gbrain_traverse_graph("external/entities/companies/[slug]", link_type="works_at")` |
| Recent interactions with a deal | Hindsight | `[org]-pipeline` bank recall |
| Human communication preferences | Hindsight | `[org]-human-[name]` bank |

**GBrain content that must exist before Leo is fully useful:**

| Document | Slug | Status |
|---|---|---|
| BL ICP | `internal/business-lines/[bl]/icp.md` | ✅ File exists — needs content |
| BL strategy | `internal/business-lines/[bl]/strategy.md` | ✅ File exists — needs content |
| BL product | `internal/business-lines/[bl]/product.md` | ✅ File exists — needs content |
| BL GTM | `internal/business-lines/[bl]/gtm.md` | ✅ File exists — needs content |

---

## Part 3 — Capabilities

### 3a. Capabilities Overview

| # | Capability | What it means | Skills | Status |
|---|---|---|---|---|
| C1 | Lead Capture | Onboard contacts from humans or events into CRM; scout and prioritise raw prospect lists | `capturing-leads`, `prospect-scouting` | ✅ Built |
| C2 | Outbound Prospecting | Run cold email sequences for qualified prospects from first contact to reply | *(to build)* | 🔧 Pending |
| C3 | Account Intelligence | Enrich prospect/lead context before outreach or meetings; monitor account watchlists for fresh commercial signals | `enriching-accounts`, `monitoring-account-signals` | ✅ Built |
| C4 | Lead Nurturing | Draft monthly personalised follow-ups; monitor inbox for inbound replies; turn meetings into follow-up packages | `nurturing-leads`, `monitoring-inbox-replies`, `drafting-call-followups` | ✅ Built |
| C5 | Pipeline Progressing | Log every interaction; prepare meetings; plan opportunity strategy; create sales assets; surface daily tasks to human | `log-engagement`, `handling-pipeline-interactions`, `creating-report-back-tasks`, `advising-on-tasks`, `sending-daily-pipeline-reminder`, `planning-deal-strategy`, `preparing-customer-meetings`, `analyzing-competitive-intelligence`, `creating-sales-assets` | ✅ Built |
| C6 | Pipeline Health Monitoring | Weekly pipeline coverage check; forecast review; monthly strategy and memory freshness review | `checking-pipeline-health`, `checking-pipeline-strategy`, `ingesting-sales-strategy`, `reviewing-sales-forecast` | ✅ Built (needs BL docs) |

---

### 3b. Skills

**Capability Skills**

| Skill | Capability | What it does |
|---|---|---|
| `capturing-leads` | C1 | Onboard new contacts from events / networking / referrals into CRM as Leads |
| `prospect-scouting` | C1 | Analyse a raw list and surface who is worth prioritising, with reasoning |
| `enriching-accounts` | C3 | Enrich company and contact context — Level 1 (new Lead) and Level 2 (monthly update) |
| `monitoring-account-signals` | C3 | Monitor named accounts or watchlists for fresh why-now signals, risk, and momentum |
| `nurturing-leads` | C4 | Draft and send monthly personalised outreach to NURTURE / OPPORTUNITY tier Leads |
| `monitoring-inbox-replies` | C4 | Poll inbox for inbound replies, log Engagements, create follow-up Tasks, notify sales team |
| `drafting-call-followups` | C4 | Convert a meeting, transcript, or notes into recap, follow-up draft, and CRM-ready internal summary |
| `log-engagement` | C5 | Log a completed meeting / call / email / demo into CRM and Hindsight |
| `handling-pipeline-interactions` | C5 | Process any human update about an Opportunity or Partnership |
| `creating-report-back-tasks` | C5 | Create a Report-Back Task whenever a future meeting or demo is mentioned |
| `advising-on-tasks` | C5 | Provide deep, context-driven advice on how to approach a specific CRM Task |
| `sending-daily-pipeline-reminder` | C5 | Generate and deliver the daily task reminder to all active Sales Reps |
| `planning-deal-strategy` | C5 | Build a grounded opportunity strategy pack with stakeholder map, risks, and prioritized next actions |
| `preparing-customer-meetings` | C5 | Build concise, source-backed meeting briefs and daily external-meeting digests |
| `analyzing-competitive-intelligence` | C5 | Build competitor comparisons, objection handling, and account-specific positioning guidance |
| `creating-sales-assets` | C5 | Create customer-facing one-pagers, executive summaries, workflow narratives, and similar sales assets |
| `ingesting-sales-strategy` | C6 | Read strategy docs from GBrain and store key insights into Hindsight |
| `checking-pipeline-health` | C6 | Weekly pipeline review — coverage ratio, gaps to target, stalled items |
| `checking-pipeline-strategy` | C6 | Monthly strategy review — memory layer freshness, trend analysis, strategic signals |
| `reviewing-sales-forecast` | C6 | Review in-period forecast posture, commit risk, and swing opportunities |

**General Skills**

| Skill | Purpose |
|---|---|
| `capturing-to-gbrain` | Write external entities and facts to GBrain |
| `routing-report-delivery` | Keep full human reports and short cron receipts on one shared delivery pattern |
| `lark-im` | Send messages to human and Lark channels |
| `managing-skills` | Maintain and update own skills |
| `managing-shared-skills` | Apply shared-skill governance and rollout rules when selective distribution matters |
| `skill-creator` | Build or refine skills with explicit Quality Bar and Fallback Behavior sections |
| `packaging-to-github` | Publish generalized reusable assets into the external package repo when needed |

---

### 3c. Cron Jobs

| Job | Schedule | Capability | Delivers to |
|---|---|---|---|
| Daily Pipeline Reminder | Mon–Fri 01:00 UTC | C5 | `[Sales] Daily Update` |
| Lead Nurturing Scanner | Daily 01:00 UTC | C4 — draft creation | `[Sales] Nurturing Review` + `[System] Backend Report` |
| Outreach Message Sender | Daily 04:00 UTC | C4 — send approved emails | `[System] Backend Report` |
| Inbox Monitor | Daily 02:00 UTC | C4 — inbound reply tracking | Silent if no replies; `[System] Backend Report` on activity |
| Weekly Pipeline Health Check | Monday 01:00 UTC | C6 | `[Sales] Pipeline and Strategy` |
| Monthly Pipeline Strategy Check | 1st of month 01:00 UTC | C6 | `[Sales] Pipeline and Strategy` |
| Monthly Account Intelligence Update | 1st of month 02:00 UTC | C3 | `[Sales] Daily Update` |

---

### 3d. Delivery Channels

| Channel | Purpose |
|---|---|
| `[Sales] Daily Update` | Daily pipeline reminder and task list for sales team |
| `[Sales] Nurturing Review` | Outreach drafts pending human approval before send |
| `[Sales] Pipeline and Strategy` | Weekly health check and monthly strategy reports |
| `[System] Backend Report` | Cron ops logs, errors, run stats — internal only |

---

## Part 4 — Tools & Permissions

### 4a. Tools Required

| Tool / Skill | Purpose |
|---|---|
| `twenty-crm` | All CRM read/write via GraphQL — foundational layer for all pipeline operations |
| `openmail` | Send/receive email via agent's dedicated mailbox |
| `web` (Tavily) | Web research for account enrichment and prospect scouting |
| `capturing-to-gbrain` | Write external entities and facts to GBrain |
| `lark-im` | Send messages to human and Lark channels |
| `managing-skills` | Maintain and update own skills |

---

### 4b. Credentials & Environment

> Every agent owns its own complete set of credentials. No inheritance, no cross-profile access. Shared credentials are duplicated into each agent's `.env` independently.

| Service | Purpose | `.env` key |
|---|---|---|
| Anthropic | LLM inference | `ANTHROPIC_API_KEY` |
| OpenRouter | LLM fallback | `OPENROUTER_API_KEY` |
| Twenty CRM | Pipeline read/write | `TWENTY_API_KEY` |
| OpenMail | Email send/receive | Agent mailbox token |
| Feishu Bot | Lark messaging | `FEISHU_APP_ID`, `FEISHU_APP_SECRET` |
| Hindsight | Pipeline bank read/write | `HINDSIGHT_BASE_URL` |
| Tavily | Web search for enrichment | `TAVILY_API_KEY` |

---

### 4c. Build Mapping

| Spec Section | Build Artifact | Location |
|---|---|---|
| 1b. Role & Goal | `SOUL.md` — Who Leo Is | `~/.hermes/profiles/leo/SOUL.md` |
| 1c. Team Positioning | `SOUL.md` — Position in the Team | `~/.hermes/profiles/leo/SOUL.md` |
| 2a. Context sources | `SOUL.md` — Knowledge Sources | `~/.hermes/profiles/leo/SOUL.md` |
| 3a. Capabilities | `SOUL.md` — Capabilities list | `~/.hermes/profiles/leo/SOUL.md` |
| 3b. Skills | Skills directory | `~/.hermes/profiles/leo/skills/` |
| 3c. Cron jobs | Hermes cron config | `artifacts/agents/leo/cron/jobs.json` |
| 4a. Tools | Skills in SOUL.md | `~/.hermes/profiles/leo/skills/` |
| 4b. Credentials | Per-profile `.env` | `~/.hermes/profiles/leo/.env` |

---

## Spec Status

| Section | Status |
|---|---|
| Part 1 — Core Need & Positioning | ✅ Complete |
| Part 2 — Context & Data Layer | ✅ Complete |
| Part 3 — Capabilities | ✅ Complete |
| Part 4 — Tools & Permissions | ✅ Complete |
| GBrain BL content filled | 📝 Files exist — content needed |
| Hindsight banks | ✅ `[org]-pipeline`, `[org]-agent-leo` |
| SOUL.md | ✅ Deployed |
| C1, C3, C4, C5, C6 skills | ✅ Built |
| C2 Outbound Prospecting | 🔧 Pending build |
| Cron jobs | ✅ Configured in `jobs.json` |
