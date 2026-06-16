---
name: twenty-crm
description: Query and mutate data in Twenty CRM (the {{COMPANY_NAME}} CRM system) — read pipeline, update records, create leads, manage contacts.
triggers:
  - "CRM"
  - "pipeline"
  - "opportunity"
  - "partnership"
  - "lead"
  - "prospect"
  - "contact in CRM"
  - "twenty"
  - "update stage"
  - "log interaction"
---

# Twenty CRM Skill

## Overview

Twenty CRM runs locally at `http://localhost:3001`. Never use an external URL.

- **API key**: stored in `.env` as `TWENTY_API_KEY`
- **Metadata endpoint**: `POST http://localhost:3001/metadata` — schema introspection only
- **Data endpoint**: `POST http://localhost:3001/graphql` — all reads and writes

## Auth Header Pattern

**Critical — token redaction affects ALL tool surfaces:**
- `write_file` content — any `Bearer <token>` pattern masked
- `terminal << 'HEREDOC'` — same masking
- `execute_code` Python sandbox — token-shaped string literals cause `SyntaxError: unterminated string literal`

**Only safe pattern:** write scripts to disk with `write_file` (loading token from `.env` at runtime, never inline), then run with `terminal python3 /path/to/script.py`. Never pass the token inline in any of the above contexts.

Load token at runtime and build the header by joining a list:

```python
def load_tok():
    with open("/mnt/disks/data/hermes/profiles/leo/.env") as f:
        for line in f:
            line = line.strip()
            if "TWENTY_API_KEY" in line and "=" in line:
                return line.split("=", 1)[1]
    return None

tok = load_tok()

def gql(query, endpoint="http://localhost:3001/graphql"):
    parts = ["Authorization", "Bearer", tok]
    hdr = ": ".join([parts[0], " ".join(parts[1:])])
    resp = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "-H", hdr,
         "-H", "Content-Type: application/json",
         "-d", json.dumps({"query": query}),
         endpoint],
        capture_output=True, text=True
    )
    return json.loads(resp.stdout)
```

Always write scripts to `/mnt/disks/data/hermes/profiles/leo/workspace/` and run with `python3`.

## Core Objects

| Object | Query | Fields |
|---|---|---|
| **Person** | `people`, `person` | name{firstName,lastName}, emails{primaryEmail}, phones, jobTitle, company, status, source, decisionRole, country, preferredChannel, lastContactDate, notes, remarks |
| **Company** | `companies`, `company` | name, domainName{primaryLinkUrl}, employees, city, linkedinLink |
| **Opportunity** | `opportunities`, `opportunity` | name, stage, businessLine, dealType, healthCheck, priority, amount{amountMicros,currencyCode}, closeDate, nextFollowUpDate, nextActionSummary, currentStatusSummary, overview, company, pointOfContact, owner |
| **Partnership** | `partnerships`, `partnership` | name, stage, status, partnerType, startDate, endDate, currentStatusSummary, nextActionSummary, partnershipOverview, primaryContact, company |
| **Task** | `tasks` | title, status, dueAt, body, taskTargets |
| **Note** | `notes` | title, body, noteTargets |

## Opportunity Stages
`NEW` → `SCREENING` → `MEETING` → `PROPOSAL` → `CUSTOMER`

## Key Enums

**Opportunity:**
- `businessLine`: BUSYCOW, GEOKERNEL, AQUAOPTIMA, TRACI, DISTIFY, DATAXQUAD
- `dealType`: DIRECT, PARTNERLED
- `healthCheck`: ON_TRACK, NEEDS_FOLLOWUP, AWAITING_RESPONSE, AT_RISK
- `priority`: HIGH, MEDIUM, LOW

**Person:**
- `status`: (check schema — e.g. PROSPECT, LEAD, etc.)
- `source`: (check schema)
- `decisionRole`: (check schema)
- `country`: (check schema)
- `preferredChannel`: (check schema)

**Partnership:**
- `stage`: (check schema)
- `status`: (check schema)
- `partnerType`: (check schema)

To check any enum values: `{ __type(name: "EnumName") { enumValues { name } } }` via /graphql

## Common Queries

### List all opportunities with stage
```graphql
{ opportunities(first: 50) { edges { node {
    id name stage businessLine dealType healthCheck priority
    nextFollowUpDate nextActionSummary currentStatusSummary
    amount { amountMicros currencyCode }
    company { name }
    pointOfContact { name { firstName lastName } }
} } } }
```

### Get a single opportunity by ID
```graphql
{ opportunity(id: "UUID") { id name stage ... } }
```

### List all partnerships
```graphql
{ partnerships(first: 50) { edges { node {
    id name stage status partnerType
    currentStatusSummary nextActionSummary
    company { name }
    primaryContact { name { firstName lastName } }
} } } }
```

### List all people
```graphql
{ people(first: 50) { edges { node {
    id name { firstName lastName }
    emails { primaryEmail }
    jobTitle company { name }
    status source lastContactDate
} } } }
```

