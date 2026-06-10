# Sales & Ops CRM — Lark Base Schema

## Overview

B2B sales pipeline schema for a multi-product company. Supports deal progression, partnership management, lead triage, quotation generation, and invoicing.

**Three-layer memory model:**
- **Lark Base** — live facts (current status, dates, amounts, owners)
- **GBrain** — accumulated knowledge (deal narrative, company intel, relationship history)
- **Lark Docs/Drive** — documents (quotation PDFs, signed contracts, invoices)

---

## Tables

### 1. Accounts (`{{TABLE_ID_ACCOUNTS}}`)

Companies in the CRM — clients, prospects, partners, vendors.

| Field | Type | Notes |
|-------|------|-------|
| Company Name | Text (Primary) | Full legal or trading name |
| Registered Name (EN) | Text | Legal English name |
| Registered Name (CH) | Text | Legal Chinese name |
| Status | SingleSelect | Hot / Warm / Cold |
| Type | MultiSelect | Client / Partner / Prospect / Vendor / Direct |
| Industry | SingleSelect | Tech/SaaS / Healthcare / Manufacturing / Retail / Logistics / etc. |
| Country | SingleSelect | e.g. Taiwan / Hong Kong / Malaysia |
| HQ Address | Text | |
| Company Email | Text | |
| Company Phone | Phone | |
| Website | URL | |
| Company LinkedIn | URL | |
| Description | Text | Company background notes |
| Enrichment Overview | Text | Auto-populated by enriching-leads skill |
| Last Contact Date | DateTime | Derived from latest Engagement |
| Last Enriched Date | DateTime | Set by account-enrichment cron |
| Contacts | DuplexLink → Contacts | |
| Opportunities | DuplexLink → Deals | |
| Partnership | DuplexLink → Partnerships | |
| Activities | DuplexLink → Engagements | |
| Invoices | DuplexLink → Invoices | |

### 2. Contacts (`{{TABLE_ID_CONTACTS}}`)

People in the CRM — linked to Accounts.

| Field | Type | Notes |
|-------|------|-------|
| Full Name | Text (Primary) | |
| 💼 Clients | DuplexLink → Accounts | Which company they work at |
| Role / Title | Text | Job title |
| Email | Email | |
| Phone | Phone | |
| Preferred Channel | SingleSelect | Email / WhatsApp / LINE / Phone |
| Decision Role | SingleSelect | Buyer / User / Influencer / Blocker / Champion |
| Source | Text | How we met them |
| Notes | Text | Background, personal context |
| 💼 Deals | SingleLink → Deals | Primary contact for a deal |
| 💼 Activities | DuplexLink → Engagements | |

### 3. Deals (`{{TABLE_ID_DEALS}}`)

Active sales opportunities.

| Field | Type | Notes |
|-------|------|-------|
| Deal Name | Text (Primary) | e.g. "[Company] — [Product] [description]" |
| Client | DuplexLink → Accounts | |
| Primary Contact | DuplexLink → Contacts | |
| Stage | SingleSelect | Lead / Qualified / Proposal / Negotiation / Won / Lost |
| Business Line | SingleSelect | [Your product lines] |
| Priority | SingleSelect | High / Medium / Low |
| Health Check | SingleSelect | On Track / Needs Follow-up / Awaiting Response / At Risk |
| Risk Indicator | SingleSelect | Low / Medium / High |
| Expected Value | Number | Estimated deal value |
| Probability % | Number | 0–100 |
| Expected Close Date | DateTime | |
| Next Follow-up Date | DateTime | |
| Last Update Date | DateTime | Set on every Leo update |
| Current Status Summary | Text | Leo-maintained narrative |
| Next Action Summary | Text | Leo-maintained next step |
| Description | Text | Deal context and background |
| Doc Link | URL | Link to proposal or contract |
| Activities | DuplexLink → Engagements | |
| Tasks | DuplexLink → Tasks | |
| Quotations | DuplexLink → Quotations | |
| Invoices | DuplexLink → Invoices | |
| Contract | DuplexLink → Contracts | |

### 4. Partnerships (`{{TABLE_ID_PARTNERSHIPS}}`)

Partner relationships — mirrors Deal progression logic, goal is signed partnership agreement.

| Field | Type | Notes |
|-------|------|-------|
| Partner Name | Text (Primary) | |
| Account | DuplexLink → Accounts | The partner company |
| Stage | SingleSelect | Prospect / Qualifying / Agreement / Active / Inactive |
| Partnership Type | SingleSelect | Reseller / Integrator / Technology / Referral |
| Status | SingleSelect | Active / Needs Follow-up / Dormant / Inactive |
| Territory | Text | Geographic or vertical coverage |
| Current Status Summary | Text | Leo-maintained |
| Next Action Summary | Text | Leo-maintained |
| Last Engagement Date | DateTime | |
| Owner | User | |
| Activities | DuplexLink → Engagements | |
| Tasks | DuplexLink → Tasks | |

