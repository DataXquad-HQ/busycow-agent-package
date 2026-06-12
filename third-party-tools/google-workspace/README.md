# Google Workspace

Connects Hermes agents to Gmail, Google Calendar, Drive, Sheets, and Docs via
the `gws` CLI (Google's official Rust tool) with an OAuth2 bridge.

## What agents can do

| Service | Operations |
|---------|-----------|
| **Gmail** | Search, read, compose, send, reply, forward, label |
| **Google Calendar** | Read events, create meetings, check availability |
| **Google Drive** | Search, upload, download, move files and folders |
| **Google Sheets** | Read/write cells, format, create sheets, run formulas |
| **Google Docs** | Read content, write sections, create documents |

## Architecture

```
Agent → google_api.py → gws_bridge.py → gws CLI → Google APIs
        (argparse)       (token refresh)   (Rust)
```

- `setup.py` — one-time OAuth2 authorization (headless, works over SSH)
- `gws_bridge.py` — refreshes the OAuth token and injects it into `gws`
- `google_api.py` — backward-compatible CLI wrapper

## Setup

### 1. Create Google Cloud credentials

1. Go to https://console.cloud.google.com → APIs & Services → Credentials
2. Create an OAuth2 client ID (Desktop application type)
3. Download as `google_client_secret.json`
4. Place at: `~/.hermes/skills/core/google-workspace/scripts/google_client_secret.json`

### 2. Install gws CLI

```bash
npm install -g @googleworkspace/cli
# or:  cargo install google-workspace-cli
gws --version
```

### 3. Authorize

```bash
python3 ~/.hermes/skills/core/google-workspace/scripts/setup.py
# Opens a URL — paste into browser, grant permissions
# Saves token to google_token.json
```

### 4. Load the skill

The `google-workspace` skill should already be in `~/.hermes/skills/core/`.
Verify: `hermes skills list | grep google`

## Skill location (shared)

`../shared-skills/google-workspace/` — full skill with all scripts and references

## Docs

https://github.com/NousResearch/hermes-agent
