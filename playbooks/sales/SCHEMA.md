# Sales & Ops Base — Schema Reference

This is the live schema of the BusyCow Sales & Operations Lark Bitable base.
Use the `lark-bitable-schema-setup` skill to recreate this in a new environment.

**19 tables across 4 domains:**
- ⚙️ Config (3 tables) — reference data: products, entities, vendors
- 💼 CRM (7 tables) — accounts, contacts, opportunities, partnerships, activities, quotations
- 💰 Finance (5 tables) — revenue, expenses, invoices, monthly summary
- 📋 Ops (4 tables) — goals, initiatives, tasks, contracts

---

## Table: ⚙️ Product Config

| Field Name | Type | Notes |
|-----------|------|-------|
| Product Name | Text | Primary field |
| Product Line | SingleSelect | |
| Unit Price (USD) | Number | |
| COGS (USD) | Number | |
| Commission Rate % | Number | |
| Description | Text | |
| Status | SingleSelect | |
| Notes | Text | |

---

## Table: ⚙️ Company Entities

| Field Name | Type | Notes |
|-----------|------|-------|
| Entity Name | Text | Primary field |
| Short Name | Text | |
| Country | SingleSelect | |
| Registration No. / UEN | Text | |
| Registered Address | Text | |
| Contact Address | Text | |
| Default Currency | SingleSelect | |
| Bank Name | Text | |
| Bank Address | Text | |
| SWIFT Code | Text | |
| Bank Code | Text | |
| Account No. (USD/HKD) | Text | |
| Account No. (NTD) | Text | |
| Account Name (EN) | Text | |
| Account Name (ZH) | Text | |
| Notes | Text | |

---

## Table: ⚙️ Vendors

| Field Name | Type | Notes |
|-----------|------|-------|
| Vendor Name | Text | Primary field |
| Short Name | Text | |
| Country | SingleSelect | |
| Category | SingleSelect | |
| Contact Person | Text | |
| Contact Email | Text | |
| Contact Phone | Phone | |
| Website | URL | |
| Default Currency | SingleSelect | |
| Payment Terms | SingleSelect | |
| Billing Entity | SingleSelect | References Company Entities |
| Recurring | SingleSelect | |
| Status | SingleSelect | |
| Notes | Text | |

---

## Table: 💼 Accounts

Central hub — links to all CRM and finance tables.

| Field Name | Type | Notes |
|-----------|------|-------|
| Client Name | Text | Primary field |
| Short Name | Text | |
| Country | SingleSelect | |
| Address | Text | |
| Company Email | Text | |
| Company Phone | Phone | |
| Type | MultiSelect | Direct / Reseller / Partner / End User |
| Status | SingleSelect | Active / Inactive / Prospect |
| Description | Text | |
| Industry | SingleSelect | |
| Company Size | SingleSelect | |
| Source | SingleSelect | How they entered pipeline |
| Website | URL | |
| Contacts | DuplexLink | → 💼 Contacts |
| Opportunities | DuplexLink | → 💼 Opportunity |
| Partnership | DuplexLink | → 💼 Partnership |
| Activities | DuplexLink | → 💼 Activities |
| Contracts | DuplexLink | → 📋 Contracts |
| Invoices | DuplexLink | → 💰 Invoices |

---

## Table: 💼 Contacts

| Field Name | Type | Notes |
|-----------|------|-------|
| Contact Name | Text | Primary field |
| Company | DuplexLink | → 💼 Accounts |
| Country | Lookup | Auto-lookup from linked Account |
| Decision Role | SingleSelect | Buyer / User / Influencer / Blocker / Champion |
| Phone / WhatsApp | Phone | |
| Contact Email | Email | |
| LinkedIn | URL | |
| Notes | Text | |
| Activities | DuplexLink | → 💼 Activities |

---

## Table: 💼 Opportunity

