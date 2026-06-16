---
name: generating-quotations
description: >
  Generate a quotation PDF for a client from Lark Base data, upload to Lark Drive,
  and write the file link back to the Quotation record. Use when user says "出報價",
  "幫我出 quotation", "generate a quote for X", "報價給", or when a pipeline
  opportunity reaches pricing discussion. Supports multiple versions (QUO-2026-HKRFID-001, -002).
triggers:
  - "出報價"
  - "出 quotation"
  - "generate quote"
  - "幫我出報價單"
  - "quotation for"
  - "報價給"
  - "建報價"
  - "new quotation"
version: "3.0"
author: DataXquad
---

# Generating Quotations

## ⚠️ MANDATORY PRE-CHECKS (run BEFORE anything else)

### 1. Get Taiwan Current Date
**NEVER assume or guess today's date.** Always fetch it:
```python
result = terminal("TZ=Asia/Taipei date '+%Y-%m-%d'")
today_tw = result.strip()  # e.g. "2026-05-19"
```
Use this for `{{ISSUE_DATE}}`, `{{DUE_DATE}}`, and the `YYYY` in the Quotation ID. If terminal is unavailable:
```python
from datetime import datetime, timezone, timedelta
today_tw = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
```
**Do NOT use UTC or local server time. Taiwan = UTC+8.**

### 2. Determine Quotation ID
Format: `QUO-{YYYY}-{CLIENT_SHORTNAME}-{NNN}`
- `YYYY` = from the Taiwan date fetched above (never hardcode)
- `NNN` = query Quotation table first, filter by client + year, count existing, then +1

```python
# Sequence: per client per year, starting 001
records = mcp_lark_bitable_v1_appTableRecord_search(
    path={"app_token": "MtvNbgCHXaRAaUsWXsCjnekep2g", "table_id": "{{TABLE_ID}}"},
    data={"filter": {"conjunction": "and", "conditions": [
        {"field_name": "Quotation ID", "operator": "contains", "value": [f"QUO-{yyyy}-{shortname}"]}
    ]}}
)
next_nnn = len(records) + 1
quo_id = f"QUO-{yyyy}-{shortname}-{next_nnn:03d}"
```

---

## Position in Sales Flow
```
Opportunity (pipeline) → [THIS SKILL] → Quotation → Contract → Invoice
```

---

## Templates — 4 Options

| Template | Doc ID | Use When |
|----------|--------|----------|
| BusyCow EN (with T&C + signature) | `12mLc7uyGDyZfkr0n-HBfI8_sjgih11M2nNeI0slJBqI` | BusyCow product, English client, want legally binding on sign |
| BusyCow CH (with T&C + signature) | `1IwhlC21pqCrOr2rG8s1ZGuqR2YeJDZ14-6MfHCgLVMY` | BusyCow product, Chinese client, want legally binding on sign |
| DX General EN (no T&C) | `1gvJbwQXQ4jbkQ8BQOO0BRm5WGTX7VvRfVuMkWGqDyPM` | All other products/services, English, standard quote |
| DX General CH (no T&C) | `1dPHLGFGOwObhfgDbDzVJkc7AxvRmjbpl7awb29hR1lg` | All other products/services, Chinese, standard quote |

**Template selection logic:**
1. Is this BusyCow? → BC template. Otherwise → DX template.
2. Client language preference → EN or CH.
3. If unsure of language → ask. If unsure of product → default DX EN.

**BusyCow T&C templates** include Terms & Conditions and a signature block — the signed quotation IS the contract. Use these when a separate contract is not planned.

---

## Placeholders (same across all 4 templates)

| Placeholder | Source |
|-------------|--------|
| `{{ENTITY_NAME}}` | Entity mapping (see below) |
| `{{ENTITY_ADDRESS}}` | Entity mapping (see below) |
| `{{QUOTATION_NO}}` | Generated: `QUO-{YYYY}-{SHORTNAME}-{NNN}` |
| `{{ISSUE_DATE}}` | Taiwan date from mandatory pre-check — EN: "28 May 2026" / CH: "2026年5月28日" — **never AI-generated** |
| `{{DUE_DATE}}` | Issue Date + 30 days (default) |
| `{{CLIENT_NAME}}` | Contact person name from Lark Base |
| `{{CLIENT_COMPANY}}` | Client company full name |
| `{{CLIENT_COMPANY_ADDRESS}}` | Client address from Lark Base |
| `{{CLIENT_TITLE}}` | Contact person title (BC templates only — signature block) |
| `{{ITEM_DESC}}` | Line item description |
| `{{ITEM_QTY}}` | Quantity |
| `{{ITEM_PRICE}}` | Unit price (formatted with commas) |
| `{{ITEM_AMOUNT}}` | Line total |
| `{{SUBTOTAL}}` | Sum of all items |
| `{{TAX}}` | Tax amount (empty string `""` if 0) |
| `{{TOTAL}}` | Grand total |
| `{{CURRENCY}}` | `HKD` / `USD` |

