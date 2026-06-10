# Sales Playbook — Setup Guide

> **This file is agent-executable.** A Leo agent can read and follow these steps to install the full sales pipeline setup on a new workspace.

## What This Setup Creates

- Lark Base CRM (9 tables: Accounts, Contacts, Deals, Partnerships, Engagements, Tasks, Quotations, Invoices, Contracts)
- GBrain auto-sync conventions (every Account, Contact, and Engagement reflected in GBrain)
- Leo skills installed: capturing-sales-intel, engagement-logging, deal-progressing, meeting-prep, lead-nurturing, reviewing-sales-pipeline, reviewing-partnership-pipeline, daily-briefing, account-onboarding, managing-sales-pipeline, managing-partnership-pipeline, generating-quotations, generating-invoices, deal-advisory, follow-up-email, enriching-leads
- 6 cron jobs wired to their skills

---

## Prerequisites

Before running this setup:
- [ ] Hermes Agent installed and running
- [ ] Lark/Feishu workspace configured (`hermes setup lark`)
- [ ] GBrain running and accessible (`gbrain status`)
- [ ] Tavily API key set (`hermes config set search.tavily_api_key YOUR_KEY`)
- [ ] Leo profile created (`hermes profile create leo`)

---

## Step 1 — Create the Lark Base CRM

### 1a. Create a new Bitable app in Lark
- Go to Lark → New Document → Bitable
- Name it: **Sales & Ops**
- Copy the App Token from the URL: `https://[domain].larksuite.com/base/{{LARK_APP_TOKEN}}`

### 1b. Create tables in this order (DuplexLinks require both tables to exist first)

Create each table with its primary field:

```
1. Accounts        — Primary: "Company Name" (Text)
2. Contacts        — Primary: "Full Name" (Text)
3. Deals           — Primary: "Deal Name" (Text)
4. Partnerships    — Primary: "Partner Name" (Text)
5. Engagements     — Primary: "Title" (Text)
6. Tasks           — Primary: "Title" (Text)
7. Quotations      — Primary: "Quotation ID" (Text)
8. Invoices        — Primary: "Invoice ID" (Text)
9. Contracts       — Primary: "Contract Name" (Text)
```

### 1c. Add all fields per table

Follow `SCHEMA.md` for the full field list of each table. Add fields in the order listed. Create DuplexLink fields last.

### 1d. Record all table IDs

After creating each table, copy its ID from the URL and note them:

```
ACCOUNTS_TABLE_ID=tbl...
CONTACTS_TABLE_ID=tbl...
DEALS_TABLE_ID=tbl...
PARTNERSHIPS_TABLE_ID=tbl...
ENGAGEMENTS_TABLE_ID=tbl...
TASKS_TABLE_ID=tbl...
QUOTATIONS_TABLE_ID=tbl...
INVOICES_TABLE_ID=tbl...
CONTRACTS_TABLE_ID=tbl...
```

---

## Step 2 — Install Leo Skills

### 2a. Download all skills from this repo

```bash
SKILLS_BASE="https://raw.githubusercontent.com/DataXquad-HQ/busycow-playbooks/main/playbooks/sales/skills"
LEO_SKILLS="~/.hermes/profiles/leo/skills/sales"

mkdir -p $LEO_SKILLS

for skill in \
  capturing-sales-intel \
  account-onboarding \
  enriching-leads \
  engagement-logging \
  deal-progressing \
  meeting-prep \
  deal-advisory \
  follow-up-email \
  managing-sales-pipeline \
  managing-partnership-pipeline \
  reviewing-sales-pipeline \
  reviewing-partnership-pipeline \
  daily-briefing \
  lead-nurturing \
  generating-quotations \
  generating-invoices; do
  mkdir -p "$LEO_SKILLS/$skill"
  curl -s "$SKILLS_BASE/$skill.md" -o "$LEO_SKILLS/$skill/SKILL.md"
  echo "✅ $skill"
done
```

