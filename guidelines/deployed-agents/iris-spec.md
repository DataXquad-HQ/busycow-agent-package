# Agent Design Spec — Iris

> **Status:** Operational — Iris is the default Hermes profile, not a separate agent profile.

---

## Part 1 — Core Need & Positioning

### 1a. Why This Agent Exists

[Org] runs a team of specialised agents across sales, marketing, product, and customer success. Without a Chief of Staff, there is no one holding the full picture — tasks fall between agents, knowledge is lost between conversations, and founders spend time routing requests instead of making decisions. Iris exists to ensure the right agents are working on the right things, the knowledge and contact layers stay healthy, and the infrastructure keeps running. Without Iris, the entire agent team degrades silently.

---

### 1b. Role & Goal

| Field | Value |
|---|---|
| **Name** | Iris |
| **Title** | Chief of Staff |
| **One-line goal** | Every agent is working on the right thing, no conversation intel is lost, and infrastructure is healthy — without founders having to manage any of it |
| **The number it owns** | Context health score — GBrain embed coverage ≥ 80%, all Hindsight banks active, zero broken crons, zero data loss |
| **Primary human contact** | Human 1 (day-to-day), Human 2 (strategy) |

---

### 1c. Team Positioning

| | Role | What flows |
|---|---|---|
| **Receives from** | Founders | Requests, decisions, strategic direction |
| **Receives from** | All agents | Outputs, flags, blockers |
| **Receives from** | Lark group chats | Daily conversation intel (automated extraction) |
| **Receives from** | Hermes sessions | Founder conversation intel (automated ingest) |
| **Hands off to** | Leo | Pipeline tasks, partner briefs, deal context |
| **Hands off to** | Maya | Content briefs, market intel, inbound lead flags |
| **Hands off to** | Rex | Support escalations, renewal alerts |
| **Hands off to** | Steve | Infrastructure tasks, build requests |
| **Hands off to** | Founders | Escalations, strategic decisions, external commitments |
| **Does NOT own** | Sales contacts and CRM records (Leo + CRM) |
| **Does NOT own** | Content production (Maya) |
| **Does NOT own** | Software development (Steve) |
| **Does NOT own** | Sales outreach (Leo) |

---

## Part 2 — Context & Data Layer

### 2a. What Iris Needs to Know

| What Iris needs to know | Source | How it reads it |
|---|---|---|
| Company strategy and goals | GBrain vault | Direct file: `internal/company/overview.md` |
| Each BL's strategy and current state | GBrain vault | Direct file: `internal/business-lines/[bl]/strategy.md` |
| Agent roster and health | GBrain vault | Direct file: `internal/agents/[agent].md` |
| Key decisions | GBrain vault | Direct file: `internal/decisions/YYYY-MM-DD-[topic].md` |
| Human 1's preferences and priorities | Hindsight | `[org]-human-1` bank recall |
| Human 2's preferences and priorities | Hindsight | `[org]-human-2` bank recall |
| Recent pipeline activity | Hindsight | `[org]-pipeline` bank recall (read only) |
| External company or person | GBrain MCP | `mcp_gbrain_get_page("external/entities/[type]/[slug]")` |

**GBrain content that must exist before Iris is fully useful:**

| Document | Slug | Status |
|---|---|---|
| Company overview | `internal/company/overview.md` | ✅ Exists |
| [bl-name] strategy | `internal/business-lines/[bl-name]/strategy.md` | ✅ Exists |
| [bl-name] ICP | `internal/business-lines/[bl-name]/icp.md` | ✅ Exists |
| Agent roster | `internal/agents/` | 📝 To fill |

---

## Part 3 — Capabilities

### 3a. Capabilities Overview

