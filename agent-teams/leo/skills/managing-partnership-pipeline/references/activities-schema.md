# Activities Schema
Table ID: `{{TABLE_ID}}`

| Field | Field ID | Type | Notes |
|-------|----------|------|-------|
| Summary | {{FIELD_ID}} | Text (primary) | Format: "[Type] [Contact] @ [Company] — [outcome]" |
| Account | {{FIELD_ID}} | DuplexLink → Accounts | `{"link_record_ids": ["recXXX"]}` |
| Contact | {{FIELD_ID}} | DuplexLink → Contacts | `{"link_record_ids": ["recXXX"]}` |
| Date | {{FIELD_ID}} | DateTime | ms timestamp UTC+8 |
| Type | {{FIELD_ID}} | SingleSelect | 電話 / 實體拜訪 / 線上會議 / WhatsApp/LINE / Demo / 訊息 |
| Client Response | {{FIELD_ID}} | Text | What the partner said / their reaction |
| Stage Advanced? | {{FIELD_ID}} | Checkbox | Boolean true/false |
| Next Action | {{FIELD_ID}} | Text | |
| Opportunity | {{FIELD_ID}} | DuplexLink → Opportunity | `{"link_record_ids": ["recXXX"]}` |
| Partnership | {{FIELD_ID}} | DuplexLink → Partnership | `{"link_record_ids": ["recXXX"]}` |

## Timestamp Helper (UTC+8)
```python
from datetime import datetime, timezone, timedelta
tz = timezone(timedelta(hours=8))
ms = int(datetime(year, month, day, tzinfo=tz).timestamp() * 1000)
```
