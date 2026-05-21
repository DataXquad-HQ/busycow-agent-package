---
name: organizing-google-drive
description: >
  Use when user asks to organize, restructure, or clean up a Google Drive —
  shared or personal. Covers folder naming philosophy, hybrid By-Type + By-BL
  structure, client folder pattern, and Drive API execution via Python.
triggers:
  - "整理 Drive"
  - "organize drive"
  - "restructure drive"
  - "folder structure"
  - "drive 命名"
version: "1.0"
author: BusyCow
---

# Organizing Google Drive

## Phase 0 — Scan First

Always scan before proposing. Never propose a structure without seeing what's actually there.

```python
import sys, os, json, urllib.request, urllib.parse
sys.path.insert(0, f"{os.environ.get('HERMES_HOME', os.path.expanduser('~/.hermes'))}/skills/productivity/google-workspace/scripts")
from gws_bridge import get_valid_token

token = get_valid_token()
DRIVE_ID = "YOUR_SHARED_DRIVE_ID"  # from URL: drive.google.com/drive/folders/DRIVE_ID

def list_folder(folder_id):
    params = {
        "driveId": DRIVE_ID, "includeItemsFromAllDrives": "true",
        "supportsAllDrives": "true", "corpora": "drive",
        "q": f"'{folder_id}' in parents",
        "fields": "files(id,name,mimeType,parents)", "pageSize": "100", "orderBy": "name"
    }
    # CRITICAL: use urllib.parse.urlencode — do NOT string-interpolate params with spaces
    # into the URL directly, causes InvalidURL control character error
    base = "https://www.googleapis.com/drive/v3/files?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(base, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read()).get("files", [])
```

For personal Drive, omit `driveId`, `corpora`, set `q = "'root' in parents"`.

Drill 3 levels deep before proposing structure.

---

## Phase 1 — Diagnose

Look for:
- Scattered files at root level (should be in folders)
- Duplicate/copy files (Copy of X, X 的副本)
- Client execution data mixed with marketing materials
- Templates in wrong BL folder (should be in shared Ops folder)
- Inconsistent naming (some numbered, some not, some bracketed)
- Dev/working directories mixed with business content

---

## Phase 2 — Propose Structure

### BusyCow Canonical Structure (confirmed 2026-05)

```
📁 [DX] Clients/          ← All client execution docs, cross-BL
    CLIENT_NAME/
      BusyCow/            ← BL-specific work for this client
      [Product]/
📁 [DX] Company/          ← Company-level: pitch, legal, brand
📁 [DX] Operations/       ← Cross-BL finance & shared tools
    Invoices/             ← All BLs' actual invoices
    Quotations/           ← All BLs' actual quotations
    Templates/            ← Shared doc templates (invoice, quote)
    Contracts/
📁 [DX] Projects/         ← Time-bounded projects, all BLs
    [BusyCow] Project Name 2026/
    [[Product]] Project Name/
📁 BusyCow/               ← BL-specific working content
    00_Inbox/
    01_Core/
    02_Sales & Marketing/
    03_Commercial/
    99_Archived/
📁 [Product]/             ← Same structure
📁 Distify/               ← Same structure
```

### Key Principles

**1. Naming convention — two-layer system:**
- Root level: `[DX]` prefix for company-level folders → visually float to top, signal "shared"
- BL level: numbered `00_` / `99_` for forced sort order
- Pure BL names (BusyCow, [Product]) for product lines — no prefix needed

**2. Numbering within BL folders:**
| Number | Purpose |
|--------|---------|
| `00_Inbox` | Temporary drop zone — always exists, sinks to bottom of "top" |
| `01_Core` | Brand identity, core product docs |
| `02_Sales & Marketing` | Decks, demos, videos, website assets |
| `03_Commercial` | Reseller agreements, partner contracts |
| `04_...` | Optional additional category |
| `99_Archived` | Old/deprecated, not deleted |

**3. Client folders — always in `[DX] Clients/`, never in BL:**
- Reason: you find clients by name, not by BL
- Structure: `[DX] Clients/CLIENT/BL_NAME/` for BL-specific execution files
- Same client can have multiple BL subfolders if they work across lines