---

## Entity Mapping

| Client / Product | Entity | `{{ENTITY_NAME}}` | `{{ENTITY_ADDRESS}}` |
|-----------------|--------|-------------------|---------------------|
| Overseas client (HK, SG, MY) | SG | DATAXQUAD PTE. LTD. | 108 Punggol Walk #07-20 Twin Waterfalls, Singapore 828764 |
| Taiwan client | TW | ATA LIMITED 應科聯有限公司 | Rm. 202, I-Hub, No. 100, Wenhua Rd., Xitun Dist., Taichung City, Taiwan 407 |
| GeoKernel / TRACI product | TW | ATA LIMITED 應科聯有限公司 | same as above |
| BusyCow / AquaOptima product | SG | DATAXQUAD PTE. LTD. | same as above |

---

## Base & Tables
- **App Token:** `MtvNbgCHXaRAaUsWXsCjnekep2g`
- **Quotation table:** `{{TABLE_ID}}`
- **Quotation Items table:** `{{TABLE_ID}}`

### Quotation Items Schema

| Field | Field ID | Type |
|-------|----------|------|
| Item Name (primary) | `{{FIELD_ID}}` | Text |
| Description | `{{FIELD_ID}}` | Text |
| Qty | `{{FIELD_ID}}` | Number |
| Unit | `{{FIELD_ID}}` | Text |
| Unit Price | `{{FIELD_ID}}` | Number |
| Amount | `{{FIELD_ID}}` | Number |
| Notes | `{{FIELD_ID}}` | Text |
| Quotation (link) | `{{FIELD_ID}}` | DuplexLink → Quotation table |

Items are linked to the Quotation via `{{FIELD_ID}}` (DuplexLink). Always pull items by filtering on this field using the Quotation record ID.
- **Clients table:** `{{TABLE_ID}}`
- **Contacts table:** `{{TABLE_ID}}`
- **PDF Upload Folder:** Google Drive — `1s-6R4hzfCWiNokkXq74KpHZXtzEHouaF`

---

## Quotation ID Format
```
QUO-{YYYY}-{CLIENT_SHORTNAME}-{NNN}
```
- `QUO` = quotation (not `ORD`)
- NNN = sequential per client per year, starting 001
- Multiple versions for same opportunity: -001, -002, -003
- To get next NNN: search Quotation table, filter by Client, count existing for that client+year

---

## Quotation Table Fields

| Field | Field ID | Type |
|-------|----------|------|
| Quotation ID | `{{FIELD_ID}}` | Text (primary) |
| Client | `{{FIELD_ID}}` | Text |
| Issue Date | `{{FIELD_ID}}` | DateTime (ms) |
| Valid Until | `{{FIELD_ID}}` | DateTime (ms) |
| Currency | `{{FIELD_ID}}` | SingleSelect: HKD / NTD / USD |
| Subtotal | `{{FIELD_ID}}` | Number |
| Tax | `{{FIELD_ID}}` | Number |
| Total | `{{FIELD_ID}}` | Number |
| Status | `{{FIELD_ID}}` | SingleSelect: Draft / Sent / Accepted / Revised / Rejected |
| Related Opportunity | `{{FIELD_ID}}` | DuplexLink → Opportunity |
| Doc Link | `{{FIELD_ID}}` | Url |
| Notes | `{{FIELD_ID}}` | Text |
| Owner | `{{FIELD_ID}}` | Text |

---

## Step 0: Collect Context + Pull Items from Base

Before touching any API, collect:

```
MUST HAVE:
□ Quotation record ID (or Quotation ID string to look up)
□ Language (EN or CH) → determines template
□ Owner (Hunter or Kevin)

SHOULD HAVE:
□ Related Opportunity ID
□ Notes / special conditions override
```

### Pull line items from Quotation Items table

Once you have the Quotation record ID, fetch all linked items:

