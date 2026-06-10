# Agent Playbooks

Each subdirectory is a self-contained agent — everything needed to install, configure, and run that agent on a new workspace.

## Available Agents

| Agent | Role | Status |
|-------|------|--------|
| [leo](./leo/) | BD Director — pipeline progression, account intelligence, partner management | ✅ Active |

## Structure

Every agent directory follows the same structure:

```
agents/<name>/
├── CAPABILITY.md   ← What the agent does (C1–CN), authority grid, funnel position
├── SOUL.md         ← Agent identity, operating principles, tone, escalation rules
├── CONTEXT.md      ← Data sources, GBrain config, documents operator must provide
├── SCHEMA.md       ← CRM / database schema the agent reads and writes
├── SETUP.md        ← Step-by-step install guide (agent-executable)
├── TOOLS.md        ← All tools the agent uses, access by capability, config checklist
└── skills/         ← All skills the agent uses
    ├── skill-name.md
    └── ...
```

## Reading Order for a New Install

1. `CAPABILITY.md` — understand what the agent does and its authority boundaries
2. `CONTEXT.md` — identify what data sources and documents you need to prepare
3. `SCHEMA.md` — create the required database tables
4. `TOOLS.md` — configure all required tools
5. `SETUP.md` — run the full install

## Adding a New Agent

1. Create `agents/<name>/` directory
2. Follow the same 7-file structure above
3. Add the agent to this README table