**4. Projects — always in `[DX] Projects/`, never in BL:**
- Reason: you find projects by name/topic, not by BL
- Naming: `[BL_NAME] Project Name YYYY` — BL context in the name, not the folder path
- Projects often span BLs anyway

**5. By-Type vs By-BL — use hybrid:**
- Finance/Ops things (invoices, quotations, templates) → By-Type in `[DX] Operations/`
- Working content (demos, decks, agreements) → By-BL
- Rationale: Finance team finds by type; product team finds by BL

**6. Templates vs actual documents:**
- Templates (the master doc with `{{placeholders}}`) → `[DX] Operations/Templates/`
- Actual quotations/invoices sent to clients → `[DX] Operations/Quotations/` or `Invoices/`
- Skills reference templates by Google Doc ID — moving files doesn't break them

**7. "Could another client use this?" test for Sales materials:**
- Yes → `BL/02_Sales & Marketing/` (generic deck)
- No → `[DX] Clients/CLIENT/BL/` (client-specific)

---

## Phase 3 — Execute via API

### Collect all IDs first (save to /tmp)

```python
def build_id_map(folder_id, prefix="", depth=2):
    id_map = {}
    for f in list_folder(folder_id):
        key = f"{prefix}/{f['name']}" if prefix else f["name"]
        id_map[key] = f["id"]
        if "folder" in f["mimeType"] and depth > 0:
            id_map.update(build_id_map(f["id"], key, depth-1))
    return id_map

ids = build_id_map(DRIVE_ID)
with open("/tmp/drive_id_map.json", "w") as f:
    json.dump(ids, f, ensure_ascii=False, indent=2)
```

### Core operations

```python
def gapi(method, path, body=None, params_dict=None):
    base = f"https://www.googleapis.com/drive/v3/{path}"
    if params_dict:
        base += "?" + urllib.parse.urlencode(params_dict)
    data = json.dumps(body).encode() if body else None
    headers = {"Authorization": f"Bearer {token}"}
    if body: headers["Content-Type"] = "application/json"
    req = urllib.request.Request(base, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "msg": e.read().decode()[:300]}

def create_folder(name, parent_id):
    r = gapi("POST", "files", {
        "name": name, "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id]
    }, {"supportsAllDrives": "true"})
    return r["id"]

def rename(file_id, new_name):
    return gapi("PATCH", f"files/{file_id}", {"name": new_name},
                {"supportsAllDrives": "true"})

def move(file_id, new_parent_id, old_parent_id):
    # CRITICAL: Shared Drive items must have exactly one parent at all times
    # addParents + removeParents in a single call — never add without removing
    return gapi("PATCH", f"files/{file_id}", {}, {
        "addParents": new_parent_id, "removeParents": old_parent_id,
        "supportsAllDrives": "true", "fields": "id,name"
    })
```

### Execution order

1. Rename root folders first (no moves needed)
2. Create new folder structure (save new IDs to `/tmp/drive_new_ids.json`)
3. Move files/folders — always move contents before removing empty shells
4. Rename numbered folders last (after structure is settled)
5. Verify with a final tree scan

---

## Pitfalls

- **`urllib.parse.urlencode` is mandatory** — never f-string params with spaces into URL directly → `InvalidURL: URL can't contain control characters`
- **Shared Drive: one parent only** — `addParents` + `removeParents` must be in same PATCH call. Moving an empty shell that already moved its contents causes `teamDrivesParentLimit` 403. Just leave empty shells in place or archive them.
- **File ID never changes on move** — skills/tools that reference files by ID are unaffected by reorganization
- **Never delete during reorganization** — move to `99_Archived` instead. Confirm with user before any deletion.
- **Propose plan, confirm, then execute** — never reorganize without showing the before/after first
- **Get Shared Drive ID from URL** — `drive.google.com/drive/folders/DRIVE_ID` — the DRIVE_ID is also the root folder ID for listing
