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