### 2b. Update table IDs in all skills

Replace all `{{TABLE_ID_*}}` placeholders with your actual table IDs from Step 1d:

```bash
cd ~/.hermes/profiles/leo/skills/sales

# Replace app token
find . -name "SKILL.md" -exec sed -i 's/{{LARK_APP_TOKEN}}/YOUR_APP_TOKEN/g' {} +

# Replace each table ID
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_ACCOUNTS}}/YOUR_ACCOUNTS_TABLE_ID/g' {} +
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_CONTACTS}}/YOUR_CONTACTS_TABLE_ID/g' {} +
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_DEALS}}/YOUR_DEALS_TABLE_ID/g' {} +
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_PARTNERSHIPS}}/YOUR_PARTNERSHIPS_TABLE_ID/g' {} +
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_ENGAGEMENTS}}/YOUR_ENGAGEMENTS_TABLE_ID/g' {} +
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_TASKS}}/YOUR_TASKS_TABLE_ID/g' {} +
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_QUOTATIONS}}/YOUR_QUOTATIONS_TABLE_ID/g' {} +
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_INVOICES}}/YOUR_INVOICES_TABLE_ID/g' {} +
find . -name "SKILL.md" -exec sed -i 's/{{TABLE_ID_CONTRACTS}}/YOUR_CONTRACTS_TABLE_ID/g' {} +
echo "✅ All placeholders replaced"
```

---

## Step 3 — Install Leo SOUL.md

```bash
SOUL_URL="https://raw.githubusercontent.com/DataXquad-HQ/busycow-playbooks/main/playbooks/agents/profiles/leo/SOUL.md"
curl -s "$SOUL_URL" -o ~/.hermes/profiles/leo/SOUL.md
echo "✅ SOUL.md installed"
```

Edit `~/.hermes/profiles/leo/SOUL.md` to fill in:
- `{{COMPANY_NAME}}` — your company name
- `{{PRODUCT_LINES}}` — your product lines
- `{{OWNER_NAME}}` — the sales rep name
- `{{ESCALATION_CONTACT}}` — who Leo escalates to for contract/pricing decisions

---

## Step 4 — Set Up Cron Jobs

Create the following cron jobs. Each cron triggers a skill — the skill holds all logic.

```bash
# Daily deal health check (07:00 local = adjust UTC offset for your timezone)
hermes cron create \
  --name "daily-deal-health-check" \
  --schedule "0 23 * * *" \
  --skills "reviewing-sales-pipeline,lark-base" \
  --prompt "Execute reviewing-sales-pipeline skill, Mode B (full scan): scan all active deals, detect stalls (7+ days no engagement), flag At Risk. Silent if all healthy."

# Daily partnership health check
hermes cron create \
  --name "daily-partnership-health-check" \
  --schedule "0 23 * * *" \
  --skills "reviewing-partnership-pipeline,lark-base" \
  --prompt "Execute reviewing-partnership-pipeline skill, Mode B (full scan): scan all active partnerships, detect silence (14+ days), create re-engagement tasks. Silent if all healthy."

# Daily morning briefing (08:00 local)
hermes cron create \
  --name "daily-briefing" \
  --schedule "0 0 * * *" \
  --skills "daily-briefing,lark-base" \
  --prompt "Execute daily-briefing skill: compile at-risk deals and tasks due today into morning summary. Deliver to sales rep."

# Pre-meeting brief (09:00 local)
hermes cron create \
  --name "meeting-prep-daily" \
  --schedule "0 1 * * *" \
  --skills "meeting-prep,lark-base" \
  --prompt "Execute meeting-prep skill, Mode B (tomorrow scan): scan for Planned Engagements happening tomorrow. Generate brief for each. Silent if none found."

# Monthly account enrichment (1st of month, 20:00 local)
hermes cron create \
  --name "account-enrichment-monthly" \
  --schedule "0 12 1 * *" \
  --skills "enriching-leads,lark-base" \
  --prompt "Execute enriching-leads skill, batch mode: re-enrich all active accounts not enriched in the last 30 days."

# Monthly lead nurturing (1st of month, 09:00 local)
hermes cron create \
  --name "lead-nurturing-monthly" \
  --schedule "0 1 1 * *" \
  --skills "lead-nurturing,lark-base" \
  --prompt "Execute lead-nurturing skill, Mode B (monthly scan): find contacts with no active Deal or Partnership and no engagement in 30+ days. Generate personalised nurture draft batch for sales rep review."
```

