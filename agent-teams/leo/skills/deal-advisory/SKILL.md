---
name: deal-advisory
description: >
  Use when an opportunity is stalled or stuck. Fetches full opportunity history from Twenty CRM,
  diagnoses the bottleneck, and recommends recovery actions. Human-triggered,
  advisory only — Leo diagnoses and proposes, human decides.
triggers:
  - "opportunity stalled"
  - "opportunity stuck"
  - "opportunity went quiet"
  - "opportunity analysis"
  - "should I follow up"
version: "3.1"
author: Leo (BD Director Agent)
---

# Opportunity Advisory

## Purpose

Systematic diagnosis of a stalled opportunity. Fetch the full interaction history from Twenty CRM, identify the stall category, and recommend next steps.

Advisory only — Leo proposes, human decides.

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost)
**GraphQL endpoint:** `http://localhost:3001/graphql`

---

## When to Use

- Opportunity has been quiet for 7+ days with no forward movement
- Client said "we'll get back to you" but went silent
- You received negative feedback and want to assess recovery options
- You need to decide: is this worth salvaging?

**Don't use for:**
- Opportunities actively progressing (use `deal-progressing` instead)
- General pipeline review (use `reviewing-sales-pipeline` instead)

---

## Workflow

### Step 1: Fetch Opportunity Intelligence

```graphql
query GetOpportunityAdvisory($id: ID!) {
  opportunity(id: $id) {
    id name stage
    amount { amountMicros currencyCode }
    closeDate
    currentStatusSummary nextActionSummary
    healthCheck priority lastUpdateDate
    primaryContact
    company {
      id name companyOverview enrichmentOverview country
    }
    pointOfContact {
      id name { firstName lastName } jobTitle decisionRole
    }
    engagements(orderBy: { engagementDate: DescNullsLast }) {
      edges {
        node {
          engagementDate engagementType engagementStatus
          outcome nextAction
          engagementNote { json }
          clientAttendees { edges { node { name { firstName lastName } jobTitle } } }
        }
      }
    }
    taskOpportunities(filter: { status: { neq: "DONE" } }) {
      edges { node { id title { text } status dueAt } }
    }
  }
}
```

---

### Step 2: Diagnose the Stall Category

Four categories:

**Information Gap** — last engagement was a pitch/demo with no clear next step; you don't know where they stand.
→ Action: Low-pressure check-in to establish status.

**Timing Mismatch** — client said "get back to you in [timeframe]" and that window is open; or budget cycle / approval still in progress.
→ Action: Respect the timeline; soft re-engagement at the promised date.

**Competitive Loss** — client is comparing options or explicitly chose competitor.
→ Action: Ask directly; if lost, request a close-out conversation for feedback.

**Structural Issue** — pricing, scope, or terms are misaligned; client has unanswered questions blocking decision.
→ Action: Clarify assumptions, propose revised structure, or escalate internally.

---

### Step 3: Assess Risk Level

```
Low Risk    (<7 days, clear next step, active negotiation)
Medium Risk (7–14 days, unclear next step, recent engagement was positive)
High Risk   (14+ days, radio silence, multiple touches with no response)
Critical    (21+ days, explicit competitor mention, unfavorable decision-maker change)
```

---

### Step 4: Output Advisory

```
[OPPORTUNITY ADVISORY] {Company Name} — {Opportunity Name}

SNAPSHOT
├─ Stage: {stage}
├─ Days since last engagement: {N}
├─ Last interaction: {date, type, outcome}
└─ Key contact: {name, title}

DIAGNOSIS
├─ Category: {Information Gap | Timing Mismatch | Competitive Loss | Structural Issue}
├─ Root cause: {2–3 sentence explanation based on actual engagement history}
└─ Confidence: {High | Medium | Low}

RECOMMENDATION
├─ Risk level: {Low | Medium | High | Critical}
├─ Next action: {specific step}
├─ Timeline: {e.g. "within 2 days"}
├─ Tone: {e.g. "casual check-in" | "confident rebuttal" | "professional close-out"}
└─ Alternative: {if primary doesn't work, try…}

ESCALATION
└─ Involve [Sales Rep]? {Yes | No | Only if X}
```

---

## Pitfalls

1. **Always use localhost** — never external URL.

2. **Diagnose at day 7–10** — by day 14, momentum is largely gone. Don't wait.

3. **"No response" ≠ "no interest"** — many stalls are timing-driven. Separate before deciding to close.

4. **Re-engage with a soft question first** — after silence, don't open with a detailed proposal. Ask a low-commitment question. Escalate only after they re-engage.

5. **Check the timeline they gave you** — if they said "end of Q3," don't follow up on day 3.

6. **`engagementNote` is RICH_TEXT** — extract plain text from `.json` before reading.