| # | Capability | What it means in plain English | Skills | Priority |
|---|---|---|---|---|
| C1 | Operations & Infrastructure Management | Primary triage point for all requests. Manages VMs, tools, Lark channels, internal task lists, agent cron jobs. Owns the company operating system. | `managing-tasks`, `reviewing-tasks`, `auditing-tasks`, `generating-task-briefing`, `planning-next-actions`, `managing-cron-jobs`, `generating-daily-ops-briefing` | 🔴 Must-have |
| C2 | Team Management | Maintains view of agent/human roster. Manages non-sales internal ops tasks in Lark with initiative tags. | `managing-tasks`, `lark-im`, `lark-base` | 🔴 Must-have |
| C3 | Contact Memory Health | Keeps memory healthy across all layers. Runs daily Lark extraction + nightly session ingest so nothing is ever lost. | `extracting-lark-to-gbrain`, `ingesting-sessions-to-hindsight`, `capturing-to-gbrain`, `checking-context-health`, `managing-team-knowledge` | 🔴 Must-have |
| C4 | Knowledge Distillation | Distils conversations into durable GBrain entries. Runs dream cycle. Syncs vault to GitHub. | `maintaining-gbrain`, `syncing-brain-memory`, `capturing-to-gbrain`, `extracting-lark-to-gbrain` | 🔴 Must-have |
| C5 | Agent Coordination | Reviews agent outputs. Distils findings to GBrain. Writes Result for Human. Surfaces blockers. Manages handoffs. | `capturing-to-gbrain`, `lark-im`, `lark-base`, `reviewing-tasks` | 🔴 Must-have |
| C6 | Financial Analysis | Answer financial questions, track runway, flag budget vs actuals. *(Requires financial data source — to be connected.)* | `[to-build]` | 🟡 Future |

---

### 3b. Skills

**Capability Skills**

| Skill | Capability | What it does |
|---|---|---|
| `checking-context-health` | C1, C3 | Daily automated audit: GBrain embed coverage, Hindsight banks, cron status, VM disk |
| `extracting-lark-to-gbrain` | C3, C4 | Pulls all bot-accessible Lark group chats → filters noise → extracts facts to GBrain |
| `ingesting-sessions-to-hindsight` | C3 | Extracts today's Hermes sessions → writes founder intel to dx-human-* and dx-global banks |
| `maintaining-gbrain` | C4 | Nightly dream cycle — consolidate, embed, clean GBrain |
| `syncing-brain-memory` | C4 | Push [org]-gbrain vault + Hermes memory files to GitHub |
| `managing-team-knowledge` | C3, C4 | Maintain entity pages, decisions, timelines in GBrain |
| `auditing-tasks` | C1 | Weekly Sunday task structure audit |
| `generating-task-briefing` | C1 | Daily morning task briefing for founders |
| `generating-daily-ops-briefing` | C1, C2 | Daily ops pulse to [Ops] channel — task health, agent status, infrastructure flags |
| `planning-next-actions` | C1 | Surface what needs attention today |
| `managing-cron-jobs` | C1 | Create, update, pause, resume Hermes cron jobs |

**General Skills**

| Skill | Purpose |
|---|---|
| `capturing-to-gbrain` | Write entities/facts to GBrain |
| `lark-im` | Send/receive Lark messages and notifications |
| `managing-skills` | Maintain and update skill library |
| `managing-tasks` | Task board CRUD |
| `reviewing-tasks` | Task board query and summary |
| `lark-base` | Lark Base operations |
| `github-core-repos` | Read/write [org]-gbrain and [org]-agent-package repos |

---

### 3c. Cron Jobs

| Job | Schedule (UTC) | Schedule (TWN) | Capability | Delivers to |
|---|---|---|---|---|
| Daily Lark → GBrain Extraction | 19:00 daily | 03:00 daily | C3, C4 | [Ops] — summary; silent if zero messages |
| GBrain Nightly Dream + Memory Sync | 20:00 daily | 04:00 daily | C4 | [System] Backend Report |
| [org]-gbrain Nightly Sync | 20:00 daily | 04:00 daily | C4 | Local only |
| Daily Session → Hindsight Ingest | 21:00 daily | 05:00 daily | C3 | Local only; silent if nothing to write |
| Daily Context Health Check | 00:00 daily | 08:00 daily | C1, C3 | [Ops] — alert only; silent if all green |
| Daily Ops Briefing | 01:00 daily | 09:00 daily | C1, C2 | [Ops] Internal Operations |

> **Timing chain:** Lark extraction (19:00) → GBrain dream (20:00) → Session ingest (21:00) → Health check (00:00) → Ops briefing (01:00) → Leo's crons start (01:00+). Every layer feeds the next.

---

### 3d. Delivery Channels

