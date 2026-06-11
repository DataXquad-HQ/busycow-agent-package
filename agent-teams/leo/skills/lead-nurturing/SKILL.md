---
name: lead-nurturing
description: >
  Identify contacts in Twenty CRM with no active Deal or Partnership who haven't
  been engaged in 30+ days. Draft personalised check-in messages. Triggered
  manually ("send a check-in to [contact]") or by monthly cron (1st of month).
  Runs in Basic mode (no article) by default.
triggers:
  - "nurture"
  - "check-in"
  - "cold contacts"
  - "monthly nurture"
  - "send check-in"
version: "3.0"
author: Leo (BD Director Agent)
---

# Lead Nurturing

## Purpose

For every Contact in Twenty CRM with no active Deal or Partnership and no engagement in 30+ days — draft a personalised check-in message for the sales rep to review and send.

Not broadcast marketing. One-to-one personal outreach. **Leo never auto-sends.**

---

## CRM Reference

**Twenty CRM:** `http://localhost:3001` (always localhost)
**GraphQL endpoint:** `http://localhost:3001/graphql`

---

## Two Modes

**Mode A — Manual:** Sales rep says "send a check-in to [name]" → Leo drafts for that contact.

**Mode B — Monthly scan (cron):** Scan all qualifying contacts, generate batch of drafts, deliver to sales rep for review.

---

## Detection Logic

A Contact qualifies when ALL of these are true:
1. **No active Deal** — no linked opportunity with stage ≠ CLOSED_WON/CLOSED_LOST
2. **No active Partnership** — no linked partnership with stage = ACTIVE
3. **No engagement in 30+ days** — last engagementDate > 30 days ago or no engagement at all

---

## Workflow

### Step 1: Find Contacts to Nurture

**Mode A:**
```graphql
query {
  people(filter: { name: { firstName: { like: "%{name}%" } } }) {
    edges {
      node {
        id
        name { firstName lastName }
        jobTitle
        emails { primaryEmail }
        preferredChannel
        remarks
        lastContactDate
        company { name companyOverview }
        pointOfContactForOpportunities {
          edges { node { id stage } }
        }
        primaryContactForPartnerships {
          edges { node { id stage } }
        }
        engagementsAttended {
          edges {
            node {
              engagementDate outcome
              engagementNote { json }
            }
          }
        }
      }
    }
  }
}
```

**Mode B — monthly scan:**
```graphql
query {
  people(
    filter: {
      lastContactDate: { lte: "{30_days_ago_iso}" }
    }
    first: 100
  ) {
    edges {
      node {
        id name { firstName lastName }
        preferredChannel lastContactDate
        remarks jobTitle
        company { name }
        pointOfContactForOpportunities { edges { node { stage } } }
        primaryContactForPartnerships { edges { node { stage } } }
      }
    }
  }
}
```

Then filter client-side:
- Skip if any linked opportunity has stage ≠ CLOSED_WON/CLOSED_LOST
- Skip if any linked partnership has stage = ACTIVE

---

### Step 2: Pull Context

For each qualifying contact:
- Last engagement: date, type, outcome summary
- Remarks field (personal background, topics discussed)
- Company overview
- Preferred channel

---

### Step 3: Draft Message (Basic Mode)

**Email:**
```
Subject: [personalised — reflects check-in context, not "just checking in"]

Hi {Name},

[1–2 sentences: personalised greeting referencing last interaction or
 something relevant to their industry/role]

[1 genuine question relevant to their world]

[Light CTA — coffee chat, quick call, simple reconnect]

[Signature]
```
Target: under 120 words.

**WhatsApp / LINE:**
```
Hi {Name},

[1 sentence warm greeting]

[1 genuine question relevant to their industry or role]

[Light CTA]
```
3–4 lines max.

---

### Step 4: Deliver Drafts

**Mode A output:**
```
📬 Nurture Draft — {Contact Name}

Channel: {Email / WhatsApp / LINE}
Last contact: {N days ago — brief summary}

--- Draft ---
{message body}
---

Should I send this, or would you prefer to send it yourself?
```

**Mode B output:**
```
📬 Monthly Nurture List — {N} contacts

1. {Name} ({Company}) — last contact: {N days ago}
   Channel: {channel}
   Draft: {first 40 chars...}

2. ...

Review one by one, or approve all for sending?
```

---

### Step 5: Log Engagement After Sending

After sending, create an Engagement record:

```graphql
mutation {
  createEngagement(input: {
    engagement: {
      name: "{YYYY-MM-DD} — Nurture — {Contact Name}"
      engagementType: "EMAIL"
      engagementStatus: "COMPLETED"
      engagementDate: "{send_date_iso}"
      engagementNote: { json: ... }
      companyId: "{company_id}"
    }
  }) { id }
}
```

Link the contact:
```graphql
mutation {
  updateEngagement(id: "{id}", input: {
    engagement: {
      clientAttendees: { connect: [{ id: "{person_id}" }] }
    }
  }) { id }
}
```

**Leave `opportunity` and `partnership` null** — nurture engagements must not appear in pipeline views.

Also update `lastContactDate` on the person:
```graphql
mutation {
  updatePerson(id: "{person_id}", input: {
    person: { lastContactDate: "{send_date_iso}" }
  }) { id }
}
```

---

## Pitfalls

1. **Always use localhost** — never external URL.

2. **Never auto-send** — always present drafts for human review.

3. **Leave opportunity/partnership null on nurture engagements** — intentional. Keeps nurture out of pipeline views.

4. **Basic mode is the default** — a genuine personalised check-in with no article is often more effective than a generic article share.

5. **Skip contacts with active deals** — those are managed by `deal-progressing`.

6. **`lastContactDate` null** — if null, treat as "never contacted" → always qualifies for nurture.

7. **`engagementNote` is RICH_TEXT** — use Twenty's JSON format for the field.
