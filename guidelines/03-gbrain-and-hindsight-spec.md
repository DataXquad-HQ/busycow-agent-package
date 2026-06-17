# GBrain & Hindsight Guideline

> This document defines how GBrain and Hindsight are used, what each stores, and how they work together.
>
> Iris owns both stores. Agents read; Iris writes.

---

## The Core Distinction

| Store | What it holds | Question it answers |
|---|---|---|
| **GBrain** | Static facts — who exists, what they are, how they're connected | "Who is this person? What are they connected to?" |
| **Hindsight** | Dynamic memory — what happened, what was said, what was decided in action | "What did we discuss last time? What did they say about budget?" |
| **CRM** | Pipeline state — structured deal objects, stages, tasks | "What stage is this deal at? What's the next action?" |
| **Knowledge Base** | Our own knowledge — strategy, ICP, product, market | "What is our GTM strategy for this BL?" |

These four stores do not overlap. Each answers a different question.

---

## GBrain: Entity Types

Five entity types. No more.

| Type | Slug prefix | What it represents |
|---|---|---|
| `company` | `companies/` | Any external organisation — prospect, partner, investor, competitor |
| `person` | `people/` | Any external individual — contact, decision-maker, introducer |
| `opportunity` | `opportunities/` | A potential deal or sale being pursued |
| `partnership` | `partnerships/` | A formal or in-progress partnership relationship |
| `decision` | `decisions/` | A key decision made internally, with rationale |

**Not in GBrain:**
- `agent` — agents are configured in SOUL.md, not stored in GBrain
- Engagements / interactions — these are dynamic; store in Hindsight pipeline bank

---

## GBrain: Relationship Types

Three relationship types that matter.

| Relationship | From | To | Meaning |
|---|---|---|---|
| `works_at` | `person` | `company` | This person works at this company |
| `involved_in` | `person` | `opportunity` or `partnership` | This person is a stakeholder in this deal/partnership |
| `made` | `person` | `decision` | This person made or was key to this decision |

### Why these three

- **`works_at`** — lets agents resolve "who do we know at Company X" without querying CRM
- **`involved_in`** — connects people to active deals; agents can traverse "who are the stakeholders in Opportunity Y"
- **`made`** — connects people to decisions; useful for understanding history and accountability

### Adding a relationship

```
mcp_gbrain_add_link(
  from="people/[person-slug]",
  to="companies/[company-slug]",
  link_type="works_at"
)
```

---

## GBrain: What Iris Writes (and When)

| Trigger | Action |
|---|---|
| New external person mentioned in conversation | `put_page people/[slug]` + `add_link works_at` |
| New external company mentioned | `put_page companies/[slug]` |
| New opportunity opened | `put_page opportunities/[slug]` + `add_link involved_in` for each stakeholder |
| New partnership initiated | `put_page partnerships/[slug]` + `add_link involved_in` |
| Key decision reached | `put_page decisions/YYYY-MM-DD-[topic]` + `add_link made` |
| Relationship discovered (e.g. intro, referral) | `add_link` between relevant entities |

**Rule:** If it's a fact about who someone is or how entities are connected → GBrain. If it's about what happened in an interaction → Hindsight.

---

## Hindsight: Bank Design

Three bank types. No more.

| Bank ID | Access | What it stores |
|---|---|---|
| `[org]-pipeline` | Read + write (all agents) | Every engagement with an opportunity or partnership — what was said, what was agreed, blockers, next steps. Tag each record with the relevant entity slugs. |
| `[org]-agent-[name]` | Read + write (that agent only) | Agent's working memory within a session — scratch notes, reasoning, temporary state |
| `[org]-human-[name]` | Read (agents), write (Iris only) | A person's communication patterns, priorities, preferences — observed over time |

### What goes in pipeline bank (per record)

```json
{
  "business_line": "[bl-name]",
  "opportunity_slug": "opportunities/[slug]",
  "company_slug": "companies/[slug]",
  "people_involved": ["people/[slug]"],
  "date": "YYYY-MM-DD",
  "channel": "email | call | meeting | message",
  "summary": "What happened",
  "outcome": "What was agreed or decided",
  "next_action": "What happens next",
  "blockers": "Anything blocking progress"
}
```

---

## How GBrain and Hindsight Work Together

The pattern for every agent action involving an external entity:

```
1. BEFORE acting
   → GBrain: who is this person/company? what are they connected to?
   → Hindsight pipeline: what happened last time with this opportunity?
   → KB: what is our strategy/ICP for this BL?

2. AFTER acting
   → Hindsight pipeline: log what happened (write)
   → GBrain: update entity or add relationship if something new was learned (write via Iris)
   → CRM: update opportunity stage if it changed (write)
```

### Example: Leo preparing for an outreach

```
# Step 1 — Load context
mcp_gbrain_get_page("companies/target-co")        # Who is this company?
mcp_gbrain_query("people at target-co")           # Who do we know there?
POST /recall {"query": "target-co last interaction", "bank": "dx-pipeline"}  # What happened last time?
read KB: business-lines/geokernel/icp.md          # Does this fit our ICP?

# Step 2 — Act (send outreach)

# Step 3 — Log
POST /memories {"bank": "dx-pipeline", ...}       # Log what was sent and why
mcp_gbrain_add_link(person → opportunity)         # If a new stakeholder was identified
```

---

## Setup: Creating Hindsight Banks

```
POST /v1/default/banks
{"id": "[org]-pipeline", "name": "Pipeline Memory"}

POST /v1/default/banks
{"id": "[org]-agent-[name]", "name": "[Agent] Working Memory"}

POST /v1/default/banks
{"id": "[org]-human-[founder-name]", "name": "[Founder] Profile"}
```

## Setup: GBrain Entity Page Format

Every entity page follows this frontmatter pattern:

```markdown
---
title: [Entity Name]
type: company | person | opportunity | partnership | decision
---

[Content]
```

Use `mcp_gbrain_add_timeline_entry` to log milestones on any entity (e.g. opportunity stage changes, partnership signed date).