```python
# Search Quotation Items — filter by linked Quotation record ID
items = mcp_lark_bitable_v1_appTableRecord_search(
    path={"app_token": "MtvNbgCHXaRAaUsWXsCjnekep2g", "table_id": "{{TABLE_ID}}"},
    data={"filter": {"conjunction": "and", "conditions": [
        {"field_name": "Quotation", "operator": "contains", "value": [quotation_record_id]}
    ]}}
)
line_items = [
    {
        "name":        r["fields"].get("Item Name", ""),
        "description": r["fields"].get("Description", ""),
        "qty":         r["fields"].get("Qty", 1),
        "unit":        r["fields"].get("Unit", ""),
        "unit_price":  r["fields"].get("Unit Price", 0),
        "amount":      r["fields"].get("Amount", 0),
        "notes":       r["fields"].get("Notes", ""),
    }
    for r in items.get("items", [])
]
```

Also pull Quotation header from `{{TABLE_ID}}` for: client, currency, subtotal, tax, total.

Confirm to user before proceeding: "找到 N 個項目，小計 HKD XX,XXX。確認？"

If no items found in table → ask user to provide items manually.

---

## Step 1: Pull Client Data from Lark Base

```python
# Search Clients table for company info
# Search Contacts table for contact person + title + address
# Use mcp_lark_bitable_v1_appTableRecord_search with filter on Client Name
```

Fill in any gaps from the conversation if Base records are incomplete.

---

## Step 2: Create Quotation Record in Base

```python
from datetime import datetime, timezone, timedelta

today_ms = int(datetime.now(timezone.utc).replace(
    hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
valid_ms = today_ms + (30 * 24 * 60 * 60 * 1000)

fields = {
    "Quotation ID": "QUO-2026-{SHORTNAME}-{NNN}",
    "Client": "{CLIENT_SHORT_NAME}",
    "Issue Date": today_ms,
    "Valid Until": valid_ms,
    "Currency": "HKD",
    "Subtotal": subtotal,
    "Tax": 0,
    "Total": subtotal,
    "Status": "Draft",
    "Related Opportunity": opportunity_id,  # if exists
    "Owner": "Hunter",
}
# → mcp_lark_bitable_v1_appTableRecord_create
# → save returned record_id as QUO_RECORD_ID
```

---

## Step 3: Generate PDF from Google Docs Template

### Python workflow

```python
HERMES_HOME = os.environ.get('HERMES_HOME', os.path.expanduser('~/.hermes'))
SKILL_DIR = f"{HERMES_HOME}/skills/productivity/google-workspace"
PYTHON_BIN = f"{HERMES_HOME}/hermes-agent/venv/bin/python"
GBRIDGE = f"{PYTHON_BIN} {SKILL_DIR}/scripts/gws_bridge.py"

# 1. Select template
TEMPLATE_ID = "12mLc7uyGDyZfkr0n-HBfI8_sjgih11M2nNeI0slJBqI"  # one of the 4 above

# 2. Copy template → new doc
r = terminal(f"{GBRIDGE} drive files copy --params "
    f"'{{\"fileId\": \"{TEMPLATE_ID}\", \"name\": \"{quo_id} | {client_name}\", \"fields\": \"id\"}}'")
new_doc_id = json.loads(r)['id']

# 3. Build replacements dict
replacements = {
    '{{ENTITY_NAME}}':           entity_name,
    '{{ENTITY_ADDRESS}}':        entity_address,
    '{{QUOTATION_NO}}':          quo_id,
    '{{ISSUE_DATE}}':            issue_date_str,   # "28 May 2026" or "2026年5月28日"
    '{{DUE_DATE}}':              valid_until_str,
    '{{CLIENT_NAME}}':           client_contact_name,
    '{{CLIENT_COMPANY}}':        client_company_full,
    '{{CLIENT_COMPANY_ADDRESS}}': client_address,
    '{{CLIENT_TITLE}}':          client_title,     # BC templates only
    '{{SUBTOTAL}}':              f"{subtotal:,.0f}",
    '{{TAX}}':                   f"{tax:,.0f}" if tax else "",
    '{{TOTAL}}':                 f"{total:,.0f}",
    '{{CURRENCY}}':              currency,
}

# 4. Handle line items — template has ONE {{ITEM_*}} row
# For N items: insert N-1 rows first, then fill each row
# Single item: just replaceAllText directly

# 5. Build batchUpdate requests
requests_list = [
    {'replaceAllText': {
        'containsText': {'text': k, 'matchCase': True},
        'replaceText': v
    }} for k, v in replacements.items()
]
params = json.dumps({'documentId': new_doc_id, 'requests': requests_list})
terminal(f"{GBRIDGE} docs documents batchUpdate --params '{params}'")

# 6. Export PDF
terminal(f"curl -s -L -H 'Authorization: Bearer TOKEN' "
    f"'https://www.googleapis.com/drive/v3/files/{new_doc_id}/export?mimeType=application/pdf' "
    f"-o /tmp/{quo_id}.pdf")
```

