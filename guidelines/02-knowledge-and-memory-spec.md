# Knowledge & Memory Guideline

> This document defines the full memory architecture for a BusyCow agent team.
> Read this alongside `03-gbrain-and-hindsight-spec.md` for the detailed dual-track design.

---

## The Four Stores

| Store | What it holds | Who writes | Read by |
|---|---|---|---|
| **GBrain repo** | Single source of truth — BL knowledge + external entities + decisions | Humans (direct) + Iris (nightly distillation) | All agents (direct file read + GBrain query) |
| **Hindsight** | Episodic memory — what happened in every interaction | Agents (bulk, session-end only) | All agents |
| **Hermes memory** | Agent/Iris session constants — env facts, preferences | Iris | Iris only |

These three stores do not overlap. Each answers a different question.

Structured data stores (CRM, databases, etc.) are out of scope for this spec — add them as needed per agent. The key principle is that structured pipeline objects live separately from memory.

---

## Architecture: Dual-Track Information Flow

```
External World + Conversations
         │
         ▼
    Agent / Iris receives or produces something
         │
         ▼
[HOT TIER]
Hindsight pipeline bank
— bulk write at session end
— full interaction record
— auto entity mention graph
         │
    (nightly)
    Iris distillation
         │
         ▼
[COLD TIER]
GBrain repo (Git + local)
— compiled truth
— human-reviewed before merge
— business-line knowledge
— external entity graph
         │
         ▼
Agent reads context →
executes task →
writes back to Hindsight
```

---

## GBrain Repo: Folder Structure

The GBrain repo is the single source of truth. It lives on disk, is synced to GitHub, and is indexed by GBrain automatically.

```
[org]-gbrain/
│
├── internal/                        ← Everything about us
│   ├── company/                     ← Company identity, team, portfolio
│   ├── business-lines/[bl-name]/    ← Per-BL: strategy, ICP, product, GTM, market
│   ├── agents/                      ← Agent role specs
│   ├── systems/                     ← Tool usage guides
│   └── decisions/                   ← Key decisions with rationale
│
├── external/                        ← Everything about the world
│   ├── entities/
│   │   ├── companies/               ← External orgs (Iris-maintained)
│   │   ├── people/                  ← External contacts (Iris-maintained)
│   │   ├── opportunities/           ← Active deals (Iris-maintained)
│   │   └── partnerships/            ← Active partnerships (Iris-maintained)
│   └── intel/
│       └── market/                  ← Market intelligence, cross-BL
│
└── hermes-memory/                   ← Iris session memory (auto-managed)
```

### Two types of content, one repo

| Folders | Written by | How it enters |
|---|---|---|
| `internal/company/` `internal/business-lines/` `internal/decisions/` | Humans | Direct commit or PR |
| `external/entities/companies/` `external/entities/people/` `external/entities/opportunities/` `external/entities/partnerships/` | Iris | Nightly distillation → PR → human merge |

**Critical:** Never merge Iris-generated PRs from GitHub web UI. Always pull locally and let GBrain's custom merge driver resolve conflicts, then push.

---

## How Agents Load Context Before Acting

Strict injection order — cold facts first, hot episodic second:

```
1. GBrain cold tier (always trusted — load first)
   → Direct file read: internal/business-lines/[bl]/icp.md, strategy.md
   → Direct file read: internal/company/overview.md
   → mcp_gbrain_get_page("external/entities/companies/[slug]") for external entities
   → mcp_gbrain_query("[entity] relationships") for graph traversal

2. Hindsight hot tier (context enrichment — load second)
   → POST /recall {"query": "[entity] recent interactions", "bank": "[org]-pipeline"}
```

### Rule of Thumb

| Question | Go to |
|---|---|
| What is our ICP / strategy for this BL? | GBrain repo — direct file read |
| Who is this external company / person? | GBrain — `mcp_gbrain_get_page` |
| Who is connected to this deal? | GBrain — `mcp_gbrain_traverse_graph` |
| What happened last time with this company? | Hindsight `[org]-pipeline` |
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
| New external person or company first encountered | `put_page external/entities/companies/` or `external/entities/people/` |
| New relationship discovered | `add_link works_at / involved_in / made` |
| Opportunity or partnership opened | `put_page external/entities/opportunities/` or `external/entities/partnerships/` |
| Key decision reached | `put_page internal/decisions/YYYY-MM-DD-topic` |
| BL strategy or ICP change confirmed | Update `internal/business-lines/[bl]/` files |

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
  slug="internal/business-lines/[bl-name]/icp",
  date="YYYY-MM-DD",
  summary="Updated ICP — removed SME segment",
  detail="ACV too low to justify BD effort. Refocusing on enterprise only."
)
```

---

## Setup Checklist

**1. GBrain repo**

The GBrain repo IS the knowledge base. Register it once as a GBrain source.

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