| Field Name | Type | Notes |
|-----------|------|-------|
| ID | Text | Primary field — format: OP-YYYY-NNN |
| Summary | Text | One-line description |
| Client | DuplexLink | → 💼 Accounts |
| Stage | SingleSelect | Lead / Qualified / Proposal / Negotiation / Closed Won / Closed Lost |
| Business Line | SingleSelect | |
| Owner | User | |
| Expected Value | Number | USD |
| Expected Close Date | DateTime | |
| Probability % | Number | |
| Doc Link | URL | |
| Description | Text | Full notes |
| Activities | DuplexLink | → 💼 Activities |
| Quotations | DuplexLink | → 💼 Quotation |
| Invoices | DuplexLink | → 💰 Invoices |
| Contract | DuplexLink | → 📋 Contracts |
| Tasks | DuplexLink | → 📋 Tasks |
| Goal | DuplexLink | → 📋 Goals |

---

## Table: 💼 Partnership

| Field Name | Type | Notes |
|-----------|------|-------|
| ID | Text | Primary field — format: PA-YYYY-NNN |
| Summary | Text | One-line description |
| Stage | SingleSelect | Prospect / Qualifying / Agreement / Active / On Hold / Inactive |
| Account | DuplexLink | → 💼 Accounts |
| Business Line | MultiSelect | |
| Description | Text | Running narrative log |
| Activities | DuplexLink | → 💼 Activities |
| Tasks | DuplexLink | → 📋 Tasks |
| Contract | DuplexLink | → 📋 Contracts |
| Goal | DuplexLink | → 📋 Goals |

---

## Table: 💼 Activities

| Field Name | Type | Notes |
|-----------|------|-------|
| Summary | Text | Primary field — one-line description |
| Account | DuplexLink | → 💼 Accounts |
| Contact | DuplexLink | → 💼 Contacts |
| Date | DateTime | When it happened |
| Type | SingleSelect | 電話 / 實體拜訪 / 線上會議 / WhatsApp/LINE / Demo / 訊息 / Other |
| Client Response | Text | What they said / their reaction |
| Stage Advanced? | Checkbox | Did the deal move forward? |
| Next Action | Text | What needs to happen next |
| Owner | User | Who conducted the interaction |
| Opportunity | DuplexLink | → 💼 Opportunity |
| Partnership | DuplexLink | → 💼 Partnership |

---

## Table: 💼 Quotation

| Field Name | Type | Notes |
|-----------|------|-------|
| Quotation ID | Text | Primary field — format: QT-YYYY-NNN |
| Client | Text | Client name (free text) |
| Issue Date | DateTime | |
| Valid Until | DateTime | |
| Currency | SingleSelect | |
| Subtotal | Number | |
| Tax | Number | |
| Total | Number | |
| Status | SingleSelect | Draft / Sent / Accepted / Rejected / Expired |
| Doc Link | URL | Link to Google Doc quotation |
| Notes | Text | |
| Owner | Text | |
| Invoices | DuplexLink | → 💰 Invoices |
| Related Opportunity | DuplexLink | → 💼 Opportunity |
| Quotation Items | DuplexLink | → 💼 Quotation Items |

---

## Table: 💼 Quotation Items

| Field Name | Type | Notes |
|-----------|------|-------|
| Item Name | Text | Primary field |
| Description | Text | |
| Qty | Number | |
| Unit | Text | |
| Unit Price | Number | |
| Amount | Number | |
| Notes | Text | |
| Quotation | DuplexLink | → 💼 Quotation |

---

## Table: 💰 Revenue

| Field Name | Type | Notes |
|-----------|------|-------|
| Month | DateTime | Primary field |
| Date | DateTime | Actual transaction date |
| Entity | SingleSelect | Which legal entity |
| Product Line | SingleSelect | |
| Fee Type | SingleSelect | |
| Revenue (USD) | Number | |
| Client | Text | |
| Invoice # | Text | |
| Status | SingleSelect | Forecast / Actual |
| Entry Type | SingleSelect | |
| Units | Number | |
| Unit Price (USD) | Number | |
| COGS (USD) | Number | |
| Gross Profit (USD) | Number | |
| Gross Margin % | Number | |
| Product / Service | Text | |
| Sales Commission (USD) | Number | |
| Notes | Text | |

