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