### Filter by field
```graphql
{ opportunities(filter: { stage: { eq: NEW } }) { edges { node { id name } } } }
```

## Common Mutations

### Update opportunity stage
```graphql
mutation {
  updateOpportunity(id: "UUID", data: { stage: SCREENING }) {
    id stage
  }
}
```

### Update opportunity fields
```graphql
mutation {
  updateOpportunity(id: "UUID", data: {
    nextFollowUpDate: "2026-06-20T00:00:00Z"
    nextActionSummary: "Follow up re proposal"
    healthCheck: ON_TRACK
    priority: HIGH
  }) {
    id name stage
  }
}
```

### Create a person
```graphql
mutation {
  createPerson(data: {
    name: { firstName: "John", lastName: "Doe" }
    emails: { primaryEmail: "john@example.com" }
    jobTitle: "CEO"
    companyId: "COMPANY_UUID"
  }) {
    id name { firstName lastName }
  }
}
```

### Create a company
```graphql
mutation {
  createCompany(data: {
    name: "Acme Corp"
    domainName: { primaryLinkUrl: "https://acme.com", primaryLinkLabel: "acme.com" }
    city: "Hong Kong"
  }) {
    id name
  }
}
```

### Create an opportunity
```graphql
mutation {
  createOpportunity(data: {
    name: "Opportunity name"
    stage: NEW
    businessLine: BUSYCOW
    companyId: "COMPANY_UUID"
    pointOfContactId: "PERSON_UUID"
    overview: "Initial context"
  }) {
    id name stage
  }
}
```

### Create a note on an opportunity
```graphql
mutation {
  createNote(data: {
    title: "Note title"
    body: "Content of the note"
    noteTargets: {
      createMany: {
        data: [{ opportunityId: "OPP_UUID" }]
      }
    }
  }) {
    id title
  }
}
```

## Schema Introspection

To explore what fields an object has:
```graphql
# via /graphql
{ __type(name: "Opportunity") { fields { name type { name kind } } } }

# or via /metadata for custom objects
{ objects { edges { node { nameSingular fields { edges { node { name label type } } } } } } }
```

To add a new custom field to an existing object, use the metadata API (POST /metadata):
```graphql
mutation {
  createField(input: {
    objectMetadataId: "OBJECT_UUID"
    field: {
      type: TEXT
      name: "myField"
      label: "My Field"
      description: "Description"
    }
  }) {
    id name
  }
}
```

## Reference Files

- `references/live-schema-snapshot.md` — verified enum values, field list, object counts, and schema divergence notes from 2026-06-14 introspection
- `scripts/twenty_query_template.py` — copy-paste baseline script with safe token loading and gql() helper; copy to workspace/ and run with `python3`

## Pitfalls

- The `/api` REST endpoint returns 404 — always use `/graphql` for data
- The `/metadata` endpoint is only for schema introspection, not data queries
- When filtering enums, use the value without quotes: `{ stage: { eq: NEW } }` not `{ stage: { eq: "NEW" } }`
- Amount is stored as `amountMicros` (millionths of currency unit) — divide by 1,000,000 for display
- The `partnership` and `opportunity` single-record queries by ID can return null if the record was soft-deleted
- When writing scripts: always load the token from env at runtime; never hardcode or pass via string interpolation in write_file (gets redacted)
- Build auth header as: `parts = ["Authorization", "Bearer", tok]; hdr = ": ".join([parts[0], " ".join(parts[1:])])`
- **`opportunity(id: "UUID")` throws "Argument not allowed: id"** — single-record lookup by direct id arg is not supported. Use `opportunities(filter: { id: { eq: "UUID" } })` and take `edges[0].node`
- **`taskTarget` and `noteTarget` link field is `targetOpportunityId`**, not `opportunityId`. Full set: `targetOpportunityId`, `targetPartnershipId`, `targetPersonId`, `targetCompanyId`, `targetEngagementId`
- **`Note.body` does not exist** — the rich text field is `bodyV2`. Use `bodyV2: { markdown: "..." }`. Do NOT pass `{ blocks: [...] }` — that throws "Invalid subfield 'blocks'". The `markdown` subfield is the reliable path
- **`Note.body` vs `bodyV2`**: same pattern applies to `Task` — body field is `bodyV2: { markdown: "..." }` not `body: "..."`
- Best pattern: write full script to `/mnt/disks/data/hermes/profiles/leo/workspace/`, run with `terminal python3 /path/script.py`
- **`opportunity(id: "...")` throws "Argument not allowed: id"** — single-record lookup does NOT accept `id` as a direct argument. Use `opportunities(filter: { id: { eq: "UUID" } }) { edges { node { ... } } }` and take `edges[0]`
- **`filter: { name: { like: "%partial%" } }` on opportunities is unreliable** — often returns empty even when records exist. Safer: list all with `opportunities(first: 100)` and filter by name in Python. Same applies to other objects.