---

## Table: 💰 Expenses

| Field Name | Type | Notes |
|-----------|------|-------|
| Month | DateTime | Primary field |
| Entity | SingleSelect | |
| Category | SingleSelect | |
| Sub-item | Text | |
| Amount (USD) | Number | |
| Vendor | Text | |
| Recurring | SingleSelect | |
| Status | SingleSelect | Forecast / Actual |
| Entry Type | SingleSelect | |
| Product Line | SingleSelect | |
| Notes | Text | |

---

## Table: 💰 Monthly Summary

Aggregated financial view per month — auto-populated by formulas or agent.

| Field Name | Type | Notes |
|-----------|------|-------|
| Month | DateTime | Primary field |
| Year-Month | Text | e.g. 2026-01 |
| Status | SingleSelect | Open / Closed |
| Total Forecast Revenue (USD) | Number | |
| Total Actual Revenue (USD) | Number | |
| Forecast Expenses (USD) | Number | |
| Actual Expenses (USD) | Number | |
| Net Cash Flow (USD) | Number | |
| Opening Balance (USD) | Number | |
| Closing Balance (USD) | Number | |
| Cumulative Balance (USD) | Number | |
| [Entity] Forecast Revenue (USD) | Number | Repeat per entity |
| [Entity] Actual Revenue (USD) | Number | Repeat per entity |
| [Entity] Forecast Expenses (USD) | Number | Repeat per entity |
| [Entity] Actual Expenses (USD) | Number | Repeat per entity |
| [Entity] Net Cash Flow (USD) | Number | Repeat per entity |
| [Product Line] Forecast Rev (USD) | Number | Repeat per product line |
| [Product Line] Actual Rev (USD) | Number | Repeat per product line |
| USD/NTD Rate | Number | If multi-currency needed |
| Total COGS (USD) | Number | |
| Forecast Gross Profit (USD) | Number | |
| Actual Gross Profit (USD) | Number | |
| Gross Margin % | Number | |
| Sales Commission (USD) | Number | |
| Notes | Text | |

---

## Table: 💰 Invoices

| Field Name | Type | Notes |
|-----------|------|-------|
| Invoice ID | Text | Primary field — format: INV-YYYY-NNN |
| Invoice Status | SingleSelect | Draft / Sent / Partially Paid / Paid / Overdue / Cancelled |
| Client | DuplexLink | → 💼 Accounts |
| Entity | SingleSelect | Which legal entity is issuing |
| Invoice Date | DateTime | |
| Due Date | DateTime | |
| Currency | SingleSelect | |
| Invoice Amount | Number | |
| Collected Amount | Number | |
| Outstanding Balance | Number | |
| Payment Date | DateTime | |
| Payment Method | SingleSelect | |
| Product Line | SingleSelect | |
| Related Quote # | Text | |
| Doc Link | URL | |
| Notes | Text | |
| Related Quotation | DuplexLink | → 💼 Quotation |
| Related Opportunity | DuplexLink | → 💼 Opportunity |
| Invoice Items | DuplexLink | → 💰 Invoice Items |

---

## Table: 💰 Invoice Items

| Field Name | Type | Notes |
|-----------|------|-------|
| Item Name | Text | Primary field |
| Description | Text | |
| Qty | Number | |
| Unit | Text | |
| Unit Price | Number | |
| Amount | Number | |
| Notes | Text | |
| Invoices | DuplexLink | → 💰 Invoices |

---

## Table: 📋 Contracts

