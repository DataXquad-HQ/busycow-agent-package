# GBrain and Hindsight Architecture

> Audience: humans designing the Contextual Layer.
> Purpose: explain how GBrain and Hindsight work together in the current Hermes AI colleague architecture.

This document replaces the older dual-track model that assumed a single pipeline bank, Iris-only distillation, or a GBrain repo as the only truth layer. The current model separates canonical knowledge, evidence, experiential memory, structured operational state, and workspace context.

---

## 1. Core Distinction

| System | Owns | Does not own |
|---|---|---|
| GBrain canonical | approved, durable, reviewable company truth | raw memory, temporary state, private scratch |
| GBrain evidence | source material and traceable support for claims | final policy or mutable workflow state |
| Hindsight | experience, corrections, recent observations, learned patterns | canonical truth, approval state, CRM/task state |

GBrain tells the agent what the company has accepted or what evidence exists.
Hindsight tells the agent what happened and what may be worth remembering.
Structured systems tell the agent what is currently operationally true.
Workspace tells the agent what it is currently working on.

---

## 2. Recommended GBrain Source Topology

Use sources as access-control and write-authority boundaries.

Recommended V1 sources:

```text
shared
customers
partners
product-eng
internal
```

Suggested folder shape:

```text
shared/
  business-lines/
  policies/
  concepts/
  people/
  companies/
customers/
  customer-pages/
  companies/
  people/
  meetings/
  product-feedback/
  objection-patterns/
  sources/
partners/
  partner-pages/
  companies/
  people/
  meetings/
  partner-feedback/
  sources/
product-eng/
  projects/
  tech-decisions/
  meetings/
  postmortems/
  sources/
internal/
  strategy/
  finance/
  legal/
  people-ops/
```

Rules:

- each role-owning AI colleague should usually have one home write source
- cross-source canonical writes should go through review or publisher flow
- subject pages should be separate from raw evidence archives
- evidence should remain traceable to source material

---

## 3. GBrain Page Types

Recommended V1 schema pack:

```text
company-colleague-v1
```

Recommended page types:

- `business_line`
- `icp`
- `messaging`
- `sales_playbook`
- `cs_playbook`
- `partner_playbook`
- `product_principle`
- `tech_decision`
- `customer_account`
- `partner_account`
- `feedback_signal`
- `objection_pattern`
- `policy`
- `decision_record`
- `evidence_note`

---

## 4. GBrain Canonical Governance

Canonical pages should include metadata such as:

```yaml
---
type: {{page_type}}
business_line: {{business_line}}
knowledge_state: canonical
approval_status: approved
owner: {{owner}}
reviewers: [{{reviewer}}]
effective_date: {{YYYY-MM-DD}}
last_reviewed_at: {{YYYY-MM-DD}}
source_refs:
  - {{source_ref}}
confidence: high
---
```

Canonical writes should be reviewed. An agent may draft or propose canonical updates, but production deployments should not allow unreviewed autonomous canonical publishing unless an explicit authority policy permits it.

---

## 5. GBrain Evidence Governance

Evidence pages should include metadata such as:

```yaml
---
type: evidence_note
knowledge_state: evidence
source_system: {{source_system}}
source_date: {{YYYY-MM-DD}}
related_subjects:
  - {{gbrain_subject_path}}
owner: {{owner}}
retention: {{policy}}
---
```

Evidence can support or challenge canonical knowledge. If evidence conflicts with canonical truth, the agent should raise a review item instead of silently overriding canonical behavior.

---

## 6. Hindsight Bank Model

Use a small number of banks and rely on metadata/tags before creating many bank boundaries.

Recommended V1 model:

| Bank type | Purpose | Default write mode |
|---|---|---|
| personal agent bank | profile-local experience, corrections, recurring patterns | auto-retain personal |
| shared/domain bank | cross-agent patterns, customer voice, product feedback, campaign learning | governed write or propose |
| human/context bank, if used | human communication preferences or relationship context | explicit governance and privacy rules |

Recommended naming pattern:

```text
{{org_slug}}/agents/{{profile_name}}
{{org_slug}}/shared/{{domain}}
{{org_slug}}/humans/{{person_slug}}
```

Do not create a new shared bank for every business slice. Prefer tags first.

---

## 7. Hindsight Memory Types

Recommended V1 memory object types:

1. `interaction_memory`
2. `customer_signal`
3. `team_decision`
4. `correction`
5. `experience_learning`
6. `research_note`
7. `product_opportunity_signal`
8. `campaign_learning`
9. `agent_behavior_note`
10. `promotion_candidate`

Recommended metadata:

```yaml
memory_type: {{memory_type}}
business_line: {{business_line}}
source: {{source}}
source_date: {{YYYY-MM-DD}}
created_by: {{agent_or_human}}
confidence: low | medium | high
status: active | stale | promoted | invalidated
visibility: personal | shared | restricted
related_gbrain_docs:
  - {{path_or_slug}}
related_structured_records:
  - {{record_ref}}
tags:
  - biz:{{business_line}}
  - domain:{{domain}}
promotion_candidate: true | false
ttl: {{optional_expiry}}
```

---

## 8. Read Routing

| Question | First source |
|---|---|
| What is officially true? | GBrain canonical |
| Why do we believe this? | GBrain evidence |
| What happened recently? | Hindsight, then evidence if a source trail is needed |
| What is the current owner/status/deadline/approval? | structured system of record |
| What is the agent currently drafting or reviewing? | agent workspace |

---

## 9. Write Routing

| New information type | Destination |
|---|---|
| approved durable knowledge | GBrain canonical |
| raw meeting/source/import evidence | GBrain evidence |
| recent experience or correction | Hindsight personal bank |
| cross-agent learned pattern | governed shared/domain Hindsight bank |
| task/deal/approval/status update | structured system of record |
| draft or review queue item | agent workspace |

---

## 10. Promotion Workflow

Default workflow:

```text
Raw Signal
  -> Memory Capture / Evidence Capture
  -> Shared Insight Candidate
  -> Governed Review
  -> Canonical Knowledge
```

When a memory becomes canonical:

- link the Hindsight memory to the GBrain document
- mark the memory as promoted
- preserve source references
- keep operational state in the structured system if the claim is stateful

---

## 11. Anti-Patterns

Avoid:

- treating Hindsight as the canonical source of truth
- storing approval state only in memory
- using GBrain as an agent scratchpad
- dumping all transcripts into canonical pages
- letting workspace notes become unreviewed policy
- creating many banks when tags would work
- allowing autonomous canonical publishing without authority rules