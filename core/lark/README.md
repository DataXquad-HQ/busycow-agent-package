# Lark / Feishu

[Lark](https://www.larksuite.com) (international) / [Feishu](https://www.feishu.cn) (mainland China)
is the team workspace that powers human ↔ agent communication and structured data storage.

## Roles in the stack

| Feature | How we use it |
|---------|--------------|
| **IM / Chat** | Primary interface between humans and agents — agents receive and send messages here |
| **Bitable (Base)** | Relational database for operational data — task tracker, CRM (pre-Twenty), financials |
| **Docs (Docx)** | Internal document creation — meeting notes, SOPs, reports |
| **Calendar** | Meeting tracking and scheduling |
| **Bot App** | How Hermes connects to Lark — a registered app with API credentials |

## Two integration modes

### lark-cli (command-line, default)

The `lark-cli` tool wraps the Lark OpenAPI. Used by agents for all Bitable,
Docs, IM, and Calendar operations.

```bash
hermes setup lark        # configure lark-cli in Hermes
lark-cli auth login      # authenticate (user or bot token)
```

**Strict mode (user token):** Since June 2026, we use `--as user` for Bitable
and document operations so files are owned by the user, not the bot.

### Lark MCP server (for direct tool access)

Some Lark operations are exposed as MCP tools directly in the Hermes tool loop
via the `lark-mcp` integration.

```bash
# Installed via: hermes setup lark
# Configured in: ~/.hermes/config.yaml under mcp_servers
```

## Required App permissions

When creating a Lark bot app in the Dev Console, enable:

- `im:message` — send and receive messages
- `bitable:app` — read/write Bitable
- `docx:document` — read/write Docs
- `contact:user.id:readonly` — resolve user IDs
- `calendar:calendar` — calendar access (optional)

## Setup

```bash
hermes setup lark
# Prompts for App ID, App Secret, and bot webhook URL
```

Verify: send a message to the Lark bot and confirm it replies.

## Docs

https://open.larksuite.com/document/home/index