| Field Name | Type | Notes |
|-----------|------|-------|
| ID | Text | Primary field — format: CT-YYYY-NNN |
| Type | SingleSelect | Sales / Partnership / NDA / Service / Other |
| Status | SingleSelect | Draft / Active / Expired / Terminated |
| Client | DuplexLink | → 💼 Accounts |
| Entity | SingleSelect | Which legal entity |
| Product Lines | MultiSelect | |
| Territory | Text | Geographic scope |
| Exclusivity | SingleSelect | Exclusive / Non-exclusive |
| Effective Date | DateTime | |
| Expiry Date | DateTime | |
| Term | Text | e.g. "1 year, auto-renewal" |
| Auto Renewal | Checkbox | |
| Currency | SingleSelect | |
| Wholesale Price (USD) | Text | |
| SRP (USD) | Text | |
| Min Annual Sales (USD) | Number | |
| Volume Discount | Text | |
| Commission Rate % | Number | |
| Payment Terms | Text | |
| Delivery Terms | Text | |
| Governing Law | Text | |
| Year 1 Target (USD) | Number | |
| Year 2 Target (USD) | Number | |
| Year 3 Target (USD) | Number | |
| Signed By (Supplier) | Text | |
| Signed By (Client) | Text | |
| Doc Link | URL | |
| Special Conditions | Text | |
| Notes | Text | |
| Related Partnership | DuplexLink | → 💼 Partnership |
| Related Opportunity | DuplexLink | → 💼 Opportunity |

---

## Table: 📋 Goals

| Field Name | Type | Notes |
|-----------|------|-------|
| Goal Name | Text | Primary field |
| Business Line | SingleSelect | |
| Status | SingleSelect | Active / Achieved / Cancelled |
| Target Date | DateTime | |
| Success Metric | Text | How we know it's achieved |
| Description | Text | |
| Initiatives | DuplexLink | → 📋 Initiatives |
| Opportunities | DuplexLink | → 💼 Opportunity |
| Partnerships | DuplexLink | → 💼 Partnership |

---

## Table: 📋 Initiatives

| Field Name | Type | Notes |
|-----------|------|-------|
| Initiative Name | Text | Primary field |
| Status | SingleSelect | Planning / In Progress / Done / Cancelled |
| Business Line | SingleSelect | |
| Type | SingleSelect | |
| Target Finished | DateTime | |
| Notes | Text | |
| Goals | DuplexLink | → 📋 Goals |
| Tasks | DuplexLink | → 📋 Tasks |

---

## Table: 📋 Tasks

| Field Name | Type | Notes |
|-----------|------|-------|
| Task Name | Text | Primary field |
| Done | Checkbox | |
| Deadline | DateTime | |
| Business Line | SingleSelect | |
| Priority | SingleSelect | High / Medium / Low |
| Responsible Person | User | |
| Description | Text | |
| Initiatives | DuplexLink | → 📋 Initiatives |
| Opportunity | DuplexLink | → 💼 Opportunity |
| Partnership | DuplexLink | → 💼 Partnership |

---

## Relationship Map

```
Goals ←→ Initiatives ←→ Tasks
  ↕              ↕          ↕
Opportunity ←→ Partnership
  ↕      ↕         ↕
Accounts  Activities  Contracts
  ↕
Contacts / Quotations / Invoices
```

## Notes for New Setup

1. **Create tables in this order:** Config tables first → Accounts → Contacts → then other CRM tables (DuplexLinks require target table to exist first)
2. **All monetary values in USD** unless specified
3. **ID formats:** OP-YYYY-NNN (Opportunities), PA-YYYY-NNN (Partnerships), CT-YYYY-NNN (Contracts), INV-YYYY-NNN (Invoices), QT-YYYY-NNN (Quotations)
4. **Monthly Summary** is manually maintained or populated by the agent via Revenue/Expenses aggregation — not formula-driven
5. Use the `lark-bitable-schema-setup` skill to automate table creation via API
