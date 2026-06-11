---
name: enriching-leads
description: >
  Use when a new Account is added to the CRM, or when user asks to enrich
  an existing Account with more info. Web-searches the company, finds description,
  website, industry, address, and confirms with user before writing to Lark Base.
  Use when user says "幫我查一下這家公司", "enrich this account", "補一下資料",
  "lead enriching", or when capturing-sales-intel creates a new Account record.
triggers:
  - "enrich"
  - "幫我查一下這家公司"
  - "補一下客戶資料"
  - "lead enriching"
  - "查這間公司"
  - "enriching"
version: "1.0"
author: DataXquad
---

# Enriching Leads

## Purpose
Automatically enrich an Account record in the CRM by web-searching the company,
extracting key facts, mapping to the correct Industry, and confirming with the user
before writing to Lark Base.

---

## Trigger Conditions
- A new Account is just created (e.g. by capturing-sales-intel)
- User mentions a company name and asks to find more info
- User explicitly says "enrich" / "查一下" / "補資料"

---

## Accounts Table
- **App Token:** `MtvNbgCHXaRAaUsWXsCjnekep2g`
- **Table ID:** `{{TABLE_ID}}`

### Writable Fields

| Field | Field ID | Type | Notes |
|-------|----------|------|-------|
| Client Name | `{{FIELD_ID}}` | Text (primary) | |
| Short Name | `{{FIELD_ID}}` | Text | |
| Country | `{{FIELD_ID}}` | SingleSelect | Taiwan / Hong Kong / Malaysia |
| Address | `{{FIELD_ID}}` | Text | |
| Company Email | `{{FIELD_ID}}` | Text | |
| Description | `{{FIELD_ID}}` | Text | 2–3 sentence company intro |
| Industry | `{{FIELD_ID}}` | SingleSelect | See options below |
| Website | `{{FIELD_ID}}` | Url | `{"link": "https://...", "text": "company.com"}` |
| Company Size | `{{FIELD_ID}}` | SingleSelect | |

### Industry Options
| Option | Use For |
|--------|---------|
| 科技/SaaS | Tech companies, software, AI platforms |
| 醫療/照護 | Healthcare, eldercare, clinics |
| 製造/代理 | Manufacturing, trading, distribution |
| 水務/公用事業 | Water utilities, power, public infrastructure |
| 零售/電商 | Retail, e-commerce |
| 物流/交通 | Logistics, transport, fleet |
| 建築/地產 | Construction, real estate |
| 金融/保險 | Finance, insurance, banking |
| 教育 | Schools, training, edtech |
| 政府/公共機構 | Government bodies, statutory bodies |
| 餐飲/酒店 | F&B, hospitality |
| 其他 | Doesn't fit above |

---

## Step 1: Identify the Account

Get the company name to enrich. Either:
- Passed in from conversation context (just created)
- User names the company explicitly

If the account already has a Lark Base record_id, retrieve current fields first:
```python
mcp_lark_bitable_v1_appTableRecord_search(
    path={"app_token": "MtvNbgCHXaRAaUsWXsCjnekep2g", "table_id": "{{TABLE_ID}}"},
    data={"filter": {"conjunction": "and", "conditions": [
        {"field_name": "Client Name", "operator": "contains", "value": [company_name]}
    ]}}
)
```

---

## Step 2: Web Search

Run 1–2 targeted searches:
```
"{company_name}" official website about
"{company_name}" company profile industry
```

Extract:
- **Official website URL**
- **Company description** (2–3 sentences, what they do, who they serve)
- **Industry** (map to one of the options above)
- **HQ address** (if findable)
- **Company email** (if findable)
- **Country** (if not already known)

---

## Step 3: Confirm with User

Present findings before writing:

```
🔍 找到以下資料：

公司：{Client Name}
網址：{website}
介紹：{description}
產業：{industry}
地址：{address}
國家：{country}

確認寫入 CRM 嗎？或有需要修正的地方？
```

Wait for user confirmation. Accept partial confirmation ("網址不對，其他 OK").

---

## Step 4: Write to Lark Base

After confirmation, update the Account record:

```python
fields = {}
if website:    fields["Website"] = {"link": website, "text": website.replace("https://","").rstrip("/")}
if description: fields["Description"] = description
if industry:   fields["Industry"] = industry          # must match exact option name
if address:    fields["Address"] = address
if email:      fields["Company Email"] = email
if country:    fields["Country"] = country

mcp_lark_bitable_v1_appTableRecord_update(
    path={"app_token": "MtvNbgCHXaRAaUsWXsCjnekep2g",
          "table_id": "{{TABLE_ID}}",
          "record_id": record_id},
    data={"fields": fields}
)
```

---

## Step 5: Confirm to User

```
✅ 已更新 {Client Name}：
- 網址、介紹、產業、地址 已寫入 CRM
```

---

## Pitfalls
- Industry must exactly match one of the SingleSelect options — if unsure, use 其他
- Website field is Url type — must pass `{"link": "...", "text": "..."}` not plain string
- Always confirm before writing — never auto-write without user approval
- If web search finds conflicting info (e.g. multiple companies with same name), ask user to clarify
- Country field only has 3 options (Taiwan / Hong Kong / Malaysia) — if other country, leave blank and note it
