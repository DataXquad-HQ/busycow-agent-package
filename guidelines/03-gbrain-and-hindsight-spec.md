# GBrain & Hindsight: Dual-Track Memory Architecture

> This document defines the dual-track hybrid memory architecture for BusyCow agent teams.
> It covers design philosophy, what each store holds, implementation details, and the human review loop.

---

## Why This Architecture Exists

BusyCow agent teams are built for **multi-agent, multi-human collaboration**. This is not a single-user assistant. It is a team of agents serving multiple humans, each with their own context, working toward shared goals across multiple business lines.

This creates a fundamental tension:

- **Each human has private memory** — their communication style, priorities, what they've shared in confidence
- **Some memory is shared** — what happened in a deal, what was agreed, who said what
- **Some facts belong to everyone** — what our ICP is, who a company is, what was decided

A single memory system cannot handle all three correctly. Using one store for all of them leads to:
- Private context leaking between humans
- Noise from one agent's session polluting another's decisions
- Unverified assumptions getting treated as canonical facts
- Agents in self-referential hallucination loops, impossible to correct

The dual-track architecture solves this by giving each type of memory its own store with explicit ownership rules.

---

## The Two Tracks

```
[Any Agent or Human interaction]
         │
         ├──► (write) ──► session buffer ──► [session end] ──► bulk retain
         │                                                           │
         │                                                   [Hindsight — Hot Tier]
         │                                                    per-bank isolation:
         │                                                    pipeline / agent / human
         │                                                           │
         │                                              (nightly — Iris distillation)
         │                                                           │
         │                                                           ▼
         └──► (read) ◄── [GBrain — Cold Tier] ◄── [human PR review + merge]
                          compiled truth:
                          entities / relationships /
                          BL knowledge / decisions
```

---

## Track 1: Episodic Hot Tier — Hindsight

**Role:** Raw, timestamped, objective record of everything that happened. Per-participant isolation built in.

### Bank Design

Three bank types. The design reflects the multi-human, multi-agent nature of the team.

| Bank | ID pattern | Who writes | Who reads | What it stores |
|---|---|---|---|---|
| **Pipeline** | `[org]-pipeline` | All agents (bulk, session-end) | All agents | Shared interaction history — every engagement with an opportunity, partnership, or company. Tagged with `business_line` and entity slugs. |
| **Agent working memory** | `[org]-agent-[name]` | That agent only | That agent only | Scratch notes, reasoning, temp state within a session. Not shared. Cleared or not promoted. |
| **Human profile** | `[org]-human-[name]` | Iris only | All agents (read-only) | Observed communication patterns, priorities, preferences for each human. One bank per human. |

### Why separate banks per human

Each human on the team has different communication preferences, decision-making styles, and context. An agent working with Hunter should not load Kevin's communication patterns, and vice versa. Bank-level isolation makes this clean — agents load the right profile for the human they're currently serving.

### Why the pipeline bank is shared

Every agent touching a deal needs the same interaction history. Leo logs a call with a prospect; if Iris later needs to brief Hunter on that deal, she reads the same pipeline bank. Shared history, isolated profiles.

### Write rules (critical)

**`auto_retain` and `auto_reflect` are disabled.** No agent writes to Hindsight in real-time mid-conversation.

Why: Real-time auto-retain captures noise — temporary assumptions, emotional signals, unverified opinions. These get reinforced in subsequent sessions and become impossible to correct. This is memory pollution.

Instead:
1. Buffer the full session transcript in memory during the conversation
2. At `session:end` (or every 30 turns for long sessions), execute a **single deterministic bulk retain**
3. One write per session — objective, complete, no mid-conversation noise

### What goes into each pipeline record

```json
{
  "business_line": "[bl-name]",
  "opportunity_slug": "external/entities/opportunities/[slug]",
  "company_slug": "external/entities/companies/[slug]",
  "people_involved": ["external/entities/people/[slug]"],
  "agent": "[agent-name]",
  "human": "[human-name]",
  "date": "YYYY-MM-DD",
  "channel": "email | call | meeting | message",
  "summary": "What happened",
  "outcome": "What was agreed or decided",
  "next_action": "What happens next",
  "blockers": "Anything blocking progress"
}
```

### Querying Hindsight

```
# Shared deal history
POST /v1/[org]/banks/[org]-pipeline/memories/recall
{"query": "[company or opportunity name] recent interactions", "top_k": 5}

# Human-specific context
POST /v1/[org]/banks/[org]-human-[name]/memories/recall
{"query": "communication style priorities", "top_k": 3}
```

---

## Track 2: Semantic Cold Tier — GBrain

