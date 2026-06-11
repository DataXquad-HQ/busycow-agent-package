---
name: follow-up-email
description: >
  Use when you need to draft a follow-up email to a prospect, client, or partner.
  Fetches deal/partnership context from Twenty CRM and generates context-aware
  copy matched to the deal stage and relationship depth.
triggers:
  - "follow-up email"
  - "draft email"
  - "follow up"
  - "寫 email"
  - "跟進信"
version: "3.0"
author: Leo (BD Director Agent)
---

# Follow-Up Email

## Purpose

Draft a follow-up email (or WhatsApp/LINE message) based on real deal context from Twenty CRM. Every draft references specific prior interactions — not generic templates.

**Leo drafts. Human sends. Never auto-send.**

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost)
**GraphQL endpoint:** `http://localhost:3001/graphql`

---

## When to Use

- Following up after a meeting or call
- Re-engaging after silence (7–20 days)
- Responding to an objection
- Confirming next steps after agreement in principle
- Closing out a deal professionally

---

## Workflow

### Step 1: Fetch Deal + Engagement Context

```graphql
query GetFollowUpContext($oppId: ID!) {
  opportunity(id: $oppId) {
    id name stage
    currentStatusSummary nextActionSummary
    primaryContact
    company { name companyOverview }
    pointOfContact {
      name { firstName lastName }
      emails { primaryEmail }
      preferredChannel
    }
    engagements(
      filter: { engagementStatus: { eq: "COMPLETED" } }
      orderBy: { engagementDate: DescNullsLast }
      first: 5
    ) {
      edges {
        node {
          engagementDate engagementType
          outcome nextAction
          engagementNote { json }
        }
      }
    }
  }
}
```

---

### Step 2: Classify Email Type

| Situation | Email Type |
|---|---|
| Just had a meeting | Summation — recap + confirm next step |
| 3–7 days since last contact | Light follow-up — low pressure |
| 7–14 days silence | Re-engagement — casual check-in |
| 14+ days silence | Direct check-in — ask if still a priority |
| Client raised objection | Objection Rebuttal — empathetic + data-backed |
| Deal closing | Close-out — professional, door open |

---

### Step 3: Draft Email

**Summation (after meeting):**
```
Subject: {Company} — {topic discussed}

Hi {Name},

Thanks for the time today. Key takeaway: {one sentence}.
Next step: {specific action + timeline}.

[Signature]
```

**Re-engagement (7–14 days):**
```
Subject: {Company} — quick question on your timeline

Hi {Name},

Following up on {topic} from {date}. Are you still evaluating, or should we check back later?

[Signature]
```

**Direct check-in (14+ days):**
```
Subject: {Company} — {deal topic}

Hi {Name},

Quick question: is {product/topic} still a priority, or should we look at this again in {timeframe}?

[Signature]
```

**Objection rebuttal:**
```
Subject: {Company} — re: {objection topic}

Hi {Name},

I hear that {concern}. Here's how we think about it: {reframe + one data point}.

Happy to walk through this on a call if helpful.

[Signature]
```

---

### Step 4: Output

```
[FOLLOW-UP EMAIL DRAFT]

TO: {name} <{email}>
SUBJECT: {subject}

{body}

---
Context:
Type: {email type}
Days since last contact: {N}
Last interaction: {date, type, key outcome}
Tone rationale: {why this tone fits}

If no response in 3 days: {alternative angle}
```

---

## Pitfalls

1. **Always use localhost** — never external URL.

2. **Every email must reference specific prior context** — date, name, topic. Generic = low response.

3. **One CTA per email** — don't mix asks. One clear request with a specific timeline.

4. **Don't apologise for following up** — say "wanted to circle back", not "sorry for bothering you".

5. **`engagementNote` is RICH_TEXT** — extract plain text from `.json` before reading.

6. **Short emails outperform long ones** — 3–4 sentences max for re-engagement. If you have a lot to say, propose a call instead.
