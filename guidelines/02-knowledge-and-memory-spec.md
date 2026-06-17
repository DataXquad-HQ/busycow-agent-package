# Knowledge & Memory Guideline

> This document defines the full memory architecture for a BusyCow agent team.
> Read this alongside `03-gbrain-and-hindsight-spec.md` for the detailed dual-track design.

---

## The Four Stores

| Store | What it holds | Who writes | Read by |
|---|---|---|---|
| **GBrain repo** | Single source of truth — BL knowledge + external entities + decisions | Humans (direct) + Iris (nightly distillation) | All agents (direct file read + GBrain query) |
| **Hindsight** | Episodic memory — what happened in every interaction | Agents (bulk, session-end only) | All agents |
| **CRM** | Pipeline state — deal stage, tasks, structured objects | Leo | Leo |
| **Hermes memory** | Agent/Iris session constants — env facts, preferences | Iris | Iris only |

These four stores do not overlap. Each answers a different question.

---

## Architecture: Dual-Track Information Flow

```
External World + Conversations
         │
         ▼
    Agent / Iris receives or produces something
         │
    ┌────┴─────────────────────────────────┐
    ▼                                       ▼
[HOT TIER]                            [STRUCTURED]
Hindsight pipeline bank               Twenty CRM
— bulk write at session end           — deal stage, tasks
— full interaction record             — updated per stage change
— auto entity mention graph               │
         │                                │
    (nightly)                             │
    Iris distillation                     │
         │                                │
         ▼                                │
[COLD TIER]                               │
GBrain repo (Git + local)                 │
— compiled truth                          │
— human-reviewed before merge             │
— business-line knowledge                 │
— external entity graph                   │
         │                                │
         └──────────────┬─────────────────┘
                        ▼
              Agent reads context →
              executes task →
              writes back to Hindsight + CRM
```

---

## GBrain Repo: Folder Structure

The GBrain repo is the single source of truth. It lives on disk, is synced to GitHub, and is indexed by GBrain automatically.

```
[org]-gbrain/
│
├── business-lines/              ← BL knowledge (human-written, cold)
│   └── [bl-name]/
│       ├── overview.md
│       ├── strategy.md
│       ├── icp.md
│       ├── product.md
│       ├── gtm.md
│       └── market.md
│
├── company/                     ← Company-layer knowledge (human-written, cold)
│   ├── overview.md
│   ├── team.md
│   ├── portfolio.md
│   └── market/                  ← Cross-BL market intel
│
├── companies/                   ← External org entities (Iris-written, reviewed)
├── people/                      ← External contact entities (Iris-written, reviewed)
├── opportunities/               ← Active deals (Iris-written, reviewed)
├── partnerships/                ← Active partnerships (Iris-written, reviewed)
├── decisions/                   ← Key decisions (human + Iris, reviewed)
│
├── agents/                      ← Agent role specs
├── systems/                     ← Tool usage guides
└── hermes-memory/               ← Iris session memory (auto-managed by Hermes)
```

### Two types of content, one repo

| Folders | Written by | How it enters |
|---|---|---|
| `business-lines/` `company/` `decisions/` | Humans | Direct commit or PR |
| `companies/` `people/` `opportunities/` `partnerships/` | Iris | Nightly distillation → PR → human merge |

**Critical:** Never merge Iris-generated PRs from GitHub web UI. Always pull locally and let GBrain's custom merge driver resolve conflicts, then push.

---

## How Agents Load Context Before Acting

Strict injection order — cold facts first, hot episodic second:

```
1. GBrain cold tier (always trusted — load first)
   → Direct file read: business-lines/[bl]/icp.md, strategy.md
   → Direct file read: company/overview.md
   → mcp_gbrain_get_page("companies/[slug]") for external entities
   → mcp_gbrain_query("[entity] relationships") for graph traversal

2. Hindsight hot tier (context enrichment — load second)
   → POST /recall {"query": "[entity] recent interactions", "bank": "[org]-pipeline"}

3. CRM (pipeline state — load when needed)
   → twenty-crm skill for current opportunity stage
```

### Rule of Thumb

| Question | Go to |
|---|---|
| What is our ICP / strategy for this BL? | GBrain repo — direct file read |
| Who is this external company / person? | GBrain — `mcp_gbrain_get_page` |
| Who is connected to this deal? | GBrain — `mcp_gbrain_traverse_graph` |
| What happened last time with this company? | Hindsight `[org]-pipeline` |
| What stage is this deal at? | Twenty CRM |
| What are this person's communication patterns? | Hindsight `[org]-human-[name]` |

---

## Hindsight Banks

Three types. No more.

| Bank | Access | What it stores |
|---|---|---|
| `[org]-pipeline` | All agents (bulk write, session-end only) | Interaction records — per deal, company, or partnership. Tag with `business_line` and entity slugs. |
| `[org]-agent-[name]` | That agent only | Working memory within a session — scratch notes, reasoning, temp state |
| `[org]-human-[name]` | Read (agents), write (Iris only) | Human communication patterns, priorities, preferences — observed over time |

**Write rule:** `auto_retain` and `auto_reflect` are disabled. Agents never write to Hindsight mid-conversation. Only bulk write at session end.

---

## Nightly Distillation (Iris → GBrain)

Every night, Iris reviews Hindsight pipeline observations and promotes high-confidence facts to GBrain:

| What Iris looks for | Action |
|---|---|
| New external person or company first encountered | `put_page companies/` or `people/` |
| New relationship discovered | `add_link works_at / involved_in / made` |
| Opportunity or partnership opened | `put_page opportunities/` or `partnerships/` |
| Key decision reached | `put_page decisions/YYYY-MM-DD-topic` |
| BL strategy or ICP change confirmed | Update `business-lines/[bl]/` files |

What Iris does NOT promote:
- Temporary states, assumptions, emotional signals
- Anything unverified or likely to change next week

---

## Document Versioning

Every GBrain repo document must include a Changelog section:

```markdown
**Last Updated:** YYYY-MM-DD
**Version:** N

## Changelog
| Date | Change | Reason |
|---|---|---|
| YYYY-MM-DD | | |
```

For significant changes, also add a GBrain timeline entry:
```
mcp_gbrain_add_timeline_entry(
  slug="business-lines/[bl-name]/icp",
  date="YYYY-MM-DD",
  summary="Updated ICP — removed SME segment",
  detail="ACV too low to justify BD effort. Refocusing on enterprise only."
)
```

---

## Setup Checklist

**1. GBrain repo**
```bash
# Register as GBrain source
gbrain sources add --id [org]-gbrain --path /path/to/gbrain-repo --federated true
gbrain sync --repo /path/to/gbrain-repo

# Push to GitHub (private repo) for human review
git remote add origin git@github.com:[org]/[org]-gbrain.git
git push origin master
```

**2. Hindsight banks**
```
POST /v1/default/banks {"id": "[org]-pipeline", "name": "Pipeline Memory"}
POST /v1/default/banks {"id": "[org]-agent-[name]", "name": "[Agent] Working Memory"}
POST /v1/default/banks {"id": "[org]-human-[founder]", "name": "[Founder] Profile"}
```

**3. Nightly cron jobs**
- GBrain dream cycle (built-in) — auto-runs nightly
- Iris distillation → GBrain PR — schedule via Hermes cron