**Role:** Human-verified compiled truth. The shared fact layer for the entire team — agents, humans, and Iris all trust this equally.

### What GBrain holds

GBrain is the single source of truth for:
- Who external entities are and how they relate to each other (entity graph)
- What our business lines are, their strategy, ICP, GTM (BL knowledge)
- What key decisions were made and why (decision log)

Nothing enters GBrain unreviewed. Everything here has been confirmed by a human.

### Entity types

| Type | Slug prefix | What it represents |
|---|---|---|
| `company` | `external/entities/companies/` | External organisations — prospects, partners, investors, competitors |
| `person` | `external/entities/people/` | External individuals — contacts, decision-makers, introducers |
| `opportunity` | `external/entities/opportunities/` | Active deals being pursued |
| `partnership` | `external/entities/partnerships/` | Formal or in-progress partnerships |
| `decision` | `internal/decisions/` | Key internal decisions with rationale |

### Relationship types

| Relationship | From → To | Meaning |
|---|---|---|
| `works_at` | person → company | This person works at this company |
| `involved_in` | person → opportunity or partnership | This person is a stakeholder in this deal |
| `made` | person → decision | This person was key to this decision |

### The human review loop (nightly)

1. Iris reviews Hindsight pipeline observations from the past 24 hours
2. High-confidence facts identified (new entity, new relationship, confirmed decision)
3. Iris formats as GBrain compiled truth Markdown and writes via `put_page` — new external facts to `external/entities/`, decisions to `internal/decisions/`
4. Human reviews on GitHub in the morning — correct or approve
5. Confirmed → stays in GBrain. Rejected → Iris marks as noise, does not re-extract.

**Important:** Never merge Iris-generated PRs from GitHub web UI. Always pull locally first — GBrain's custom merge driver resolves conflicts correctly. GitHub's server-side merge does not run custom drivers.

### What Iris does NOT promote to GBrain

- Temporary states ("they seem interested today")
- Unverified assumptions ("I think they might have budget")
- Emotional signals ("they seemed hesitant")
- Anything agent-internal or session-specific

These stay in Hindsight only.

---

## How Agents Load Context Before Acting

Strict injection order. Cold facts first, hot episodic second.

```
1. GBrain cold tier (hard constraint — always trusted)
   → Direct file read: internal/business-lines/[bl]/icp.md + strategy.md
   → mcp_gbrain_get_page("external/entities/companies/[slug]")
   → mcp_gbrain_traverse_graph("external/entities/opportunities/[slug]", link_type="involved_in")

2. Hindsight pipeline (shared deal history — context)
   → POST /recall {"query": "[entity] recent interactions", "bank": "[org]-pipeline"}

3. Hindsight human profile (if serving a specific human)
   → POST /recall {"query": "priorities communication style", "bank": "[org]-human-[name]"}

4. Current conversation
```

GBrain is the hard constraint. Hindsight provides context. Agents never let recent episodic memory override authoritative cold facts.

---

## Multi-Agent, Multi-Human Collaboration Model

This is the core purpose of the architecture.

```
Human: Hunter ──► [org]-human-hunter bank  ┐
Human: Kevin  ──► [org]-human-kevin bank   ├── Iris reads, agents load on demand
                                           ┘

Agent: Leo    ──► [org]-agent-leo bank     ┐
Agent: Maya   ──► [org]-agent-maya bank    ├── Private per-agent, not shared
Agent: Rex    ──► [org]-agent-rex bank     ┘

All agents ──► [org]-pipeline bank         ← Shared deal/interaction history

Iris (nightly) ──► GBrain                 ← Shared fact layer, human-reviewed
                     │
                 internal/business-lines/  ← Same truth for all agents
                 external/entities/        ← Same entities for all agents
                 internal/decisions/       ← Same decisions for all agents
```

**The key insight:** Agents share facts (GBrain) and deal history (pipeline bank), but human context is always isolated. No agent ever loads another human's profile unless explicitly serving that human. No agent's scratch memory bleeds into another session.

---

## Why This Works: Problem → Solution Map

| Problem | Solution |
|---|---|
| Memory pollution from noise | `auto_retain` disabled. Bulk write at session end only. |
| Self-referential hallucination loops | GBrain compiled truth is hard constraint — always loaded first |
| Private human context leaking | Per-human banks, read-only by agents, write only by Iris |
| Agent scratch memory polluting shared history | `[org]-agent-[name]` banks are private, never shared |
| Unverified facts becoming canonical | Nothing enters GBrain without human review |
| Multiple agents disagreeing on facts | One shared GBrain cold tier — same truth for all agents |
| Losing interaction history | Hindsight keeps full episodic record — nothing deleted, just not promoted |
