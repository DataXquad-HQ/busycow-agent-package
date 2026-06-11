# CRM Schema — Twenty

Object definitions for the BusyCow CRM layer, powered by
[Twenty](https://twenty.com) (self-hosted).

For the install guide → `../../third-party-tools/twenty-crm/SETUP.md`
For the Hermes skill  → `../../shared-skills/twenty-crm.md`

---

## Standard Objects (built into Twenty)

These exist in every fresh Twenty workspace. No setup needed.

| Object | GraphQL query | Purpose |
|--------|--------------|---------|
| Company | `companies` | Accounts — clients, prospects, partners |
| Person | `people` | Contacts |
| Opportunity | `opportunities` | Sales deals |
| Note | `notes` | Interaction logs, meeting notes, research |
| Task | `tasks` | Action items with due dates + assignees |

**Note vs Task convention:**
Use `note` for *information* (meeting summaries, intel, research output).
Use `task` for *actions* (follow-ups, deadlines, assignments).
Prefer these built-in objects over custom `activity` objects —
they have better Timeline and relation support in the Twenty UI.

---

## Custom Objects

Create via Twenty UI (Settings → Data Model) or via the `twenty-crm` Hermes skill.

| Object singular | Plural | GraphQL query | Purpose |
|----------------|--------|--------------|---------|
| `partner` | `partners` | `partners` | Partnership pipeline (resellers, alliances, channels) |
| `quotation` | `quotations` | `quotations` | Sales quotations |
| `quotationItem` | `quotationItems` | `quotationItems` | Line items on quotations |
| `invoice` | `invoices` | `invoices` | Invoices issued to clients |
| `invoiceItem` | `invoiceItems` | `invoiceItems` | Line items on invoices |

### partner fields

| Field | Type | Purpose |
|-------|------|---------|
| `name` | TEXT (auto) | Partner name |
| `partnerStage` | SELECT | `PROSPECT / ACTIVE / ON_HOLD / ENDED` |
| `businessLine` | SELECT | Which product line this partner covers |
| `summary` | TEXT | One-line description |
| `description` | TEXT | Running narrative / notes |

### quotation fields

| Field | Type | Purpose |
|-------|------|---------|
| `quotationId` | TEXT | Human-readable ID e.g. `QT-2026-001` |
| `status` | SELECT | `DRAFT / SENT / ACCEPTED / REJECTED / EXPIRED` |
| `issueDate` | DATE_TIME | Date issued |
| `validUntil` | DATE_TIME | Expiry date |
| `currency` | TEXT | Currency code e.g. `USD` |
| `subtotal` | NUMBER | Before tax |
| `tax` | NUMBER | Tax amount |
| `total` | NUMBER | Grand total |
| `docLink` | LINKS | Link to the actual document (Google Doc / PDF) |
| `notes` | TEXT | Free-form notes |

### invoice fields

| Field | Type | Purpose |
|-------|------|---------|
| `invoiceId` | TEXT | Human-readable ID e.g. `INV-2026-001` |
| `invoiceStatus` | SELECT | `DRAFT / ISSUED / PAID / OVERDUE / VOID` |
| `invoiceDate` | DATE_TIME | Date of issue |
| `dueDate` | DATE_TIME | Payment due date |
| `paymentDate` | DATE_TIME | Actual payment received (if paid) |
| `currency` | TEXT | Currency code |
| `invoiceAmount` | NUMBER | Total billed |
| `collectedAmount` | NUMBER | Amount received |
| `outstandingBalance` | NUMBER | `invoiceAmount − collectedAmount` |
| `paymentMethod` | SELECT | `Bank Transfer / Stripe / Crypto / Other` |
| `docLink` | LINKS | Link to invoice document |
| `notes` | TEXT | Free-form notes |

---

## Custom Fields on Standard Objects

### Company extensions

| Field name | Type | Options |
|-----------|------|---------|
| `shortName` | TEXT | — |
| `companyType` | SELECT | `Client / Prospect / Partner / Vendor` |
| `source` | SELECT | `Referral / Inbound / Outbound / Event / Other` |

### Person extensions

| Field name | Type | Options |
|-----------|------|---------|
| `decisionRole` | SELECT | `Champion / Decision Maker / Influencer / Blocker` |
| `source` | SELECT | `Referral / Inbound / Outbound / Event / Other` |
| `whatsapp` | TEXT | — |
| `notes` | TEXT | — |

---

## Relations Map

```
Company ──< Opportunity    (company has many opportunities)
Company ──< Person         (company has many people)
Company ──< Partner        (company has many partner records)
Company ──< Quotation      (company has many quotations)
Company ──< Invoice        (company has many invoices)
Quotation ──< QuotationItem
Invoice   ──< InvoiceItem
Opportunity ──< Note       (auto-linked via Twenty's relation system)
Opportunity ──< Task
```

---

## Reserved Field Names (cannot be used)

`currency`, `name`, `id`, `createdAt`, `updatedAt`, `deletedAt`
