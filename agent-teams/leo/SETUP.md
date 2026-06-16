# Leo — Agent Setup

Step-by-step guide to get Leo operational from scratch. Complete these in order — each step is a prerequisite for the next.

---

## Overview

Leo requires the following before the agent can run:

| # | What | Type | Est. time |
|---|---|---|---|
| 1 | Hermes Agent + core infrastructure | Self-hosted | 30 min |
| 2 | Twenty CRM | Self-hosted | 20 min |
| 3 | Hindsight | Self-hosted | 15 min |
| 4 | OpenMail inbox | Cloud (SaaS) | 5 min |
| 5 | GitHub SSH access | Cloud (SaaS) | 10 min |
| 6 | Tavily API key | Cloud (API) | 5 min |
| 7 | Anthropic API key | Cloud (API) | 5 min |
| 8 | Leo profile + credentials | Configuration | 15 min |
| 9 | Skills installation | Configuration | 10 min |
| 10 | Cron jobs | Configuration | 10 min |
| 11 | Memory seeding | Content | 30 min |

**Total: ~2.5 hours**

---

## Step 1 — Core Infrastructure

Complete the core stack setup first:

→ `../../SETUP.md`

This installs Hermes Agent, GBrain, and wires up your communication platform (Lark or equivalent).

---

## Step 2 — Twenty CRM

Leo's primary data store. All pipeline objects live here.

→ `../../third-party-tools/twenty-crm/SETUP.md`

After setup, record:

```
TWENTY_API_KEY=<jwt token from Settings → API & Webhooks>
CRM_EXTERNAL_URL=https://crm.{{YOUR_DOMAIN}}   # public URL for human-facing links
```

---

## Step 3 — Hindsight

Leo's contextual memory layer. Must be running before any cron jobs execute.

**Install:**

```bash
# Clone and start Hindsight
git clone https://github.com/{{HINDSIGHT_REPO}} /your/install/path
cd /your/install/path
docker compose up -d

# Verify
curl -sf http://localhost:8888/health && echo "UP"
```

**Create Leo's memory banks:**

```bash
# Create all required banks
for bank in pipeline global agent-leo internal human-sales-rep human-manager; do
  curl -s -X POST http://localhost:8888/v1/default/banks \
    -H "Content-Type: application/json" \
    -d "{\"id\": \"{{ORG_PREFIX}}-${bank}\", \"name\": \"${bank}\"}"
  echo "Created: {{ORG_PREFIX}}-${bank}"
done
```

Replace `{{ORG_PREFIX}}` with your organisation's short prefix (e.g. `acme`).

**Banks created:**

| Bank | Purpose |
|---|---|
| `{{ORG_PREFIX}}-pipeline` | Per-opportunity context — primary bank for C5/C6 |
| `{{ORG_PREFIX}}-global` | Company-level facts approved across the team |
| `{{ORG_PREFIX}}-agent-leo` | Leo's private working memory |
| `{{ORG_PREFIX}}-internal` | Cross-agent handoffs |
| `{{ORG_PREFIX}}-human-sales-rep` | Sales Rep's priorities (read-only for Leo) |
| `{{ORG_PREFIX}}-human-manager` | Manager's priorities (read-only for Leo) |

---

## Step 4 — OpenMail

Leo's dedicated outbound/inbound email inbox.

