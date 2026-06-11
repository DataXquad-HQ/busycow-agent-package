# Google Docs Invoice Workflow

## Template IDs

| Template | Doc ID |
|----------|--------|
| EN | `1zQ4w3GbVDNTWzH2TCsxNjuRBxRpN93xVWNfO15MHQrQ` |
| CH | `1y1ZPn65MsUfaz1Cl9HiokH67YdxmOdh342mppY4qO68` |

Language selection: match client language / prior quotation language.

## PDF Storage
- Lark Drive Folder Token: `S9aTfSFeBlU9sIdz5LojcUgLpob`
- Filename: `{INVOICE_NO}_{CLIENT_SHORT}_{YYYYMM}.pdf`

## Entity Config
```python
ENTITIES = {
    'SG': {
        'name':             'DATAXQUAD PTE. LTD.',
        'address':          '108 Punggol Walk #07-20 Twin Waterfalls, Singapore 828764',
        'bank_name':        'DBS Bank',
        'bank_account_name':'DATAXQUAD PTE. LTD.',
        'bank_account_no':  '0721151979',
        'swift_code':       'DBSSSGSG',
    },
    'TW': {
        'name':             'ATA LIMITED 應科聯有限公司',
        'address':          'Rm. 202, I-Hub, No. 100, Wenhua Rd., Xitun Dist., Taichung City, Taiwan 407',
        'bank_name':        'Taipei Fubon Bank',
        'bank_account_name':'ATA LIMITED',
        'bank_account_no':  '83110000387935',
        'swift_code':       'TPBKTWTPXXX',
    },
}
```

## Placeholders (both EN and CH templates)
```
{{ENTITY_NAME}}         {{ENTITY_ADDRESS}}
{{INVOICE_NO}}          {{INVOICE_DATE}}        {{DUE_DATE}}
{{BILL_TO_NAME}}        {{BILL_TO_COMPANY}}     {{BILL_TO_ADDRESS}}
{{SHIP_TO_NAME}}        {{SHIP_TO_ADDRESS}}     ← empty string if no hardware
{{ITEM_DESC}}           {{ITEM_QTY}}            {{ITEM_PRICE}}    {{ITEM_AMOUNT}}
{{SUBTOTAL}}            {{TAX}}                 {{TOTAL}}         {{CURRENCY}}
{{BANK_NAME}}           {{BANK_ACCOUNT_NAME}}   {{BANK_ACCOUNT_NO}}  {{SWIFT_CODE}}
```

## Date Formatting
- EN: `"28 May 2026"`
- CH: `"2026年5月28日"`

## Step 1 — Copy Template
```python
HERMES_HOME = os.environ.get('HERMES_HOME', os.path.expanduser('~/.hermes'))
PYTHON_BIN = f"{HERMES_HOME}/hermes-agent/venv/bin/python"
# gws_bridge.py lives under core/, NOT productivity/
GBRIDGE = f"{PYTHON_BIN} ~/.hermes/skills/core/google-workspace/scripts/gws_bridge.py"
TEMPLATE_ID = '1zQ4w3GbVDNTWzH2TCsxNjuRBxRpN93xVWNfO15MHQrQ'  # or CH version

r = terminal(f"{GBRIDGE} drive files copy --params "
    f"'{{\"fileId\": \"{TEMPLATE_ID}\", \"name\": \"{invoice_no} | {client_name}\", \"fields\": \"id\"}}'")
new_doc_id = json.loads(r)['id']
```

## Step 2 — Replace Placeholders
```python
entity = ENTITIES['SG']  # or TW
replacements = {
    '{{ENTITY_NAME}}':         entity['name'],
    '{{ENTITY_ADDRESS}}':      entity['address'],
    '{{INVOICE_NO}}':          invoice_no,
    '{{INVOICE_DATE}}':        invoice_date_str,
    '{{DUE_DATE}}':            due_date_str,
    '{{BILL_TO_NAME}}':        bill_to_name,
    '{{BILL_TO_COMPANY}}':     bill_to_company,
    '{{BILL_TO_ADDRESS}}':     bill_to_address,
    '{{SHIP_TO_NAME}}':        ship_to_name or '',
    '{{SHIP_TO_ADDRESS}}':     ship_to_address or '',
    '{{SUBTOTAL}}':            f"{subtotal:,.0f}",
    '{{TAX}}':                 f"{tax:,.0f}" if tax else '',
    '{{TOTAL}}':               f"{total:,.0f}",
    '{{CURRENCY}}':            currency,
    '{{BANK_NAME}}':           entity['bank_name'],
    '{{BANK_ACCOUNT_NAME}}':   entity['bank_account_name'],
    '{{BANK_ACCOUNT_NO}}':     entity['bank_account_no'],
    '{{SWIFT_CODE}}':          entity['swift_code'],
}
requests_list = [
    {'replaceAllText': {'containsText': {'text': k, 'matchCase': True}, 'replaceText': v}}
    for k, v in replacements.items()
]
params = json.dumps({'documentId': new_doc_id})
body = json.dumps({'requests': requests_list})
# IMPORTANT: --params is for URL query params only (documentId goes here)
# --json carries the request body (requests array goes here)
# Do NOT combine them into --params — the API rejects arrays in query params
terminal(f"{GBRIDGE} docs documents batchUpdate --params '{params}' --json '{body}'")
```

