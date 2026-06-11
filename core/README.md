# Core

Platform-level integrations and infrastructure that Hermes Agent depends on.
Every deployment installs this layer first before adding third-party tools or agent teams.

---

## Stack Overview

| Tool | Type | Purpose | Location |
|------|------|---------|----------|
| Hermes Agent | Runtime | AI agent loop, tool execution, cron jobs | `hermes/` |
| Lark / Feishu | Chat platform | Agent ↔ human interface, Bitable DBs, Docs | `lark/` |
| GBrain | Knowledge graph | Long-term memory — entities, decisions, intel | `gbrain/` |
| Tavily | Web search API | Real-time web search for agents | `tavily/` |
| Google Workspace | External suite | Email (Gmail), Calendar, Drive, Sheets, Docs | `google-workspace/` |
| Cloudflare Tunnels | Networking | Expose self-hosted tools via public domain, no open ports | `cloudflare-tunnels/` |

**Third-party tools with their own UI and Docker containers** →
see `../third-party-tools/` (Twenty CRM, Ghost)

---

## Install Order

```
1. hermes/        → Hermes Agent + Lark MCP + GBrain init
2. lark/          → lark-cli auth + Bitable permissions
3. gbrain/        → GBrain vault init
4. tavily/        → set Tavily API key
5. google-workspace/ → OAuth2 setup
6. cloudflare-tunnels/ → expose third-party tool UIs after they're running
```

---

## What "Core" means here

Core tools are configured **via CLI or config file** and integrate directly into the
Hermes Agent process. They don't run as separate Docker containers with their own UIs
(that's `../third-party-tools/`).

Exception: Cloudflare Tunnels runs as a `systemd` service but it's networking
infrastructure — not a product tool — so it lives here.
