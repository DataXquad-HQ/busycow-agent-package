# Google Docs Quotation Workflow

## Template IDs

| Template | Doc ID | Notes |
|----------|--------|-------|
| BC EN (T&C + signature) | `12mLc7uyGDyZfkr0n-HBfI8_sjgih11M2nNeI0slJBqI` | BusyCow only, EN |
| BC CH (T&C + signature) | `1IwhlC21pqCrOr2rG8s1ZGuqR2YeJDZ14-6MfHCgLVMY` | BusyCow only, CH |
| DX General EN | `1gvJbwQXQ4jbkQ8BQOO0BRm5WGTX7VvRfVuMkWGqDyPM` | All other, EN |
| DX General CH | `1dPHLGFGOwObhfgDbDzVJkc7AxvRmjbpl7awb29hR1lg` | All other, CH |

## PDF Upload Folder
- Lark Drive Folder Token: `YS6IfaoFElljcjdpsN6jx1rYpBg`
- URL: https://cjpg0xp67g6h.jp.larksuite.com/drive/folder/YS6IfaoFElljcjdpsN6jx1rYpBg

## Placeholders (identical across all 4 templates)
```
{{ENTITY_NAME}}            ← company entity name
{{ENTITY_ADDRESS}}         ← company entity address
{{QUOTATION_NO}}           ← QUO-YYYY-SHORTNAME-NNN
{{ISSUE_DATE}}             ← EN: "28 May 2026" / CH: "2026年5月28日"
{{DUE_DATE}}               ← valid until (same format as ISSUE_DATE)
{{CLIENT_NAME}}            ← contact person name
{{CLIENT_COMPANY}}         ← client company full name
{{CLIENT_COMPANY_ADDRESS}} ← client address
{{CLIENT_TITLE}}           ← contact title (BC templates only — signature block)
{{ITEM_DESC}}              ← line item description (one row in template)
{{ITEM_QTY}}               ← quantity
{{ITEM_PRICE}}             ← unit price (formatted with commas)
{{ITEM_AMOUNT}}            ← line total
{{SUBTOTAL}}               ← sum of items
{{TAX}}                    ← tax (empty string if 0)
{{TOTAL}}                  ← grand total
{{CURRENCY}}               ← HKD / USD
```

## Entity Config
```python
ENTITIES = {
    'SG': {
        'name': 'DATAXQUAD PTE. LTD.',
        'address': '108 Punggol Walk #07-20 Twin Waterfalls, Singapore 828764',
    },
    'TW': {
        'name': 'ATA LIMITED 應科聯有限公司',
        'address': 'Rm. 202, I-Hub, No. 100, Wenhua Rd., Xitun Dist., Taichung City, Taiwan 407',
    },
}
```

## Step 1 — Copy Template
```python
HERMES_HOME = os.environ.get('HERMES_HOME', os.path.expanduser('~/.hermes'))
SKILL_DIR = f"{HERMES_HOME}/skills/productivity/google-workspace"
PYTHON_BIN = f"{HERMES_HOME}/hermes-agent/venv/bin/python"
GBRIDGE = f"{PYTHON_BIN} {SKILL_DIR}/scripts/gws_bridge.py"

r = terminal(f"{GBRIDGE} drive files copy --params "
    f"'{{\"fileId\": \"{TEMPLATE_ID}\", \"name\": \"{quo_id} | {client_name}\", \"fields\": \"id\"}}'")
new_doc_id = json.loads(r)['id']
```

## Step 2 — Replace Placeholders
```python
replacements = {
    '{{ENTITY_NAME}}': entity['name'],
    '{{ENTITY_ADDRESS}}': entity['address'],
    '{{QUOTATION_NO}}': quo_id,
    '{{ISSUE_DATE}}': issue_date_str,
    '{{DUE_DATE}}': valid_until_str,
    '{{CLIENT_NAME}}': client_contact,
    '{{CLIENT_COMPANY}}': client_company,
    '{{CLIENT_COMPANY_ADDRESS}}': client_address,
    '{{CLIENT_TITLE}}': client_title,   # BC only
    '{{SUBTOTAL}}': f"{subtotal:,.0f}",
    '{{TAX}}': f"{tax:,.0f}" if tax else "",
    '{{TOTAL}}': f"{total:,.0f}",
    '{{CURRENCY}}': currency,
}
requests_list = [
    {'replaceAllText': {'containsText': {'text': k, 'matchCase': True}, 'replaceText': v}}
    for k, v in replacements.items()
]
params = json.dumps({'documentId': new_doc_id, 'requests': requests_list})
terminal(f"{GBRIDGE} docs documents batchUpdate --params '{params}'")
```

## Step 3 — Line Items (multi-item)
Template has ONE `{{ITEM_DESC}}` row per item.
- Single item: replaceAllText directly (already done above)
- Multiple items: use `insertTableRow` to add rows, then fill with unique markers per row

## Step 4 — Export PDF
```python
terminal(f"curl -s -L -H 'Authorization: Bearer TOKEN' "
    f"'https://www.googleapis.com/drive/v3/files/{new_doc_id}/export?mimeType=application/pdf' "
    f"-o /tmp/{quo_id}.pdf")
```

## Step 5 — Upload to Lark Drive
```python
# parent_node = YS6IfaoFElljcjdpsN6jx1rYpBg (quotation folder)
# Returns file_token → construct URL:
file_url = f'https://cjpg0xp67g6h.jp.larksuite.com/file/{file_token}'
```

## Pitfalls
- OAuth: needs full `drive` + `documents` scopes (not readonly)
- Date format differs by language: EN = "28 May 2026", CH = "2026年5月28日"
- `{{CLIENT_TITLE}}` only in BC templates — DX templates don't have signature block
- Record update: PUT not PATCH (PATCH returns 404 on Lark Bitable)
- For multi-item: insertTableRow before replaceAllText, otherwise only first row gets filled
