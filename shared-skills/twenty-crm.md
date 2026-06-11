---
name: twenty-crm
description: >
  Use when any agent needs to read, write, configure, or query Twenty CRM.
  Covers authentication, GraphQL CRUD, schema introspection, custom objects/fields,
  and common pitfalls. Load this skill before writing any Twenty API code.
  Works across all Hermes profiles — always call the internal VM endpoint.
triggers:
  - "twenty crm"
  - "twenty api"
  - "crm query"
  - "crm write"
  - "twenty graphql"
  - "read from twenty"
  - "write to twenty"
  - "twenty schema"
  - "twenty object"
  - "twenty field"
version: "1.0"
author: BusyCow
---

# Twenty CRM — Universal Access Skill

## ⚠️ Access Rule (ALL agents, ALL profiles)

**Always use the internal VM endpoint. Never use external URLs in agent code.**

| Purpose | URL |
|---------|-----|
| Data CRUD | `http://localhost:3001/graphql` |
| Schema / metadata | `http://localhost:3001/metadata` |
| Health check | `http://localhost:3001/healthz` |
| MCP server | `http://localhost:3001/mcp` |

Tailscale IPs and Cloudflare tunnel URLs are for **human browser access only**.
Using them in agent code causes unnecessary latency and external round-trips.

---

## Authentication

### API Key (preferred for agents)

API keys are long-lived JWTs. Store in a file — never interpolate in shell
(tokens are ~400 chars and get truncated):

```bash
echo "{{TWENTY_API_TOKEN}}" > /tmp/twenty_token.txt
```

```python
TOKEN = open('/tmp/twenty_token.txt').read().strip()
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
```

Get/regenerate via UI: **Settings → API & Webhooks → API Keys → Generate API Key**

> ⚠️ `/tmp` is cleared on VM restart. Regenerate the token at the start of each
> agent session using the refresh flow below.

---

### Token Refresh Flow (when token expires / UNAUTHENTICATED error)

```python
import requests

BASE = "http://localhost:3001/metadata"

def gql(query, token=None, url=BASE):
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return requests.post(url, json={"query": query}, headers=h).json()

# Step 1 — get loginToken from credentials
r1 = gql(
    'mutation { getLoginTokenFromCredentials('
    '  email: "{{TWENTY_ADMIN_EMAIL}}",'
    '  password: "{{TWENTY_ADMIN_PASSWORD}}",'
    '  origin: "http://localhost:3001"'
    ') { loginToken { token } } }'
)
login_token = r1["data"]["getLoginTokenFromCredentials"]["loginToken"]["token"]

# Step 2 — exchange loginToken → accessToken
# IMPORTANT: field is "accessOrWorkspaceAgnosticToken", NOT "accessToken"
r2 = gql(
    f'mutation {{ getAuthTokensFromLoginToken('
    f'  loginToken: "{login_token}",'
    f'  origin: "http://localhost:3001"'
    f') {{ tokens {{ accessOrWorkspaceAgnosticToken {{ token }} }} }} }}'
)
access_token = r2["data"]["getAuthTokensFromLoginToken"]["tokens"]["accessOrWorkspaceAgnosticToken"]["token"]

# Step 3 — generate a fresh API key token
API_KEY_ID = "{{TWENTY_API_KEY_ID}}"
r3 = gql(
    f'mutation {{ generateApiKeyToken('
    f'  apiKeyId: "{API_KEY_ID}",'
    f'  expiresAt: "2030-01-01T00:00:00Z"'
    f') {{ token }} }}',
    access_token
)
api_token = r3["data"]["generateApiKeyToken"]["token"]

with open("/tmp/twenty_token.txt", "w") as f:
    f.write(api_token)
print("Token refreshed and saved.")
```

**Critical pitfalls in the refresh flow:**
1. Both `getLoginTokenFromCredentials` and `getAuthTokensFromLoginToken` require `origin` param — omitting it → validation error
2. Use `accessOrWorkspaceAgnosticToken` — NOT `accessToken`
3. `generateApiKeyToken` requires the **accessToken** from step 2, not the loginToken
4. All three mutations go to `/metadata`, not `/graphql`

---

## Python Helper (copy-paste baseline)

```python
import requests, json

TOKEN = open('/tmp/twenty_token.txt').read().strip()
GQL  = "http://localhost:3001/graphql"
META = "http://localhost:3001/metadata"

def gql(query, url=GQL, variables=None):
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    r = requests.post(url, json=payload, headers=headers, timeout=15)
    d = r.json()
    if d.get("errors"):
        print("GraphQL errors:", json.dumps(d["errors"], indent=2))
    return d
```

---

## Reading & Writing Data (`/graphql`)

### List records

```python
# Standard object
r = gql("{ companies { edges { node { id name } } } }")

# With filter
r = gql('{ companies(filter: { name: { like: "%Acme%" } }) { edges { node { id name } } } }')

# Custom object
r = gql("{ partners { edges { node { id name partnerStage } } } }")
```

### Get single record

```python
r = gql(f'{{ company(id: "{record_id}") {{ id name }} }}')
```

### Create record

```python
r = gql("""
mutation {
  createCompany(data: {
    name: "Acme Corp"
    domainName: { primaryLinkUrl: "acme.com", primaryLinkLabel: "Acme" }
  }) { id name }
}
""")
```

### Update record

```python
r = gql(f"""
mutation {{
  updateCompany(id: "{record_id}", data: {{
    annualRevenue: {{ amountMicros: "5000000000", currencyCode: "USD" }}
  }}) {{ id name }}
}}
""")
```