### 5. Engagements (`{{TABLE_ID_ENGAGEMENTS}}`)

All customer and partner interactions.

| Field | Type | Notes |
|-------|------|-------|
| Title | Text (Primary) | Auto: "YYYY-MM-DD — [Contact] ([Type])" |
| Status | SingleSelect | Planned / Completed |
| Type | SingleSelect | Phone Call / In-person Visit / Online Meeting / WhatsApp/LINE / Demo / Email / Event |
| Date | DateTime | When the interaction happened or is planned |
| Account | DuplexLink → Accounts | |
| Contact | DuplexLink → Contacts | |
| Related Deal | DuplexLink → Deals | **Optional** — leave blank for nurture interactions |
| Related Partnership | DuplexLink → Partnerships | **Optional** |
| Notes | Text | Free-form notes |
| Next Action | Text | What happens next (extracted by Leo) |
| Owner | User | Who conducted the interaction |

> **Key design rule:** Related Deal and Related Partnership are both optional. Nurture engagements (C7) link only to Account/Contact — this keeps them out of the pipeline view.

### 6. Tasks (`{{TABLE_ID_TASKS}}`)

Follow-up actions generated by Leo after each engagement.

| Field | Type | Notes |
|-------|------|-------|
| Title | Text (Primary) | Task description |
| Done | Checkbox | Completion flag |
| Deadline | DateTime | Due date |
| Business Line | SingleSelect | [Your product lines] |
| Priority | SingleSelect | 🔴 High / 🟡 Medium / 🟢 Low |
| Responsible Person | User | Assignee |
| Description | Text | Task details |
| Agent Advice | Text | Leo-generated strategic advice |
| Related Deal | DuplexLink → Deals | |
| Related Partnership | DuplexLink → Partnerships | |
| Output Link | URL | Link to deliverable |

### 7. Quotations (`{{TABLE_ID_QUOTATIONS}}`)

| Field | Type | Notes |
|-------|------|-------|
| Quotation ID | Text (Primary) | Auto: QUO-YYYY-[Client]-NNN |
| Related Opportunity | DuplexLink → Deals | |
| Status | SingleSelect | Draft / Sent / Accepted / Rejected / Expired |
| Total Amount | Number | |
| Currency | SingleSelect | TWD / USD / HKD / SGD |
| Valid Until | DateTime | |
| Doc Link | URL | Link to PDF |
| Notes | Text | |

### 8. Invoices (`{{TABLE_ID_INVOICES}}`)

| Field | Type | Notes |
|-------|------|-------|
| Invoice ID | Text (Primary) | Auto: INV-YYYY-[Client]-NNN |
| Related Opportunity | DuplexLink → Deals | |
| Client | DuplexLink → Accounts | |
| Status | SingleSelect | Draft / Sent / Paid / Overdue |
| Amount | Number | |
| Currency | SingleSelect | TWD / USD / HKD / SGD |
| Issue Date | DateTime | |
| Due Date | DateTime | |
| Doc Link | URL | Link to PDF |

### 9. Contracts (`{{TABLE_ID_CONTRACTS}}`)

| Field | Type | Notes |
|-------|------|-------|
| Contract Name | Text (Primary) | |
| 💼 Opportunity | DuplexLink → Deals | |
| Signed By (Client) | DuplexLink → Accounts | |
| Status | SingleSelect | Draft / Sent / Signed / Expired |
| Start Date | DateTime | |
| End Date | DateTime | |
| Doc Link | URL | Link to signed PDF |

---

## Relationship Map

```
Account ──┬── Contacts (1:N)
          ├── Deals (1:N)
          ├── Partnerships (1:N)
          └── Engagements (1:N)

Deal ──┬── Engagements (1:N)
       ├── Tasks (1:N)
       ├── Quotations (1:N)
       ├── Invoices (1:N)
       └── Contracts (1:N)

Partnership ──┬── Engagements (1:N)
              └── Tasks (1:N)

Engagement ── (optional) Deal OR Partnership OR neither (nurture)
Task ──────── (optional) Deal OR Partnership
```

---

## GBrain Page Conventions

Every Account and Contact saved to Lark Base must also have a corresponding GBrain page:

| CRM Record | GBrain Slug | Page Type |
|------------|-------------|-----------|
| Account | `companies/{kebab-name}` | `company` |
| Contact | `people/{kebab-full-name}` | `person` |

Every Engagement logged must trigger:
1. `mcp_gbrain_add_timeline_entry` on the Account's GBrain page
2. `mcp_gbrain_extract_facts` from the engagement notes