## Step 3 — Line Items (multi-item)
Template has ONE `{{ITEM_DESC}}` row.
- Single item: replaceAllText handles it directly
- Multiple items: use `insertTableRow` to add N-1 rows, then fill each row

## Step 4 — Export PDF
```python
# Get token from ~/.hermes/google_token.json (NOT gws auth export — that requires gws CLI login which is not set up)
token_data = json.loads(open(f"{HERMES_HOME}/google_token.json").read())
token = token_data['token']  # gws_bridge.py refreshes this automatically when called, so it stays fresh

terminal(f"curl -s -L -H 'Authorization: Bearer {token}' "
    f"'https://www.googleapis.com/drive/v3/files/{new_doc_id}/export?mimeType=application/pdf' "
    f"-o /tmp/{invoice_no}.pdf")
```

## Step 5 — Upload to Google Drive + Update Base

```python
# Google Drive folder for Invoices
INVOICE_FOLDER_ID = "1En01XBCAV8j3IDPhPR2vwlp_7Sngm_2P"

filepath = f'/tmp/{invoice_no}.pdf'
filename = f'{invoice_no}_{client_short}.pdf'

token_data = json.loads(open(f"{HERMES_HOME}/google_token.json").read())
access_token = token_data['token']

with open(filepath, 'rb') as f:
    pdf_data = f.read()

metadata = json.dumps({"name": filename, "parents": [INVOICE_FOLDER_ID]}).encode()
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

# PUT Base record: Doc Link + Invoice Status
# Record update: always PUT not PATCH (PATCH returns 404)
```

## Pitfalls
- **Token**: Read from `~/.hermes/google_token.json` directly — `gws auth export` does NOT work (no encrypted creds stored via gws CLI). The `gws_bridge.py` script handles auto-refresh when called, so the token in `google_token.json` stays fresh after any `{GBRIDGE} ...` call.
- **gws_bridge.py path**: Lives at `~/.hermes/skills/core/google-workspace/scripts/gws_bridge.py` — NOT under `productivity/google-workspace/scripts/`. Canonical GBRIDGE definition:
  ```bash
  PYTHON_BIN="~/.hermes/venv/bin/python"
  GBRIDGE="$PYTHON_BIN ~/.hermes/skills/core/google-workspace/scripts/gws_bridge.py"
  ```
- **batchUpdate split**: `--params '{"documentId": "..."}' --json '{"requests": [...]}'` — NOT `--params` for both. The `requests` array silently stringifies if put in `--params`, causing a 400 error.
- OAuth: needs full `drive` + `documents` scopes (not readonly)
- Ship To fields: pass empty string `''` not None — None may render as "None" in doc
- `{{CURRENCY}}` appears in footer line too — replaceAllText catches all instances
- Multi-item: insertTableRow before replaceAllText — only first row gets filled otherwise
- Record update: PUT not PATCH
- **Shared Drive upload returns 404** if you omit `supportsAllDrives=true`. The Invoices folder lives in the DataXquad shared drive (`0AMV9-bYAvS7GUk9PVA`). Always append `?uploadType=multipart&supportsAllDrives=true` to the upload URL. The metadata body does NOT need `supportsAllDrives` — only the URL query param matters.
- **Finding the Invoices folder via gws_bridge**: standard `drive files list` with `q="name='Invoices'"` returns empty when folder is in a shared drive. Use params `corpora=allDrives`, `includeItemsFromAllDrives=true`, `supportsAllDrives=true`. Confirmed Invoices folder ID: `1En01XBCAV8j3IDPhPR2vwlp_7Sngm_2P` (parent: DataXquad shared drive).
