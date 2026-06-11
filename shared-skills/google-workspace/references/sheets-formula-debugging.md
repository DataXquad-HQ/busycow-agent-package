# Sheets Formula Debugging — Merged Cells & Cross-Sheet References

## Symptom → Root Cause Map

| Symptom | Likely cause | Fix |
|---|---|---|
| `batchUpdate` returns `updatedCells: N` but data not visible | Row has merged cells — only anchor col (A) accepts writes | Unmerge first, then write |
| `FORMULA` render shows col1 only per row | Row is merged | Check `sheet.merges` in metadata |
| `FORMATTED_VALUE` shows one value, `FORMULA` shows empty cols | Row merged AND write landed as static value | Unmerge, re-write as formula |
| Cross-sheet formula evaluates to `#REF!` | Tab name has Chinese chars/spaces, no quotes | Use `='TabName'!Cell` syntax |
| `batchUpdate` succeeds but formula shows wrong result | `valueInputOption` was `RAW` not `USER_ENTERED` | Always use `USER_ENTERED` for formulas |

## Diagnostic Sequence

```python
# 1. Check for merges in affected rows
meta = gapi("GET", f"https://sheets.googleapis.com/v4/spreadsheets/{SID}")
for s in meta["sheets"]:
    if s["properties"]["title"] == "TARGET_TAB":
        for m in s.get("merges", []):
            sr, er = m["startRowIndex"]+1, m["endRowIndex"]
            sc, ec = m["startColumnIndex"]+1, m["endColumnIndex"]
            print(f"rows {sr}-{er}, cols {sc}-{ec}")

# 2. Read with FORMATTED_VALUE to see actual computed values
r = gapi("GET", f"https://sheets.googleapis.com/v4/spreadsheets/{SID}/values/{tab_enc}!A35:I46",
         params={"valueRenderOption": "FORMATTED_VALUE"})
# → shows actual computed output; empty = truly empty or merged anchor

# 3. Read with FORMULA to see what's stored
r = gapi("GET", f"https://sheets.googleapis.com/v4/spreadsheets/{SID}/values/{tab_enc}!A35:I46",
         params={"valueRenderOption": "FORMULA"})
# → shows formula text; empty in merged row = normal (not a write failure)
```

## Unmerge + Rewrite Pattern (confirmed working)

```python
SHEET_ID_INT = 611455117  # integer sheetId from metadata, NOT the spreadsheet string ID

# Unmerge rows (0-indexed row indices)
unmerge_requests = []
for row_idx in range(38, 44):  # rows 39-44 in 1-indexed
    unmerge_requests.append({
        "unmergeCells": {
            "range": {
                "sheetId": SHEET_ID_INT,
                "startRowIndex": row_idx,
                "endRowIndex": row_idx + 1,
                "startColumnIndex": 0,
                "endColumnIndex": 16   # cover all columns generously
            }
        }
    })
gapi("POST", f"https://sheets.googleapis.com/v4/spreadsheets/{SID}:batchUpdate",
     {"requests": unmerge_requests})
time.sleep(1)  # allow Sheets to settle before writing

# Now write values — they will land in all columns
tab_enc = urllib.parse.quote("匯總對照")
put_range("A39:I39", [["Label", "=B33", "=B39/$H$39", "=D33", ...]])
```

## Cross-Sheet Formula Syntax

```python
# Tab with Chinese / spaces / special chars → wrap in single quotes
"='管理費分擔'!D7"    # ✓
"='Sheet 1'!A1"       # ✓
"=管理費分擔!D7"      # ✗ — #REF! error

# Internal same-sheet reference — no quotes needed
"=B33"
"=$H$39"

# Always use USER_ENTERED so Sheets parses the formula string
gapi("POST", f"{BASE}/{SID}/values:batchUpdate", {
    "valueInputOption": "USER_ENTERED",   # ← required for formulas
    "data": [{"range": "Tab!A1", "values": [["='OtherTab'!D2"]]}]
})
```

## Summary Sheet (匯總對照) Formula Architecture — 銀河世紀社區 Case

- **Source tabs**: 大樓區 (rows 4-31), 複層區 (rows 4-43), 別墅區 (rows 4-10)
- **Column mapping in detail tabs**: E=063面積, G=064面積, I=065面積, K=072面積, L=土地合計, M=換算坪, P=車位, R=共有, T=153-2F, V=153-3F, X=153-4F, Z=152底, AA=大公設合計, AB=換算坪
- **Section 5 links**: 管理費分擔 tab rows 2-11 → D/E/F/G = 大樓/複層/別墅/總計
- **坪數佔比 formula**: `=D5/G5` (internal), NOT linked to external tab
- **換算坪**: `=total_sqm / 3.305785` (1坪 = 3.305785㎡)