### Delete record

```python
r = gql(f'mutation {{ deleteCompany(id: "{record_id}") {{ id }} }}')
```

---

## Schema Introspection

### List all queryable objects

```python
r = gql("{ __schema { queryType { fields { name } } } }", url=META)
all_objects = sorted([f["name"] for f in r["data"]["__schema"]["queryType"]["fields"]])
```

### List custom objects only

```python
r = gql("{ objects { edges { node { id nameSingular labelSingular isCustom } } } }", url=META)
custom = [n["node"] for n in r["data"]["objects"]["edges"] if n["node"]["isCustom"]]
```

> **Important:** Standard objects (`company`, `person`, `opportunity`, `note`, `task`)
> do NOT appear in `/metadata` objects query. Use `/graphql` directly.
> Get their metadata IDs from the DB if needed:
> ```bash
> docker exec twenty-db-1 psql -U twenty -d default -c \
>   "SELECT \"nameSingular\", id FROM core.\"objectMetadata\" WHERE \"nameSingular\" IN ('company','person','opportunity');"
> ```

---

## Schema Management — Custom Objects & Fields

### Create custom object

```python
r = gql("""
mutation {
  createOneObject(input: { object: {
    nameSingular: "partner"
    namePlural: "partners"
    labelSingular: "Partner"
    labelPlural: "Partners"
    description: "Resellers and alliances"
    icon: "IconHandshake"
  }}) { id nameSingular }
}
""", url=META)
# Note: "object:" wrapper inside "input:" is REQUIRED
```

### Add a TEXT/NUMBER/DATE_TIME field

```python
r = gql(f"""
mutation {{
  createOneField(input: {{ field: {{
    objectMetadataId: "{OBJECT_ID}"
    name: "quotationId"
    label: "Quotation ID"
    type: TEXT
  }} }}) {{ id name }}
}}
""", url=META)
```

**Supported field types:** `TEXT`, `NUMBER`, `DATE_TIME`, `BOOLEAN`, `LINKS`,
`SELECT`, `MULTI_SELECT`, `CURRENCY`, `FULL_NAME`, `EMAIL`, `PHONE`, `RELATION`

### Add a SELECT field (must use GraphQL variables — not inline strings)

```python
import uuid

mutation = """
mutation CreateField($input: CreateOneFieldMetadataInput!) {
  createOneField(input: $input) { id name }
}"""

variables = {
    "input": {
        "field": {
            "objectMetadataId": OBJECT_ID,
            "name": "status",
            "label": "Status",
            "type": "SELECT",
            "options": [
                {"id": str(uuid.uuid4()), "value": "DRAFT",  "label": "Draft",  "color": "GRAY",  "position": 0},
                {"id": str(uuid.uuid4()), "value": "ACTIVE", "label": "Active", "color": "GREEN", "position": 1},
                {"id": str(uuid.uuid4()), "value": "CLOSED", "label": "Closed", "color": "RED",   "position": 2},
            ]
        }
    }
}

r = gql(mutation, url=META, variables=variables)
```

**SELECT option required fields (all five are required):**
`id` (UUID), `value` (UPPER_SNAKE), `label` (display), `color` (ALL_CAPS), `position` (int 0-based)

**Color enum:** `GRAY` `BLUE` `GREEN` `RED` `YELLOW` `ORANGE` `PURPLE` `TURQUOISE` `SKY` `PINK`

**Reserved field names (will be rejected):** `currency`, `name`, `id`, `createdAt`, `updatedAt`, `deletedAt`

---

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `UNAUTHENTICATED` / `Token invalid` | Token expired (cleared from `/tmp` on reboot) | Run token refresh flow above |
| `Multiple validation errors` | Field already exists, reserved name, OR schema cache stale | Check DB first; restart server if cache stale |
| `Field "CreateOneObjectInput.object" not provided` | Missing `object:` wrapper in `createOneObject` | `input: { object: { ... } }` |
| Object not in `/metadata` objects query | Standard objects don't appear there | Query via `/graphql`; get IDs from DB |
| SELECT options failing | Missing `id` or `position`, or inline JSON escaping | Use variables approach, include all 5 option fields |
| Schema cache stale after object creation | Server hasn't reloaded schema | Restart: `docker compose restart twenty-server-1` (wait ~2 min) |
| Filter on `/metadata` objects not working | Filter arg not supported on metadata API | Fetch all, filter in Python |

### Diagnose "Multiple validation errors" — check nested errors

```python
for e in d.get("errors", []):
    print(json.dumps(e.get("extensions", {}).get("errors", {}), indent=2))
```

---

## Server Management

```bash
# Health check
curl -sf http://localhost:3001/healthz && echo "UP"

# Restart server (clears in-memory schema cache)
cd ~/twenty && docker compose restart twenty-server-1
# Wait ~2 min for NestJS boot

# DB direct access
docker exec twenty-db-1 psql -U twenty -d default

# List fields on an object
docker exec twenty-db-1 psql -U twenty -d default -c \
  "SELECT name, type FROM core.\"fieldMetadata\" WHERE \"objectMetadataId\" = '{{OBJECT_ID}}' ORDER BY name;"

# Database backup
docker exec twenty-db-1 pg_dump -U twenty default > backup_$(date +%Y%m%d).sql
```

---

## Official Docs

- User Guide: https://docs.twenty.com/user-guide/introduction
- Developer Docs: https://docs.twenty.com/developers/introduction
- Self-hosting: https://docs.twenty.com/developers/self-hosting/docker-compose
