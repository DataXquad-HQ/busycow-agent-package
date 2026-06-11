# Environment Variables & API Keys

## Design

Each Hermes profile has **two layers** of env configuration:

```
~/.hermes/shared.env                ← shared keys (one copy, all profiles read)
~/.hermes/.env                      ← default profile keys (model API + overrides)
~/.hermes/profiles/leo/.env         ← Leo's keys (model API + profile-specific)
~/.hermes/profiles/maya/.env        ← Maya's keys
~/.hermes/profiles/quinn/.env       ← Quinn's keys
~/.hermes/profiles/rex/.env         ← Rex's keys
~/.hermes/profiles/steve/.env       ← Steve's keys
```

**Why not symlink everything to one file?**
Each profile has its own model API keys (Anthropic, Gemini, OpenRouter etc.)
so we can track costs per agent. Shared infrastructure keys (Lark, Tavily, Ghost…)
live in `shared.env` and are synced into each profile — no duplication, no manual
copy-paste when a key changes.

---

## What goes where

### `shared.env` — infrastructure keys shared by all agents

Keys that have nothing to do with which model an agent uses.
One update here → run `sync-shared-env.sh` → all profiles updated.

| Key | What it's for |
|-----|--------------|
| `FEISHU_APP_ID` | Lark bot app credentials |
| `FEISHU_APP_SECRET` | Lark bot app credentials |
| `FEISHU_DOMAIN` | Lark workspace domain |
| `FEISHU_CONNECTION_MODE` | Lark connection mode |
| `FEISHU_GROUP_POLICY` | Lark group access policy |
| `FEISHU_ALLOW_ALL_USERS` | Lark user access policy |
| `LARK_CLI_WORKSPACE` | lark-cli default workspace |
| `TAVILY_API_KEY` | Web search (shared across all agents) |
| `TELEGRAM_BOT_TOKEN` | Telegram gateway |
| `TELEGRAM_ALLOWED_USERS` | Telegram access list |
| `GHOST_URL` | Ghost blog endpoint |
| `GHOST_ADMIN_API_KEY` | Ghost admin API (Maya uses this) |
| `GITHUB_TOKEN` | GitHub access (repo push, etc.) |
| `NOTION_API_KEY` | Notion read access |

### Each profile's `.env` — model keys + profile-specific config

Keys that are intentionally different per agent for cost tracking
or per-profile functionality.

| Key | Why per-profile |
|-----|----------------|
| `ANTHROPIC_API_KEY` | Cost tracking per agent |
| `OPENROUTER_API_KEY` | Cost tracking per agent |
| `GOOGLE_GENERATIVE_AI_API_KEY` | Cost tracking per agent |
| `FEISHU_HOME_CHANNEL` | Each agent has its own Lark channel |
| `FEISHU_HOME_CHANNEL_THREAD_ID` | Each agent's home thread |
| `FEISHU_BOT_OPEN_ID` | Each bot has a different Open ID |
| `FEISHU_ALLOWED_USERS` | Per-profile access control |
| Any agent-specific runtime config | e.g. `BRAND_TONE`, `CONTENT_LANGUAGE` |

---

## Syncing shared keys

When you add or update a key in `shared.env`:

```bash
bash ~/.hermes/sync-shared-env.sh
```

This adds missing keys to every profile's `.env`.
It **never overwrites** keys already present in a profile.

Sync specific profiles only:

```bash
bash ~/.hermes/sync-shared-env.sh leo maya
```

The script lives at `~/.hermes/sync-shared-env.sh`.
A copy is kept in this repo at `core/hermes/sync-shared-env.sh`.

---

## Adding a new key

**Shared key (same value for all agents):**
1. Add to `~/.hermes/shared.env`
2. Run `bash ~/.hermes/sync-shared-env.sh`
3. Update the table above in this file

**Per-profile key (different per agent):**
1. Add to each profile's `.env` manually
2. Update the table above in this file

---

## Setting up a new profile

```bash
# 1. Create the profile
hermes profile create <name>

# 2. Add model API keys to the new profile's .env
echo "ANTHROPIC_API_KEY=sk-..." >> ~/.hermes/profiles/<name>/.env

# 3. Sync all shared keys in
bash ~/.hermes/sync-shared-env.sh <name>
```

---

## Security

- All `.env` and `shared.env` files are `chmod 600` (owner read/write only)
- `shared.env` and `.env` files are **never committed to git**
- Only this documentation file and the sync script are in the repo
- The `.env.example` files use `{{PLACEHOLDER}}` — fill in locally, never push real values