### Date formatting by language
- EN templates: `"28 May 2026"`
- CH templates: `"2026年5月28日"`

### Multi-item handling
Template has ONE `{{ITEM_DESC}}` row. For multiple items:
1. Use Docs API `insertTableRow` to add N-1 rows after the template row
2. Fill each row's placeholders using `replaceAllText` with row-specific unique markers
   (e.g. `{{ITEM_DESC_1}}`, `{{ITEM_DESC_2}}`) — requires modifying the inserted rows first

---

## Step 4: Upload PDF to Google Drive

```python
# Google Drive folder for Quotations
QUOTATION_FOLDER_ID = "1s-6R4hzfCWiNokkXq74KpHZXtzEHouaF"

filepath = f'/tmp/{quo_id}.pdf'
filename = f'{quo_id}_{client_short}.pdf'

token_data = json.loads(open(f"{HERMES_HOME}/google_token.json").read())
access_token = token_data['token']

with open(filepath, 'rb') as f:
    pdf_data = f.read()

metadata = json.dumps({"name": filename, "parents": [QUOTATION_FOLDER_ID]}).encode()
boundary = "DXUploadBoundary"
body = (
    f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()
    + metadata
    + f'\r\n--{boundary}\r\nContent-Type: application/pdf\r\n\r\n'.encode()
    + pdf_data
    + f'\r\n--{boundary}--'.encode()
)
req = urllib.request.Request(
    'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
    data=body,
    headers={'Authorization': f'Bearer {access_token}',
             'Content-Type': f'multipart/related; boundary={boundary}'},
    method='POST')
result = json.loads(urllib.request.urlopen(req, timeout=30).read())
file_id = result['id']
file_url = f'https://drive.google.com/file/d/{file_id}/view'
```

---

## Step 5: Update Base Record with PDF Link

```python
# PUT (not PATCH — PATCH returns 404 on Lark Bitable)
mcp_lark_bitable_v1_appTableRecord_update(
    path={"app_token": "MtvNbgCHXaRAaUsWXsCjnekep2g",
          "table_id": "{{TABLE_ID}}",
          "record_id": QUO_RECORD_ID},
    data={"fields": {
        "Doc Link": {"link": file_url, "text": f"{quo_id} PDF"},
        "Status": "Draft"
    }}
)
```

---

## Step 6: Update Opportunity Stage (if linked)

```python
# Update Opportunity record: Stage → "Proposal"
# mcp_lark_bitable_v1_appTableRecord_update on {{TABLE_ID}}
```

---

## Step 7: Confirm to User

```
✅ 報價單已產出：
- QUO ID: QUO-2026-HKRFID-002
- 範本: BusyCow CH（含條款）
- Client: Hong Kong RFID Limited / Richard Chan
- 金額: HKD 85,000
- Valid until: 2026年6月27日
- PDF: [link]
- 已上傳至 Google Drive + Base 已更新

下一步：確認內容後說「Mark QUO-2026-HKRFID-002 as Sent」。
```

---

## Versioning (Multiple Revisions)

1. Do NOT overwrite existing quotation — create new record with NNN +1
2. Update old record Status → "Revised"
3. New record Status → "Draft"

---

## Status Flow
```
Draft → Sent → Accepted → [trigger generating-invoices]
              ↘ Revised  → [create new version]
              ↘ Rejected → [update Opportunity stage: Re-negotiate / Lost]
```

When Accepted:
- Update Opportunity Stage → "Closed Won"
- Prompt: "要直接出 Invoice 嗎？還是先建合約記錄？"

---

## Pitfalls
- Template selection: BusyCow templates have T&C + signature block — use only for BusyCow product
- `{{CLIENT_TITLE}}` appears in BC templates only (signature block) — leave empty for DX templates
- Multi-item: need insertTableRow before replaceAllText — single item is simpler
- Date format differs: EN = "28 May 2026", CH = "2026年5月28日"
- **Date must always be fetched via terminal (`TZ=Asia/Taipei date`) — never assumed or AI-generated**
- **Invoice/Quotation ID YYYYMM/YYYY must come from the fetched Taiwan date — never hardcoded**
- PDF upload: Google Drive multipart upload to folder `1s-6R4hzfCWiNokkXq74KpHZXtzEHouaF`
- Record update: PUT not PATCH (PATCH returns 404)
- Auth: use busycow profile app (`cli_a97aab1888f8de17`) for Lark Base API
- OAuth for Google: needs full `drive` + `documents` scopes (not readonly)
- Check existing QUO records before assigning NNN to avoid duplicates