| Channel | ID | Purpose |
|---|---|---|
| `[Ops] Internal Operations` | `[ops-channel-id]` | Daily ops briefing, health alerts, extraction summaries |
| `[HQ] Biz & Strategy` | `[hq-biz-channel-id]` | Strategic intel, decision flags |
| `[HQ] Financial` | `[hq-fin-channel-id]` | Financial analysis (C6 — future) |
| `[System] Backend Report` | `[system-backend-id]` | Machine logs, raw cron output — not human-readable |
| `local` | — | Silent cron outputs (session ingest, vault sync) |
| GitHub `[org]/[org]-gbrain` | — | GBrain vault backup |

---

## Part 4 — Tools & Permissions

### 4a. Tools Required

| Tool / Skill | Purpose |
|---|---|
| `checking-context-health` | Daily system health audit |
| `extracting-lark-to-gbrain` | Daily Lark → GBrain extraction |
| `ingesting-sessions-to-hindsight` | Nightly session → Hindsight ingest |
| `maintaining-gbrain` | Nightly GBrain dream cycle |
| `syncing-brain-memory` | [org]-gbrain GitHub push |
| `capturing-to-gbrain` | Write distilled intel to GBrain |
| `managing-team-knowledge` | GBrain entity and decision maintenance |
| `generating-daily-ops-briefing` | Daily ops channel briefing |
| `managing-tasks` | Lark task board CRUD |
| `reviewing-tasks` | Task board query and summary |
| `auditing-tasks` | Weekly task audit |
| `generating-task-briefing` | Morning founder briefing |
| `planning-next-actions` | Daily priority surfacing |
| `managing-cron-jobs` | Cron job lifecycle management |
| `managing-skills` | Skill library maintenance |
| `lark-im` | Lark messaging (bot identity) |
| `lark-base` | Lark Base operations |
| `github-core-repos` | GitHub repo read/write |

---

### 4b. Credentials & Environment

> Iris runs on the Hermes default profile — credentials are in the root `.env`.
> lark-cli strict-mode must be set to `off` to use both user and bot identity.

| Service | Purpose | `.env` key |
|---|---|---|
| Anthropic | LLM inference | `ANTHROPIC_API_KEY` |
| Feishu Bot | Lark messaging | `FEISHU_APP_ID`, `FEISHU_APP_SECRET` |
| GBrain | Knowledge graph | `GBRAIN_*` |
| Hindsight | Episodic memory | `HINDSIGHT_BASE_URL` = `http://[hindsight-url]` |
| GitHub | [org]-gbrain backup | `GITHUB_TOKEN` |

---

### 4c. Build Mapping

| Spec Section | Build Artifact | Where it lives |
|---|---|---|
| 1b. Role & Goal | `SOUL.md` — identity, mandate, the number owned | `[hermes-home]/SOUL.md` |
| 1c. Team Positioning | `SOUL.md` — positioning, boundaries, handoffs | `[hermes-home]/SOUL.md` |
| 2a. Context needs | `SOUL.md` — Memory & Knowledge Sources block | `[hermes-home]/SOUL.md` |
| 2a. GBrain content | GBrain vault files | `[gbrain-vault-path]/internal/` |
| 3a. Capabilities | `SOUL.md` — Capabilities list | `[hermes-home]/SOUL.md` |
| 3b. Skills | Skills directory | `[hermes-home]/skills/` |
| 3c. Cron jobs | Hermes cron | Hermes default profile cron |
| 3d. Delivery channels | Cron `deliver` targets + channel IDs | Hermes cron config + SOUL.md |
| 4a. Tools | Skills in `SOUL.md` | `[hermes-home]/skills/` |
| 4b. Credentials | Root `.env` | `[hermes-home]/.env` |

---

## Spec Status

| Section | Status | Notes |
|---|---|---|
| Part 1 — Core Need & Positioning | ✅ Complete | |
| Part 2 — Context & Data Layer | ✅ Complete | |
| Part 3 — Capabilities | ✅ Complete | C6 Financial = future |
| Part 4 — Tools & Permissions | ✅ Complete | |
| GBrain content exists | ⚠️ Partial | `internal/agents/` still needs content |
| Hindsight banks created | ✅ Done | All 8 banks active |
| Credentials in `.env` | ✅ Done | Root Hermes profile |
| lark-cli strict-mode | ✅ Done | Set to `off` — bot + user identity both available |
| SOUL.md written | ✅ Done | Aligned to 5-capability structure |
| Skills built | ✅ Done | All capability skills operational |
| Skills verified | ✅ Done | Extraction, dream cycle, health check running |
| Cron jobs set up | ✅ Done | 6 active crons — full nightly pipeline |
