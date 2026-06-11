# Partnership Schema
Table ID: `{{TABLE_ID}}`

| Field | Field ID | Type | Notes |
|-------|----------|------|-------|
| ID | {{FIELD_ID}} | Text (primary) | Format: P001, P002... Next: P009 |
| Name | {{FIELD_ID}} | Text | Partner company name |
| Summary | {{FIELD_ID}} | Text | Short partner description (1 line) |
| Description | {{FIELD_ID}} | Text | Full notes / running narrative log — append on each update |
| Account | {{FIELD_ID}} | DuplexLink → Accounts | `{"link_record_ids": ["recXXX"]}` |
| Stage | {{FIELD_ID}} | SingleSelect | Prospect / Qualifying / Agreement / Active / On Hold / Inactive |
| Activities | {{FIELD_ID}} | DuplexLink → Activities | |
| Contract | {{FIELD_ID}} | DuplexLink → Contracts | |

## Stage Options
Prospect → Qualifying → Agreement → Active → On Hold / Inactive
