# Leo — BD Director Agent Context

## Overview

This document defines everything Leo needs to operate — data sources, GBrain configuration, and documents the human operator must provide before Leo can function effectively.

---

## 1. Structured Data Sources (Lark Base)

Leo reads from and writes to the following Lark Base tables. All table IDs are defined in `SCHEMA.md`.

| Table | Purpose | Leo's Access |
|-------|---------|-------------|
| Accounts | Company records — clients, prospects, partners | Read + Write |
| Contacts | People records — linked to Accounts | Read + Write |
| Deals | Active sales opportunities | Read + Write |
| Partnerships | Partner relationships in progression | Read + Write |
| Engagements | All customer/partner interactions | Read + Write |
| Tasks | Follow-up actions with Agent Advice | Read + Write |
| Quotations | Pricing documents | Read + Write |
| Invoices | Billing documents | Read |
| Contracts | Signed agreements | Read |

**Required before setup:**
- Create a Lark Base app (Sales & Ops)
- Create all 9 tables following `SCHEMA.md`
- Record the App Token and all Table IDs
- Set `{{LARK_APP_TOKEN}}` and all `{{TABLE_ID_*}}` placeholders in skills

---

## 2. GBrain Configuration

Leo maintains a knowledge graph in GBrain alongside the Lark Base CRM. Every Account, Contact, and Engagement logged in Lark Base is automatically reflected in GBrain.

### Page Types Leo Creates and Maintains

| GBrain Page Type | Slug Pattern | Created When |
|-----------------|-------------|-------------|
| Company | `companies/{kebab-name}` | New Account added to CRM |
| Person | `people/{kebab-full-name}` | New Contact added to CRM |
| Deal narrative | (timeline entries on company page) | Engagement logged |

### GBrain Operations Leo Runs Automatically

| Operation | Trigger | Tool |
|-----------|---------|------|
| Create company page | New Account created | `mcp_gbrain_put_page` |
| Create person page | New Contact created | `mcp_gbrain_put_page` |
| Add timeline entry | Engagement logged | `mcp_gbrain_add_timeline_entry` |
| Extract facts | Engagement notes saved | `mcp_gbrain_extract_facts` |
| Update recent insights | Negative outcome or key blocker detected | `mcp_gbrain_put_page` |

**Required before setup:**
- GBrain instance running and accessible
- `gbrain status` returns healthy
- Leo's Hermes profile has GBrain MCP configured

---

## 3. Documents the Operator Must Provide

These documents are not created by Leo — they must be prepared by the human operator and referenced in the relevant skills.

| Document | Purpose | Where to Reference |
|----------|---------|-------------------|
| Pricing Tier Table | Defines Standard / Professional / Enterprise tiers and price ranges | Update `generating-quotations` skill with your pricing |
| Quotation Template | Lark Doc template for quotation PDFs | Set `{{GOOGLE_DOC_TEMPLATE_ID}}` or Lark Doc token in `generating-quotations` |
| Invoice Template | Lark Doc template for invoice PDFs | Set template token in `generating-invoices` |
| Company Product Descriptions | What each product/service does, key features, use cases | Add to GBrain under `products/{product-slug}` |
| Approved Objection Handling | Common objections and approved rebuttals per product | Add to GBrain under `sales/objection-handling` |
| Partner Commission Structure | Commission rates and tiers for each partner type | Add to GBrain under `partnerships/commission-structure` |

**Optional but recommended:**
| Document | Purpose |
|----------|---------|
| Competitor Comparison | How your product compares to key competitors | Improves Agent Advice quality in quotations |
| Case Studies / References | Customer success stories | Used in meeting-prep and proposal generation |
| Ideal Customer Profile (ICP) | Target company size, industry, geography, pain points | Improves lead triage recommendations |

---

## 4. External Integrations

| Integration | Purpose | Status |
|-------------|---------|--------|
| Tavily API | Web search for account enrichment | Required — set `TAVILY_API_KEY` |
| Lark IM | Deliver briefs, alerts, and draft batches | Auto-configured via Hermes Lark setup |
| Lark Docs / Drive | Store quotation and proposal PDFs | Required for `generating-quotations` |
| Content Engine (Lark Base) | Published articles for nurture messages | Optional — wire in when ready |

---

## 5. Cron Job Schedule

Leo runs the following automated jobs. All jobs must be created as part of `SETUP.md` Step 4.

| Job Name | Schedule | → Skill | Notes |
|----------|----------|---------|-------|
| daily-deal-health-check | Daily 07:00 local | reviewing-sales-pipeline | Stall detection |
| daily-partnership-health-check | Daily 07:00 local | reviewing-partnership-pipeline | Silence detection |
| daily-briefing | Daily 08:00 local | daily-briefing | Morning summary |
| meeting-prep-daily | Daily 09:00 local | meeting-prep | Silent if no meeting tomorrow |
| account-enrichment-monthly | 1st of month 20:00 local | enriching-leads | Re-enrichment |
| lead-nurturing-monthly | 1st of month 09:00 local | lead-nurturing | Cold contact outreach batch |
