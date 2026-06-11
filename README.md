# BusyCow Playbooks

Production-grade AI agent skills, schemas, and setup guides — built for the
[Hermes Agent](https://hermes-agent.nousresearch.com) stack.

This repo is the **canonical reference for duplicating a BusyCow-powered
agent team** on any fresh VM. Every directory has its own `README.md` that
explains what lives there and in what order to install things.

---

## Repository Structure

```
busycow-playbooks/
├── structural-data/      ← Shared schemas (CRM objects, DB definitions) — read by all agents
├── contextual-knowledge/ ← Shared background knowledge docs
├── core/                 ← Hermes install, identity templates, core skills
├── third-party-tools/    ← Self-hosted tools (Twenty CRM, Ghost, etc.)
├── shared-skills/        ← Hermes skills available to every agent profile
└── agent-teams/          ← Per-agent configs, capabilities, agent-specific skills
```

---

## Layer Responsibilities

| Layer | Who reads it | What it contains |
|-------|-------------|-----------------|
| `structural-data/` | All agents | CRM schemas, DB table/field definitions |
| `contextual-knowledge/` | All agents | Background docs — company, products, team |
| `core/` | Installer / all agents | Hermes setup, identity templates, core skills |
| `third-party-tools/` | Installer / maintainer | Docker-based tool installs with SETUP.md |
| `shared-skills/` | All agents | Hermes `.md` skills — one copy, used by everyone |
| `agent-teams/` | Per-agent | SOUL.md, CAPABILITY.md, agent-specific skills |

---

## Installation Order

```
Phase 0  (human, manual)
  └── VM + Hermes install
  └── Lark / Feishu bot app created

Phase 1  (agent-automated)
  └── core/SETUP.md             ← Hermes config, GBrain init, Lark MCP
  └── third-party-tools/*/SETUP.md  ← install each self-hosted service

Phase 2  (shared layer)
  └── shared-skills/            ← copy skills into ~/.hermes/skills/

Phase 3  (per agent)
  └── agent-teams/<agent>/SETUP.md
```

---

## Stack

| Layer | Tool |
|-------|------|
| Agent runtime | Hermes Agent |
| Workspace | Lark / Feishu |
| Knowledge graph | GBrain |
| CRM | Twenty (self-hosted) |
| External comms | Google Workspace |

---

## Access Convention (important)

All agent code must address internal services by **localhost** or the
VM's internal address — never Tailscale IPs or Cloudflare tunnel URLs.
Those external addresses are for human browser access only.

```
✅  http://localhost:3001    (Twenty CRM — agent code)
❌  http://100.x.x.x:3001   (Tailscale — browser only)
❌  https://crm.example.com  (Cloudflare tunnel — browser only)
```
