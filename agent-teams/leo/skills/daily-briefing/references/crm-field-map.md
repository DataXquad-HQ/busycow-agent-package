# CRM Field Map — Sales & Ops Base
# Verified: 2026-06-11 via live field inspection

## App Token
`MtvNbgCHXaRAaUsWXsCjnekep2g`

## Chats
| Chat Name | chat_id |
|---|---|
| [DX] Sales Daily Update | `{{LARK_CHAT_ID}}` |
| 🤖 DataXquad Agent Team | `{{LARK_CHAT_ID}}` |
| [SYS] Backend Report | `{{LARK_CHAT_ID}}` |

---

## 💼 Deals Table (`{{TABLE_ID}}`)

| Field Name | Field ID | Type | Notes |
|---|---|---|---|
| `Deal Name` | `{{FIELD_ID}}` | Text (primary) | Text array — extract `.text` |
| `Client` | `{{FIELD_ID}}` | DuplexLink | Links to Accounts table |
| `Stage` | `{{FIELD_ID}}` | SingleSelect | Lead / Qualified / Proposal / Negotiation / Won / Lost |
| `Priority` | `{{FIELD_ID}}` | SingleSelect | High / Medium / Low |
| `Health Check` | `{{FIELD_ID}}` | SingleSelect | **"At Risk" / "Needs Follow-up" / "Awaiting Response" / "On Track"** |
| `Risk Indicator` | `{{FIELD_ID}}` | SingleSelect | Low / Medium / High — NOT auto-populated by health checks |
| `Business Line` | `{{FIELD_ID}}` | SingleSelect | BusyCow / GeoKernel / AquaOptima / TRACI / Distify / DataXquad |
| `Current Status Summary` | `{{FIELD_ID}}` | Text | |
| `Next Action Summary` | `{{FIELD_ID}}` | Text | |
| `Deal ID` | `{{FIELD_ID}}` | Text | |
| `Owner` | `{{FIELD_ID}}` | User (multi) | |
| `Expected Value` | `{{FIELD_ID}}` | Number | |
| `Expected Close Date` | `{{FIELD_ID}}` | DateTime | |
| `Probability %` | `{{FIELD_ID}}` | Number | |
| `Next Follow-up Date` | `{{FIELD_ID}}` | DateTime | |
| `Last Update Date` | `{{FIELD_ID}}` | DateTime | Manual update timestamp |
| `Week Review Status` | `{{FIELD_ID}}` | SingleSelect | Reviewed / Pending / N/A |
| `Primary Contact` | `{{FIELD_ID}}` | DuplexLink | Links to Contacts table |
| `Tasks` | `{{FIELD_ID}}` | DuplexLink | Links to Sales Tasks table |
| `Activities` | `{{FIELD_ID}}` | DuplexLink | Links to Engagements table |

**⚠️ Risk flag to use for briefing: `Health Check` = "At Risk"**
The `Risk Indicator` field exists but health checks do NOT write to it automatically.

---

## 💼 Sales Tasks Table (`{{TABLE_ID}}`)

| Field Name | Field ID | Type | Notes |
|---|---|---|---|
| `Title` | `{{FIELD_ID}}` | Text (primary) | Text array — extract `.text`. NOT "Task Name" |
| `Done` | `{{FIELD_ID}}` | Checkbox | true/false. NOT a Status field |
| `Deadline` | `{{FIELD_ID}}` | DateTime | NOT "Due Date". Format: `yyyy/MM/dd` |
| `Business Line` | `{{FIELD_ID}}` | SingleSelect | BusyCow / GeoKernel / AquaOptima / TRACI / DataXquad / Distify |
| `Priority` | `{{FIELD_ID}}` | SingleSelect | "🔴 High" / "🟡 Medium" / "🟢 Low" |
| `Responsible Person` | `{{FIELD_ID}}` | User (single) | NOT "Assigned To" |
| `Description` | `{{FIELD_ID}}` | Text | |
| `Agent Advice` | `{{FIELD_ID}}` | Text | |
| `Related Deal` | `{{FIELD_ID}}` | DuplexLink | Links to Deals table |
| `Related Partnership` | `{{FIELD_ID}}` | DuplexLink | Links to Partnership table |
| `Output Link` | `{{FIELD_ID}}` | Url | |

**Filter pattern for today's tasks:**
```json
{
  "conjunction": "and",
  "conditions": [
    {"field_name": "Done", "operator": "is", "value": ["false"]},
    {"field_name": "Deadline", "operator": "is", "value": ["Today"]}
  ]
}
```

**Filter pattern for overdue tasks:**
```json
{
  "conjunction": "and",
  "conditions": [
    {"field_name": "Done", "operator": "is", "value": ["false"]},
    {"field_name": "Deadline", "operator": "isLess", "value": ["Today"]}
  ]
}
```

---

## DateTime Filter Notes

Confirmed working operators for DateTime fields:
- `is` with `["Today"]` → tasks due today ✅
- `is` with `["ExactDate", "<timestamp_ms>"]` → tasks due on specific date ✅
- `isLess` with `["Today"]` → tasks overdue (deadline passed) ✅ (inferred)
- `isGreater` with `["Today"]` → tasks due in future ✅ (inferred)

NOT working:
- `isGreaterEqual` → returns InvalidFilter for DateTime ❌
- `isGreater` / `isLess` with raw numeric timestamp strings ❌
- `is` with `"YYYY-MM-DD"` date string ❌
