# CRM Schema — Twenty

Object definitions for the DataXquad / GeoKernel CRM layer, powered by
[Twenty](https://twenty.com) (self-hosted, `localhost:3001`).

For the install guide → `../../third-party-tools/twenty-crm/SETUP.md`

> **Format note:** Every field entry below includes:
> - `type` — the Twenty field type used when creating via API or Settings → Data Model
> - `options` — valid values for SELECT / MULTI_SELECT fields (written as the `value` key in Twenty's API)
> - `description` — what this field is for; this text maps directly to the `description` property when creating fields via the metadata API

---

## Standard Objects (built into Twenty)

These exist in every fresh Twenty workspace. No setup needed — only extend with custom fields.

| Object | GraphQL query | Purpose |
|--------|--------------|---------|
| Account | `accounts` | Account master record — clients, prospects, partners |
| Contact | `people` | Individual contact |
| Deal | `opportunities` | Sales deal / pipeline opportunity |
| Note | `notes` | Information record — meeting summaries, research, intel (Twenty built-in) |
| Task | `tasks` | Action items with due dates and assignees |

**Note vs Task convention:**
Use `note` for *information* (meeting summaries, intel, research output).
Use `task` for *actions* (follow-ups, deadlines, assignments).
These built-in objects have full Timeline and relation support in Twenty UI.

---

## Custom Objects

Create via Settings → Data Model or via the metadata API.

| Object singular | Plural | GraphQL query | Purpose |
|----------------|--------|--------------|---------|
| `partnership` | `partnerships` | `partnerships` | Partner relationship lifecycle — resellers, integrators, technical providers |
| `engagement` | `engagements` | `engagements` | Customer / partner interaction record — call, meeting, email, event |
| `quotation` | `quotations` | `quotations` | Sales quotation document |
| `quotationItem` | `quotationItems` | `quotationItems` | Line items within a quotation |
| `contract` | `contracts` | `contracts` | Signed agreement document |

---

## Field Definitions

### Account (Twenty object: `company`)

> **Purpose:** Account master record — clients, prospects, partners. `companyOverview` 是這間公司的基本事實（是誰、做什麼）；`enrichmentOverview` 是最新市場消息，由 enrichment run 寫入。

#### 🔧 System（內部系統欄位，無法修改）

| Field Name | Label | Type |
|---|---|---|
| `id` | Id | UUID |
| `createdAt` | Creation date | DATE_TIME |
| `updatedAt` | Last update | DATE_TIME |
| `deletedAt` | Deleted at | DATE_TIME |
| `createdBy` | Created by | ACTOR |
| `updatedBy` | Updated by | ACTOR |
| `position` | Position | POSITION |
| `searchVector` | Search vector | TS_VECTOR |

#### 📦 App（Twenty 預設內建）

| Field Name | Label | Type |
|---|---|---|
| `name` | Company Name | TEXT |
| `domainName` | Website | LINKS |
| `address` | HQ Address | ADDRESS |
| `annualRevenue` | Annual Revenue | CURRENCY |
| `linkedinLink` | Company Linkedin | LINKS |
| `accountOwner` | Account Owner | RELATION |
| `people` | People | RELATION |
| `opportunities` | Opportunities | RELATION |
| `noteTargets` | Notes | RELATION |
| `taskTargets` | Tasks | RELATION |
| `attachments` | Attachments | RELATION |
| `timelineActivities` | Timeline Activities | RELATION |

#### ✏️ Custom（我們自己加的）

| Field Name | Label | Type | Options |
|---|---|---|---|
| `accountStatus` | Status | SELECT | `HOT` / `WARM` / `COLD` |
| `accountType` | Type | MULTI_SELECT | `CLIENT` / `PARTNER` / `PROSPECT` / `VENDOR` / `DIRECT` |
| `country` | Country | SELECT | `TAIWAN` / `HONG_KONG` / `MALAYSIA` / `OMAN` / `SINGAPORE` / `JAPAN` / `CHINA` / `OTHER` |
| `industry` | Industry | MULTI_SELECT | `TECH_SAAS` / `HEALTHCARE` / `MANUFACTURING_TRADING` / `WATER_UTILITIES` / `RETAIL_ECOMMERCE` / `LOGISTICS_TRANSPORT` / `CONSTRUCTION_PROPERTY` / `FINANCE_INSURANCE` / `EDUCATION` / `GOVERNMENT_PUBLIC` / `FNB_HOSPITALITY` / `OTHER` |
| `enrichmentOverview` | Enrichment Overview | TEXT | — |
| `companyOverview` | Company Overview | TEXT | — |
| `registeredNameEn` | Registered Name (EN) | TEXT | — |
| `registeredNameCh` | Registered Name (CH) | TEXT | — |
| `companyEmail` | Company Email | EMAILS | — |
| `companyPhone` | Company Phone | PHONES | — |
| `lastEnrichedDate` | Last Enriched Date | DATE_TIME | — |
| `lastContactDate` | Last Contact Date | DATE_TIME | — |
| `pic` | *(pic)* | TEXT | — |
| `partnerships` | Partnerships | RELATION | — |
| `engagements` | Engagements | RELATION | — |

---

### Contact (Twenty object: `person`)

> **Purpose:** Individual contact master record. Source tracks how we first met this person — it lives on the Contact, not the Account.

#### 🔧 System（內部系統欄位，無法修改）

| Field Name | Label | Type |
|---|---|---|
| `id` | Id | UUID |
| `createdAt` | Creation date | DATE_TIME |
| `updatedAt` | Last update | DATE_TIME |
| `deletedAt` | Deleted at | DATE_TIME |
| `createdBy` | Created by | ACTOR |
| `updatedBy` | Updated by | ACTOR |
| `avatarUrl` | Avatar | TEXT |
| `avatarFile` | Avatar File | FILES |
| `position` | Position | POSITION |
| `searchVector` | Search vector | TS_VECTOR |

#### 📦 App（Twenty 預設內建）

| Field Name | Label | Type |
|---|---|---|
| `name` | Name | FULL_NAME |
| `emails` | Emails | EMAILS |
| `phones` | Phones | PHONES |
| `jobTitle` | Job Title | TEXT |
| `linkedinLink` | Linkedin | LINKS |
| `company` | Company | RELATION |
| `pointOfContactForOpportunities` | Opportunities | RELATION |
| `noteTargets` | Notes | RELATION |
| `taskTargets` | Tasks | RELATION |
| `attachments` | Attachments | RELATION |
| `messageParticipants` | Message Participants | RELATION |
| `calendarEventParticipants` | Calendar Event Participants | RELATION |
| `timelineActivities` | Events | RELATION |

#### ✏️ Custom（我們自己加的）

| Field Name | Label | Type | Options |
|---|---|---|---|
| `status` | Status | SELECT | `HOT` / `WARM` / `COLD` / `INACTIVE` |
| `country` | Country | SELECT | `TAIWAN` / `HONG_KONG` / `CHINA` / `MALAYSIA` / `JAPAN` / `SINGAPORE` / `OTHER` |
| `preferredChannel` | Preferred Channel | SELECT | `WHATSAPP` / `EMAIL` / `PHONE` / `LINKEDIN` / `LINE` / `WECHAT` |
| `decisionRole` | Decision Role | SELECT | `DECISION_MAKER` / `CHAMPION` / `INFLUENCER` / `END_USER` / `GATEKEEPER` |
| `source` | Source | SELECT | `OUTBOUND_MAYA` / `INBOUND_WEB` / `REFERRAL` / `EVENT` / `PARTNER` |
| `department` | Department | TEXT | — |
| `remarks` | Remarks | TEXT | — |
| `lastContactDate` | Last Contact Date | DATE_TIME | — |

---

### Deal (Twenty object: `opportunity`)

> **Purpose:** Sales pipeline deal. One deal = one sales motion for one product/service to one account.

#### 🔧 System（內部系統欄位，無法修改）

| Field Name | Label | Type |
|---|---|---|
| `id` | Id | UUID |
| `createdAt` | Creation date | DATE_TIME |
| `updatedAt` | Last update | DATE_TIME |
| `deletedAt` | Deleted at | DATE_TIME |
| `createdBy` | Created by | ACTOR |
| `updatedBy` | Updated by | ACTOR |
| `position` | Position | POSITION |
| `searchVector` | Search vector | TS_VECTOR |

#### 📦 App（Twenty 預設內建）

| Field Name | Label | Type |
|---|---|---|
| `name` | Name | TEXT |
| `amount` | Expected Amount | CURRENCY |
| `closeDate` | Expected Close date | DATE_TIME |
| `stage` | Stage | SELECT |
| `company` | Company | RELATION |
| `owner` | Owner | RELATION |
| `pointOfContact` | Primary Contact | RELATION |
| `noteTargets` | Notes | RELATION |
| `taskTargets` | Tasks | RELATION |
| `attachments` | Attachments | RELATION |
| `timelineActivities` | Timeline Activities | RELATION |

#### ✏️ Custom（我們自己加的）

| Field Name | Label | Type | Options |
|---|---|---|---|
| `priority` | Priority | SELECT | `HIGH` / `MEDIUM` / `LOW` |
| `dealType` | Deal Type | SELECT | `DIRECT` / `PARTNER_LED` |
| `healthCheck` | Health Check | SELECT | `ON_TRACK` / `NEEDS_FOLLOW_UP` / `AWAITING_RESPONSE` / `AT_RISK` |
| `probability` | Probability % | NUMBER | — |
| `currentStatusSummary` | Current Status Summary | TEXT | — |
| `nextActionSummary` | Next Action Summary | TEXT | — |
| `overview` | Overview | TEXT | — |
| `lastUpdateDate` | Last Contact Date | DATE_TIME | — |
| `nextFollowUpDate` | Next Follow-up Date | DATE | — |
| `relevantContacts` | Relevant Contacts | RELATION | — |
| `engagements` | Engagements | RELATION | — |

---

### Task (standard object — extended)

> **Purpose:** Internal action item (Twenty built-in object). Extended with Leo agent-specific fields. The `agentAdvice` field is auto-populated by Leo based on task type and context — it contains prioritised guidance, talking points, and next steps.
>
> **App column key:** `Standard` = built into Twenty, no creation needed — only rename if label differs. `Custom` = must be created via Settings → Data Model or metadata API.

| Field | App | Type | Options | Description |
|-------|-----|------|---------|-------------|
| `title` | **Standard** | TEXT | — | Concise action title, e.g. "Prepare quotation for Acme" (Twenty built-in primary field) |
| `status` | **Standard** | SELECT | `TODO` / `IN_PROGRESS` / `DONE` | Task status (Twenty built-in) |
| `dueAt` | **Standard** | DATE_TIME | — | Task deadline (Twenty built-in) |
| `assignee` | **Standard** | RELATION | — | Workspace member this task is assigned to (Twenty built-in) |
| `body` | **Standard** | RICH_TEXT | — | Task body / detail (Twenty built-in) |
| `createdAt` | **Standard** | DATE_TIME | — | Record creation timestamp (Twenty built-in, system field) |
| `updatedAt` | **Standard** | DATE_TIME | — | Last update timestamp (Twenty built-in, system field) |
| `deletedAt` | **Standard** | DATE_TIME | — | Soft-delete timestamp (Twenty built-in, system field) |
| `createdBy` | **Standard** | ACTOR | — | Who created this record (Twenty built-in, system field) |
| `taskId` | Custom | TEXT | — | Human-readable ID, e.g. `TASK-2026-001` |
| `taskType` | Custom | SELECT | `PREPARE_QUOTATION` / `PREPARE_MOU` / `PREPARE_DEMO` / `FOLLOW_UP_CALL` / `PARTNER_ENABLEMENT` / `OTHER` | Task category — determines the type of agent advice Leo generates |
| `agentAdvice` | Custom | TEXT | — | Leo's auto-generated guidance: pricing notes, objection handling, checklist, talking points. Editable by the task owner before execution. |
| `outputLink` | Custom | LINKS | — | Link to the deliverable produced by this task (quotation PDF, deck, document) |

**Relations (Twenty built-in):**
- `taskTargets → linked to any object (Account, Contact, Deal, Partnership, etc.) via Twenty's polymorphic task target system

---

### Partnership (custom object)

> **Purpose:** Partner relationship lifecycle. Tracks from first contact to signed agreement to active co-selling. One partnership = one partner company for one relationship scope.

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `name` | TEXT *(auto)* | — | Partnership name, e.g. "Acme Systems - GeoKernel Reseller" |
| `partnershipId` | TEXT | — | Human-readable ID, e.g. `PART-2026-001` |
| `stage` | SELECT | `PROSPECT` / `QUALIFYING` / `AGREEMENT` / `ACTIVE` / `ON_HOLD` / `INACTIVE` | Partnership lifecycle stage |
| `currentStatusSummary` | TEXT | — | Narrative status: why at this stage, blockers, enablement gaps |
| `targetCloseDate` | DATE_TIME | — | Expected date for contract signature |
| `description` | TEXT | — | Partnership context: commission structure, territory, terms background |

**Relations:**
- `account` → Account (the partner company, many-to-one)
- `primaryContact` → Contact (decision maker at the partner)
- `engagements` → Engagement
- `contracts` → Contract
- `notes` → Note (Twenty built-in)
- `tasks` → Task (Twenty built-in)

---

### Engagement (custom object)

> **Purpose:** Interaction audit trail. Every meaningful touchpoint with a customer or partner gets logged here. Links to Account, Contact, Deal, and/or Partnership.

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `name` | TEXT *(auto)* | — | Engagement title / summary, e.g. "Discovery call with CTO" |
| `engagementId` | TEXT | — | Human-readable ID, e.g. `ENG-2026-001` |
| `status` | SELECT | `PLANNED` / `COMPLETED` | Whether the interaction has occurred or is upcoming |
| `engagementType` | SELECT | `PHONE_CALL` / `IN_PERSON_VISIT` / `ONLINE_MEETING` / `WHATSAPP_LINE` / `DEMO` / `MESSAGE` / `EMAIL` / `EVENT` | Type of interaction channel |
| `date` | DATE_TIME | — | When the interaction occurred or is scheduled |
| `notes` | TEXT | — | What happened: outcomes, decisions made, sentiment, key discussion points |
| `nextAction` | TEXT | — | The single most important next step from this interaction |

**Relations:**
- `account` → Account (always linked)
- `contact` → Contact (who we spoke to)
- `deal` → Deal (which deal this touches, optional)
- `partnership` → Partnership (which partnership this touches, optional)
- `notes` → Note (Twenty built-in)
- `tasks` → Task (Twenty built-in)

---

### Quotation (custom object)

> **Purpose:** Pricing quotation document. Issued to a client as part of a deal. Contains header info; line items live in QuotationItem.

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `name` | TEXT *(auto)* | — | Quotation name, e.g. "Q-2026-001 Acme GeoKernel" |
| `quotationId` | TEXT | — | Human-readable ID, e.g. `Q-2026-001` |
| `status` | SELECT | `DRAFT` / `SENT` / `ACCEPTED` / `REJECTED` / `EXPIRED` | Current state of this quotation |
| `totalAmount` | CURRENCY | — | Grand total (sum of all line items) |
| `quotationCurrency` | SELECT | `USD` / `HKD` / `TWD` / `MYR` / `OMR` | Currency for this quotation |
| `validUntil` | DATE_TIME | — | Expiry date — quotation is no longer valid after this date |
| `docLink` | LINKS | — | Link to the actual quotation document (PDF or cloud doc) |
| `notes` | TEXT | — | Internal notes about this quotation |

**Relations:**
- `deal` → Deal (the deal this quotation belongs to, many-to-one)
- `items` → QuotationItem (line items)
- `notes` → Note (Twenty built-in)
- `tasks` → Task (Twenty built-in)

---

### QuotationItem (custom object)

> **Purpose:** Individual line item within a quotation. Each item represents one product, service, or fee.

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `name` | TEXT *(auto)* | — | Item name / product name |
| `itemName` | TEXT | — | Display name for the line item (may differ from object name) |
| `description` | TEXT | — | Detailed description of the item, scope, or deliverable |
| `quantity` | NUMBER | — | Quantity of units |
| `unitPrice` | CURRENCY | — | Price per unit |
| `totalPrice` | CURRENCY | — | Line total (quantity × unit price) |

**Relations:**
- `quotation` → Quotation (parent quotation, many-to-one)

---

### Contract (custom object)

> **Purpose:** Signed agreement. Created after a quotation is accepted (for non-BusyCow products) or directly for partnership agreements. Links to either a Deal or a Partnership.

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `name` | TEXT *(auto)* | — | Contract name, e.g. "MSA - Acme GeoKernel 2026" |
| `contractId` | TEXT | — | Human-readable ID, e.g. `CON-2026-001` |
| `status` | SELECT | `DRAFT` / `UNDER_REVIEW` / `SIGNED` / `EXPIRED` / `TERMINATED` | Current state of this contract |
| `signedDate` | DATE_TIME | — | Date all parties signed |
| `expiryDate` | DATE_TIME | — | Date the contract expires or is up for renewal |
| `totalValue` | CURRENCY | — | Total contract value over the full term |
| `docLink` | LINKS | — | Link to the signed contract document |
| `notes` | TEXT | — | Internal notes, key terms summary, renewal flags |

**Relations:**
- `client` → Account (the counterparty — client or partner company)
- `deal` → Deal (if this contract is for a sales deal, optional)
- `partnership` → Partnership (if this contract is for a partnership agreement, optional)
- `notes` → Note (Twenty built-in)
- `tasks` → Task (Twenty built-in)

---

## Relations Map

```
Account ──< Contact             (account has many contacts)
Account ──< Deal                (account has many deals)
Account ──< Partnership         (account has many partnership records)
Account ──< Engagement          (account has many interactions)
Account ──< Contract            (account has many contracts as client)

Contact ──< Engagement           (contact appears in many interactions)
Contact ──  Partnership          (contact is primary contact on a partnership)

Deal ──< Engagement      (deal has many interactions)
Deal ──< Quotation       (deal has many quotations)
Deal ──< Contract        (deal has one or more contracts)
Deal ──< Note            (Twenty built-in)
Deal ──< Task            (Twenty built-in)

Partnership ──< Engagement      (partnership has many interactions)
Partnership ──< Contract        (partnership has one or more contracts)
Partnership ──< Note            (Twenty built-in)
Partnership ──< Task            (Twenty built-in)

Quotation ──< QuotationItem     (quotation has many line items)
```

---

## Reserved Field Names (cannot create as custom fields)

`currency`, `name`, `id`, `createdAt`, `updatedAt`, `deletedAt`, `position`, `type`

> **Workarounds used:**
> - `currency` → use `quotationCurrency`
> - `type` → use `engagementType`
> - `position` → already built into Twenty objects as a system field

---

## Changelog

| Date | Change |
|------|--------|
| 2026-06-11 | Full rewrite — aligned to live Twenty instance. Added Partnership, Engagement, Contract objects. Extended Account, Contact, Deal, Task. Added field types, options, and descriptions throughout. Renamed `description` → `overview` on Account (bio vs enrichment distinction). Removed `businessLine` from shared schema (product-specific, not universal). Added Note and Task conventions. |
| 2026-06-11 | Renamed standard objects to business terms: Company → Account, Person → Contact, Opportunity → Deal. Partnership added as core object alongside the four. |