> **Note on timezones:** Cron schedules above use UTC. Adjust the hour to match your local timezone (e.g. UTC+8 Taiwan: subtract 8 hours).

---

## Step 5 — Verify Installation

Run these checks after setup:

```bash
# 1. Check skills are loaded
hermes skills list --profile leo | grep -E "engagement-logging|deal-progressing|meeting-prep|lead-nurturing"

# 2. Check cron jobs are registered
hermes cron list --profile leo

# 3. Test CRM connection (run a pipeline review)
hermes run --profile leo "幫我看一下 pipeline 狀況"

# 4. Test a new lead intake
hermes run --profile leo "新 lead 進來了，公司叫做 Test Corp，在台灣，科技業"

# 5. Check GBrain is syncing
gbrain search "Test Corp"
```

Expected results:
- [ ] Skills list shows all 16 sales skills
- [ ] Cron list shows 6 jobs, all enabled
- [ ] Pipeline review returns structured output (or "no active deals" if CRM is empty)
- [ ] New lead creates both a Lark Base record AND a GBrain page
- [ ] GBrain search finds the new company page

---

## Step 6 — First Run

Once verified, onboard your first real lead:

```
Tell Leo: "認識了 [Company Name] 的 [Contact Name]，他是 [Title]，在 [Event/Channel] 認識的"
```

Leo will:
1. Ask clarifying questions to fill required fields
2. Create Account + Contact in Lark Base
3. Create GBrain pages for both
4. Run enrichment on the company
5. Recommend first action

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Skill says `{{TABLE_ID}}` in error | Run Step 2b to replace all placeholders |
| GBrain page not created after new Account | Check `capturing-sales-intel` skill Phase 5 — ensure `mcp_gbrain_put_page` is being called |
| Cron job runs but no output | Check skill is returning content — it may be silent (no at-risk deals, no planned meetings) |
| Engagement logged but no Task created | Check `engagement-logging` Step 4 — Task creation requires a clear Next Action in the engagement |
| Meeting brief not sent day before | Check Planned Engagement `Date` field is set correctly and `Status = Planned` |

---

## Next Steps

After the base sales pipeline is running:

1. **Add quotation templates** — set up Lark Docs templates for your product lines and update `generating-quotations` skill with template IDs
2. **Connect Content Engine** — when your content Lark Base is ready, update `lead-nurturing` skill with the table token to enable article-based nurturing
3. **Build C6 Partner Success** — create `partner-monthly-scorecard` skill for monthly partner health checks
4. **Add GBrain knowledge pages** — run `account-onboarding` for your existing key accounts to populate the knowledge graph

---

## Files in This Playbook

```
playbooks/sales/
├── SETUP.md          ← this file
├── SCHEMA.md         ← full table/field definitions
└── skills/
    ├── capturing-sales-intel.md
    ├── account-onboarding.md
    ├── enriching-leads.md
    ├── engagement-logging.md
    ├── deal-progressing.md
    ├── meeting-prep.md
    ├── deal-advisory.md
    ├── follow-up-email.md
    ├── managing-sales-pipeline.md
    ├── managing-partnership-pipeline.md
    ├── reviewing-sales-pipeline.md
    ├── reviewing-partnership-pipeline.md
    ├── daily-briefing.md
    ├── lead-nurturing.md
    ├── generating-quotations.md
    └── generating-invoices.md
```
