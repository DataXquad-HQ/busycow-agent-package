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
