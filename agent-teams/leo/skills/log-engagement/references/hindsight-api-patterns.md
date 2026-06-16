# Hindsight API Patterns — Verified 2026-06-15

Base URL: `http://localhost:8888`
Auth: None (local)

---

## Create a Bank

```bash
# ❌ WRONG — POST returns "Method Not Allowed"
curl -X POST http://localhost:8888/v1/default/banks ...

# ✅ CORRECT — use PUT with bank_id in the path
curl -X PUT http://localhost:8888/v1/default/banks/{{HINDSIGHT_PIPELINE_BANK}} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "{{COMPANY_NAME}} Pipeline Memory",
    "mission": "Description of what this bank stores and why.",
    "disposition": {"skepticism": 3, "literalism": 3, "empathy": 3}
  }'
```

## List All Banks

```bash
curl http://localhost:8888/v1/default/banks
```

Returns array with `bank_id`, `name`, `fact_count`, `last_document_at`.

## Store a Memory

```bash
curl -X POST http://localhost:8888/v1/default/banks/{{HINDSIGHT_PIPELINE_BANK}}/memories \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{
      "content": "CompanyName — 2026-06-15: Had discovery call. Outcome: interested but CFO not looped in yet. Blocker: need CFO intro. Next: Hunter to ask primary contact to arrange intro — by June 20.",
      "tags": ["opportunity", "company-name", "opportunity"]
    }]
  }'
```

## Recall Memories (Semantic Search)

```bash
curl -X POST http://localhost:8888/v1/default/banks/{{HINDSIGHT_PIPELINE_BANK}}/memories/recall \
  -H "Content-Type: application/json" \
  -d '{"query": "CompanyName opportunity — background and blockers", "top_k": 5}'
```

---

## Bank Design Decisions

### Why `{{HINDSIGHT_PIPELINE_BANK}}` is a separate bank (not `{{HINDSIGHT_INTERNAL_BANK}}`)

`{{HINDSIGHT_INTERNAL_BANK}}` is designed for cross-agent handoffs and team-level operational decisions.
If Leo, Iris, Maya all write to `{{HINDSIGHT_INTERNAL_BANK}}`, opportunity-level context gets mixed with
unrelated team ops — recall signal degrades.

`{{HINDSIGHT_PIPELINE_BANK}}` is:
- Opportunity-scoped: every entry is about a specific Opportunity or Partnership
- Multi-agent readable (Leo writes, but any agent can recall)
- Clean signal: only sales context, nothing else

### Bank inventory (as of 2026-06-15)

| Bank | Facts | Purpose |
|---|---|---|
| `{{HINDSIGHT_PIPELINE_BANK}}` | 0 (new) | Opportunity contextual memory — C4/C5 primary bank |
| `{{HINDSIGHT_GLOBAL_BANK}}` | 54 | Company-level facts, portfolio, team structure |
| `{{HINDSIGHT_HUMAN_BANK_1}}` | 12 | Hunter's style and priorities |
| `{{HINDSIGHT_HUMAN_BANK_2}}` | 16 | Kevin's style and priorities |
| `dx-agent-iris` | 10 | Iris working memory |
| `{{HINDSIGHT_AGENT_BANK}}` | 0 | Leo private working memory |
| `{{HINDSIGHT_INTERNAL_BANK}}` | 0 | Cross-agent team ops |