1. Sign up at [openmail.sh](https://openmail.sh)
2. Create an inbox — name it `leo` or similar
3. Set the email address (e.g. `leo@{{YOUR_DOMAIN}}.openmail.sh` or a custom domain)
4. Copy the API token and inbox ID from the dashboard

Record:

```
OPENMAIL_API_KEY=<your api token>
OPENMAIL_INBOX_ID=<your inbox id>
AGENT_EMAIL=<leo's email address>
```

---

## Step 5 — GitHub SSH Access

Leo reads the internal wiki and agent package repos via SSH. The SSH key is configured once per VM and shared across all agents on that machine.

```bash
# Generate key (skip if one already exists at ~/.ssh/github_agents)
ssh-keygen -t ed25519 -C "agents@{{YOUR_DOMAIN}}" -f ~/.ssh/github_agents

# Add to SSH config
cat >> ~/.ssh/config << 'EOF'
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/github_agents
  IdentitiesOnly yes
EOF

# Print public key — add this to GitHub Settings → SSH and GPG keys
cat ~/.ssh/github_agents.pub

# Verify
ssh -T git@github.com
# Expected: Hi <username>! You've successfully authenticated...
```

Clone the repos Leo needs:

```bash
git clone git@github.com:{{YOUR_ORG}}/{{INTERNAL_WIKI_REPO}}.git /your/path/{{INTERNAL_WIKI_REPO}}
git clone git@github.com:{{YOUR_ORG}}/{{AGENT_PACKAGE_REPO}}.git /your/path/{{AGENT_PACKAGE_REPO}}
```

---

## Step 6 — Tavily API Key

Leo uses Tavily for web search in enrichment and scouting skills.

1. Sign up at [app.tavily.com](https://app.tavily.com)
2. Go to Dashboard → API Keys → Create key
3. Record:

```
TAVILY_API_KEY=*** api key>
```

This goes into Leo's `.env`. Hermes will route all `web_search` calls through Tavily automatically when this key is present.

---

## Step 7 — Anthropic API Key

Leo uses Claude as its reasoning model via Hermes.

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an API key
3. Record:

```
ANTHROPIC_API_KEY=<your api key>
```

This goes into the Hermes global `.env`, not Leo's profile `.env`.

---

## Step 8 — Create Leo's Profile

```bash
# Create the Leo profile in Hermes
hermes profile create leo

# This creates: ~/.hermes/profiles/leo/
```

**Write the SOUL.md:**

```bash
cp agent-teams/leo/SOUL.md ~/.hermes/profiles/leo/SOUL.md
```

Open the file and fill in all `{{PLACEHOLDER}}` values. See the full placeholder list below.

**Write Leo's `.env`:**

```bash
cat > ~/.hermes/profiles/leo/.env << 'EOF'
TWENTY_API_KEY=*** here>
OPENMAIL_API_KEY=*** here>
OPENMAIL_INBOX_ID=<paste here>
AGENT_EMAIL=<paste here>
TAVILY_API_KEY=*** here>
EOF
```

**Configure Leo's `config.yaml`:**

Key settings to add/update in `~/.hermes/profiles/leo/config.yaml`:

```yaml
agent:
  name: Leo
  profile: leo

models:
  default: claude-sonnet-4   # or your preferred model

toolsets:
  enabled:
    - web
    - terminal
    - file
    - mcp
  # Do NOT enable: image_gen, spotify, computer_use
```

---

## Step 9 — Install Skills

```bash
# Copy all Leo skills into the profile
cp -r agent-teams/leo/skills/* ~/.hermes/profiles/leo/skills/

# Verify
hermes --profile leo skills list
```

After copying, search for any remaining `{{PLACEHOLDER}}` values in the skills and replace them:

```bash
grep -r "{{" ~/.hermes/profiles/leo/skills/ --include="*.md" -l
```

---

## Step 10 — Set Up Cron Jobs

Leo's cron jobs are defined in `agent-teams/leo/cron/jobs.json` as a reference template. They must be created manually via the Hermes CLI — the JSON file is not directly importable.

First, fill in the channel IDs. You need three Lark (or equivalent) channel IDs:

```
SALES_DAILY_UPDATE_CHANNEL_ID=<sales team daily channel>
OUTREACH_REVIEW_CHANNEL_ID=<channel for draft review notifications>
SYSTEM_BACKEND_CHANNEL_ID=<internal ops log channel>
```

Then create each job. Example for the Lead Nurturing Scanner:

```bash
hermes --profile leo cron create \
  --name "Lead Nurturing Scanner" \
  --schedule "0 1 * * *" \
  --skill nurturing-leads \
  --deliver "feishu:{{SYSTEM_BACKEND_CHANNEL_ID}}" \
  --toolsets "web,terminal,file" \
  --prompt "..."   # copy prompt from cron/jobs.json
```

Repeat for all 7 jobs in `cron/jobs.json`. See that file for the full prompt and schedule for each.

**Verify cron is working:**

```bash
hermes --profile leo cron list
# Should show all 7 jobs in 'scheduled' state
```

---

## Step 11 — Seed Memory

Before Leo can operate intelligently, it needs baseline context loaded into GBrain and Hindsight.

**GBrain — load wiki pages:**

Copy the templates from `wiki-setup/` and fill in your company's details, then load each into GBrain:

```bash
# For each file in wiki-setup/
gbrain capture --file wiki-setup/company-background.md --slug wiki/company-background
gbrain capture --file wiki-setup/product-overview.md   --slug wiki/products/{{PRODUCT_SLUG}}
gbrain capture --file wiki-setup/sales-strategy.md     --slug wiki/{{ORG_PREFIX}}-sales-strategy
gbrain capture --file wiki-setup/brand-messaging.md    --slug wiki/brand-messaging
gbrain capture --file wiki-setup/key-contacts.md       --slug wiki/key-contacts
```

**Hindsight — load Sales Rep context:**

Tell Hindsight about the Sales Rep so Leo can adapt its style:

```bash
curl -s -X POST http://localhost:8888/v1/default/banks/{{ORG_PREFIX}}-human-sales-rep/memories \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{
      "content": "{{SALES_REP_NAME}} — {{SALES_REP_ROLE}}. Communication style: {{COMMUNICATION_STYLE}}. Key priorities: {{PRIORITIES}}.",
      "tags": ["profile", "sales-rep"]
    }]
  }'
```

---

## Placeholder Reference

All values that must be replaced before Leo is operational:

| Placeholder | Where | What to put |
|---|---|---|
| `{{ORG_PREFIX}}` | SOUL.md, skills, .env | Short org identifier, e.g. `acme` |
| `{{COMPANY_NAME}}` | SOUL.md | Your company name |
| `{{YOUR_DOMAIN}}` | SETUP.md (SSH key) | Your company domain |
| `{{YOUR_ORG}}` | SETUP.md (git clone) | Your GitHub organisation name |
| `{{COMPANY_BLOG_URL}}` | cron/jobs.json | Your blog or news URL |
| `{{CRM_EXTERNAL_URL}}` | SOUL.md, skills | Public-facing CRM URL |
| `{{AGENT_EMAIL}}` | SOUL.md, skills, .env | Leo's OpenMail address |
| `{{OPENMAIL_TOKEN}}` | skills/openmail | Leo's OpenMail API token |
| `{{OPENMAIL_INBOX_ID}}` | skills/openmail, .env | Leo's inbox ID |
| `{{SALES_DAILY_UPDATE_CHANNEL_ID}}` | SOUL.md, cron | Sales team channel ID |
| `{{OUTREACH_REVIEW_CHANNEL_ID}}` | SOUL.md, cron | Draft review channel ID |
| `{{SYSTEM_BACKEND_CHANNEL_ID}}` | SOUL.md, cron | Ops log channel ID |
| `{{YOUR_PRODUCT_LINES}}` | context/schemas/crm.md | Your CRM businessLine enum values |
| `{{PRODUCT_SLUG}}` | SOUL.md, wiki-setup | GBrain slug for each product |
| `{{INTERNAL_WIKI_REPO}}` | skills/github-core-repos | Your internal wiki repo name |
| `{{AGENT_PACKAGE_REPO}}` | skills/github-core-repos | This repo's name |
| `{{PRODUCT_CORE_REPO}}` | skills/github-core-repos | Your product knowledge repo name |

---

## Verify Everything

```bash
# Profile is loaded
hermes --profile leo whoami

# Skills are visible
hermes --profile leo skills list | grep -E "twenty-crm|openmail|nurturing"

# Cron jobs scheduled
hermes --profile leo cron list

# CRM is reachable
curl -sf http://localhost:3001/healthz && echo "CRM UP"

# Hindsight is reachable
curl -sf http://localhost:8888/health && echo "HINDSIGHT UP"

# Test a live interaction — ask Leo to check the pipeline
hermes --profile leo chat "How many active opportunities are in the CRM right now?"
```

---

## Next Steps After Setup

1. **Ingest the sales strategy** — use the `ingesting-sales-strategy` skill to load your strategy document. This enables C6 pipeline health checks to run gap analysis.
2. **Enter first contacts** — use C1 Lead Capture to onboard your first prospects.
3. **Run inbox monitor manually** — trigger the `monitoring-inbox-replies` skill once to verify OpenMail integration end-to-end.
4. **Let the first cron fire** — watch the `{{SYSTEM_BACKEND_CHANNEL_ID}}` channel for the first ops log.
