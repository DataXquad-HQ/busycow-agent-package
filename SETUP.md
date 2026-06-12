# Core Setup

## What this creates

- Hermes Agent configured with Lark MCP + GBrain
- Core identity files written: `SOUL.md`, `MEMORY.md`, `USER.md`
- Skills Registry Base created in Lark

## Prerequisites (human, manual)

- [ ] VM running Linux (Ubuntu 22.04+ recommended)
- [ ] `hermes` CLI installed — see https://hermes-agent.nousresearch.com/docs
- [ ] Lark / Feishu workspace with a bot app created in the Dev Console
- [ ] Lark app permissions enabled: messenger, bitable, docx, contact
- [ ] Tavily API key (for web search)

## Steps

### 1. Hermes initial setup

```bash
hermes setup
```

Fill in SOUL.md from `templates/SOUL.md` as a starting point.
Fill in MEMORY.md from `templates/MEMORY.md`.
Fill in USER.md from `templates/USER.md`.

### 2. Lark MCP

```bash
hermes setup lark
# Follow prompts: Lark App ID, App Secret, bot webhook URL
```

Verify: send a message to the Lark bot and confirm it replies.

### 3. GBrain

```bash
hermes setup gbrain
gbrain init
```

### 4. Verify

```bash
hermes skills list    # should show default skills
hermes health         # all green
```

## Next step

→ `../third-party-tools/twenty-crm/SETUP.md`


---

# Hermes Agent

[Hermes Agent](https://hermes-agent.nousresearch.com) is the AI agent runtime
that powers the entire BusyCow stack.

## What it does

- Runs a persistent agent loop connected to chat platforms (Lark, Telegram, etc.)
- Executes tools: file system, terminal, web search, MCP servers, memory
- Loads skills (SKILL.md files) that define reusable task procedures
- Runs scheduled cron jobs autonomously
- Maintains persistent memory across sessions

## Key concepts

| Concept | What it is |
|---------|-----------|
| **Profile** | A named agent identity with its own SOUL.md, MEMORY.md, skills, and cron jobs |
| **Skill** | A SKILL.md file that tells the agent how to do a specific task |
| **GBrain** | Knowledge graph plugin for long-term structured memory |
| **Cron** | Background jobs that run on a schedule without user interaction |

## Install

```bash
pip install hermes-agent
hermes setup
```

See the full setup guide: `../SETUP.md`

## Config location

```
~/.hermes/
├── config.yaml          ← main config (model, provider, tools)
├── SOUL.md              ← agent identity (role, style, values)
├── MEMORY.md            ← persistent session-level facts
├── USER.md              ← user profile facts
├── skills/              ← shared skill library
└── profiles/            ← per-agent profiles (leo/, maya/, etc.)
```

## Docs

https://hermes-agent.nousresearch.com/docs


---

# GBrain

GBrain is Hermes Agent's long-term knowledge graph — a local-first, self-hosted
structured memory layer. It stores entities, decisions, intel, and facts that
persist across sessions and can be queried by agents.

## What it stores

| Type | Examples |
|------|---------|
| **People** | Contacts, their roles, relationships, signals |
| **Companies** | Clients, partners, prospects — firmographic + relationship data |
| **Decisions** | Architectural choices, strategic calls — with rationale |
| **Takes** | Beliefs, bets, hunches — typed and weighted |
| **Facts** | Claims extracted from conversations |
| **Timelines** | Longitudinal history of any entity |

## Why it exists alongside Twenty CRM

- **Twenty CRM** → structured operational data (deals, pipeline, invoices, contacts)
- **GBrain** → rich knowledge graph (decisions, relationships, intel, patterns)

They overlap on contacts/companies but serve different query patterns.
Agents write to both — CRM for workflow state, GBrain for intelligence.

## Install

```bash
hermes setup gbrain
gbrain init              # initialises the local vault
gbrain sync              # syncs knowledge from the git-backed vault
```

## Config location

```
~/.hermes/gbrain/        ← vault root (git repo)
    pages/               ← markdown knowledge pages
    config.yaml          ← GBrain settings
```

## Key operations for agents

```python
# Write a page
mcp_gbrain_put_page(slug="companies/acme", content="...")

# Query
mcp_gbrain_query(query="who knows about water infrastructure")

# Extract facts from conversation
mcp_gbrain_extract_facts(turn_text="...")

# Add timeline entry
mcp_gbrain_add_timeline_entry(slug="companies/acme", date="2026-06-11", summary="...")
```

## Docs

https://hermes-agent.nousresearch.com/docs/gbrain
