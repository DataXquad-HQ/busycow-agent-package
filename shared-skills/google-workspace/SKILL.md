---
name: google-workspace
description: >
  Use Gmail, Google Calendar, Drive, Sheets, and Docs via the gws CLI.
  Use when user asks to send an email, check calendar, read/write a Google Doc or Sheet,
  search Drive, or manage Google contacts. Requires gws binary and valid OAuth token.
version: 2.0.0
author: Nous Research
license: MIT
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials (downloaded from Google Cloud Console)
---

# Google Workspace

Gmail, Calendar, Drive, Contacts, Sheets, and Docs — powered by `gws` (Google's Rust CLI).

## Architecture

```
google_api.py  →  gws_bridge.py  →  gws CLI → Google APIs
(argparse)        (token refresh)   (Rust binary)
```

- `scripts/setup.py` — one-time OAuth2 authorization (headless-compatible)
- `scripts/gws_bridge.py` — refreshes OAuth token, injects into `gws`
- `scripts/google_api.py` — backward-compatible CLI wrapper

## Prerequisites

Install `gws`:

```bash
npm install -g @googleworkspace/cli
# or: cargo install google-workspace-cli
gws --version
```

## Setup (one-time)

1. Create OAuth2 credentials in Google Cloud Console:
   - APIs & Services → Credentials → Create OAuth2 Client ID (Desktop app)
   - Download JSON → save as `scripts/google_client_secret.json`

2. Run authorization:
```bash
python3 scripts/setup.py
# Opens a browser URL — authorize and paste the code back
```

3. Token saved to `google_token.json` — gws_bridge.py handles refresh from here.

## Google Sheets

### Read cells
```python
import subprocess, json

result = subprocess.run(
    ["python3", "scripts/google_api.py", "sheets", "read",
     "--spreadsheet-id", "{{SPREADSHEET_ID}}",
     "--range", "Sheet1!A1:Z100"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
```

### Write cells
```python
result = subprocess.run(
    ["python3", "scripts/google_api.py", "sheets", "write",
     "--spreadsheet-id", "{{SPREADSHEET_ID}}",
     "--range", "Sheet1!A1",
     "--values", json.dumps([["Header1", "Header2"], ["val1", "val2"]])],
    capture_output=True, text=True
)
```

### Batch update (formatting, merges, formulas)
Use the Sheets API `batchUpdate` directly via `gws_bridge` for complex operations.
See `references/sheets-formula-debugging.md` for merged-cell patterns.

## Gmail

### Search messages
```python
result = subprocess.run(
    ["python3", "scripts/google_api.py", "gmail", "search",
     "--query", "from:{{EMAIL}} is:unread",
     "--max-results", "10"],
    capture_output=True, text=True
)
```

### Send email
```python
result = subprocess.run(
    ["python3", "scripts/google_api.py", "gmail", "send",
     "--to", "{{RECIPIENT}}",
     "--subject", "{{SUBJECT}}",
     "--body", "{{BODY}}"],
    capture_output=True, text=True
)
```

See `references/gmail-search-syntax.md` for search operators.

## Google Drive

### Search files
```python
result = subprocess.run(
    ["python3", "scripts/google_api.py", "drive", "search",
     "--query", "name contains '{{FILENAME}}'",
     "--drive-id", "{{SHARED_DRIVE_ID}}"],  # omit for My Drive
    capture_output=True, text=True
)
```

### Download file
```python
result = subprocess.run(
    ["python3", "scripts/google_api.py", "drive", "download",
     "--file-id", "{{FILE_ID}}",
     "--output", "/tmp/output.pdf"],
    capture_output=True, text=True
)
```

### Share a file
```python
# Always share by explicit email — "anyone with link" does NOT grant API access
result = subprocess.run(
    ["python3", "scripts/google_api.py", "drive", "share",
     "--file-id", "{{FILE_ID}}",
     "--email", "{{COLLABORATOR_EMAIL}}",
     "--role", "writer"],  # or "reader"
    capture_output=True, text=True
)
```

## Google Docs

### Read document
```python
result = subprocess.run(
    ["python3", "scripts/google_api.py", "docs", "read",
     "--document-id", "{{DOC_ID}}"],
    capture_output=True, text=True
)
```

### Create document
```python
result = subprocess.run(
    ["python3", "scripts/google_api.py", "docs", "create",
     "--title", "{{TITLE}}",
     "--content", "{{BODY}}"],
    capture_output=True, text=True
)
```

## Running scripts via terminal (avoid execute_code)

The gws_bridge requires `$HOME` to be set. Always run via `terminal()`:

```python
# Write script to /tmp, then run via terminal
write_file('/tmp/gws_script.py', script_content)
terminal(command='HOME={{USER_HOME}} python3 /tmp/gws_script.py')
```

Do NOT use `execute_code` for Google API calls — the sandbox may not have `$HOME` set.

## Sheets formatting patterns (key rules)

- Always read `effectiveFormat` from reference rows, not `userEnteredFormat`
- **Unmerge cells BEFORE writing** — merged rows silently discard writes to non-anchor columns
- Correct order: `unmergeCells` → sleep 0.5s → write values → `mergeCells` + `repeatCell`
- Always explicitly set `backgroundColor` even for white — inherited fills from merged rows persist
- After `insertDimension`, recompute all row indices below the insertion point
- See `references/sheets-formula-debugging.md` for detailed patterns

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `403 Forbidden` on write | Wrong OAuth app used for Shared Drive | Use the app that owns the Drive |
| `404` on a shared Doc | "Anyone with link" doesn't grant API access | Owner must explicitly add OAuth email as collaborator |
| `get_valid_token()` raises `TypeError: can't compare offset-naive and offset-aware datetimes` | Naive datetime in token expiry | Call `refresh_token()` directly, bypass `get_valid_token()` |
| `ModuleNotFoundError: No module named 'gws_bridge'` in execute_code | Sandbox can't resolve skill path | Use `terminal()` with explicit `HOME` env var |
| `HOME` not set → `get_token_path()` fails | Sandbox strips env | Set `os.environ['HOME'] = '{{USER_HOME}}'` at script top |
