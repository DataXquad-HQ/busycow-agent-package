# GBrain & Hindsight: Dual-Track Memory Architecture

> This document defines the dual-track hybrid memory architecture for BusyCow agent teams.
> It covers what each store holds, how they work together, and the human review loop.

---

## Design Philosophy

A single memory system cannot do two fundamentally different jobs well:
- Recording raw, unbiased interaction history (dynamic, high-frequency, messy)
- Holding authoritative, human-verified facts about the world (static, low-frequency, clean)

Trying to use one system for both leads to **memory pollution** — agents auto-retain every noise, assumption, and temporary opinion from conversations, reinforce them as facts in subsequent sessions, and spiral into self-referential hallucination loops that become nearly impossible to correct.

The solution: two separate tracks with explicit roles, connected by a nightly distillation pipeline with mandatory human review.

---

## The Two Tracks

```
[Agent Interaction]
       │
       ├──► (write path) ──► session buffer ──► [session end] ──► bulk retain ──► [Hindsight — Hot Tier]
       │                                                                                    │
       │                                                                         (nightly dream cycle)
       │                                                                                    │
       │                                                                                    ▼
       └──► (read path) ◄── GBrain compiled truth ◄── [human PR merge] ◄── auto-formatted Markdown
```

---

## Track 1: Episodic Hot Tier (Hindsight)

**Component:** Hindsight  
**Role:** Raw, objective, chronological record of everything that happened

### What goes in
- Every agent interaction: what was said, what was agreed, what was blocked
- Timestamped, tagged with entity slugs (`company`, `opportunity`, `person`)
- Full session transcripts at bulk-write time

### Write strategy
**Disable** Hindsight's `auto_retain` and `auto_reflect`. Never let agents write to Hindsight in real-time mid-conversation — this is how memory pollution starts.

Instead:
1. Buffer the full session transcript in memory during the conversation
2. At `session:end` (or every 30 turns for long sessions), execute a single deterministic **bulk retain** to Hindsight
3. One write per session — clean, objective, no mid-conversation noise

### What agents do with it
Query before acting to get recent interaction history:
```
POST /v1/[org]/banks/[org]-pipeline/memories/recall
{"query": "[company or opportunity name] recent interactions", "top_k": 5}
```

### Bank types

| Bank | Who writes | What it stores |
|---|---|---|
| `[org]-pipeline` | All agents (bulk, session-end only) | Interaction records — per opportunity/partnership/company |
| `[org]-agent-[name]` | That agent only | Working memory within a session — scratch, reasoning, temp state |
| `[org]-human-[name]` | Iris only | Observed human communication patterns, preferences, priorities |

---

## Track 2: Semantic Cold Tier (GBrain)

**Component:** GBrain (local Markdown Git repo)  
**Role:** Human-verified compiled truth — authoritative facts about entities and their relationships

### What goes in
Only facts that have been reviewed and confirmed by a human. Nothing gets into GBrain unreviewed.

| Entity type | Slug prefix | What it represents |
|---|---|---|
| `company` | `companies/` | External organisations — prospects, partners, investors, competitors |
| `person` | `people/` | External individuals — contacts, decision-makers, introducers |
| `opportunity` | `opportunities/` | Active deals being pursued |
| `partnership` | `partnerships/` | Formal or in-progress partnerships |
| `decision` | `decisions/` | Key internal decisions with rationale |

### Relationship types

| Relationship | From → To | Meaning |
|---|---|---|
| `works_at` | person → company | This person works at this company |
| `involved_in` | person → opportunity or partnership | This person is a stakeholder in this deal |
| `made` | person → decision | This person was key to this decision |

### The human review loop (nightly)

1. **Dream cycle runs** — Iris reviews Hindsight pipeline observations from the past 24 hours
2. **High-confidence facts identified** — e.g. a new stakeholder discovered, a company's status confirmed, a decision reached
3. **Auto-formatted as Markdown** — Iris writes a `put_page` to GBrain with the compiled truth format
4. **Human reviews** — Hunter or Kevin checks what was written, corrects if needed
5. **Confirmed = committed** — fact becomes part of the cold tier, queried with full trust

### What agents do with it
Query before acting to get entity facts and relationships:
```
mcp_gbrain_get_page(slug="companies/[slug]")
mcp_gbrain_query("[company name] stakeholders")
mcp_gbrain_traverse_graph(slug="opportunities/[slug]", direction="in", link_type="involved_in")
```

---

## How Agents Load Context Before Acting

Strict injection order — cold facts first, hot episodic second:

```
1. GBrain compiled truth (cold — load first, always trusted)
   → mcp_gbrain_get_page("companies/[slug]")
   → mcp_gbrain_query("[entity] relationships")

2. Knowledge Base files (our own strategy — load by BL)
   → read: business-lines/[bl]/icp.md
   → read: business-lines/[bl]/strategy.md

3. Hindsight recent interactions (hot — load last, provides context)
   → POST /recall {"query": "[entity] recent interactions"}

4. Current conversation
```

This order ensures agents never let recent noisy episodic memory override authoritative cold facts. GBrain is the hard constraint; Hindsight is the contextual enrichment.

---

## The Nightly Distillation Pipeline

The pipeline that moves facts from hot to cold is owned by Iris and runs as a nightly cron job.

```
Hindsight pipeline bank
       │
       │  (Iris reviews observations at 20:00 UTC)
       ▼
High-confidence facts identified
       │
       │  (Iris formats as GBrain compiled truth Markdown)
       ▼
mcp_gbrain_put_page() or mcp_gbrain_extract_facts()
       │
       │  (human reviews in morning — correct or approve)
       ▼
Confirmed → stays in GBrain cold tier
Rejected → Iris marks as noise, does not re-extract
```

### What Iris looks for in Hindsight observations
- New external person or company encountered for the first time → create entity page
- New relationship discovered (person joined a company, new stakeholder on a deal) → add link
- Key decision reached → create decisions/ page
- Opportunity or partnership status change → update entity + timeline entry

### What Iris does NOT promote to GBrain
- Temporary states ("they seem interested today")
- Unverified assumptions ("I think they might have budget")
- Emotional signals ("they seemed hesitant")
- Anything that could change next week

These stay in Hindsight only.

---

## Why This Works

| Problem | Solution |
|---|---|
| Memory pollution (auto-retain noise) | Disabled. Agents never write mid-session. Bulk write at session end only. |
| Self-referential hallucination loops | GBrain compiled truth overrides Hindsight — hard constraint on cold facts |
| Unverified facts becoming canonical | Nothing enters GBrain without human review |
| Losing interaction history | Hindsight keeps full episodic record — nothing is deleted, just not promoted |
| Agents not knowing what to trust | Injection order is explicit: GBrain first = always trusted, Hindsight = context only |
