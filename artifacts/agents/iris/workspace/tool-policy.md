# Iris Tool Policy

## Business surfaces
- Lark conversations
- Lark Tasks (target execution layer)
- Lark Bitable / legacy Task Tracker (current executable fallback path)
- GBrain Core / Evidence
- Hindsight banks
- Review Queue
- Approval surface

## Hermes runtime toolsets
- file
- skills
- todo
- session_search
- cronjob
- terminal (restricted)
- memory / Hindsight provider
- GBrain surface

## Side-effect routing rule
- task owner / deadline / blocked-state changes should land in structured task state
- durable historical proof should land in `evidence/`
- governed truth changes should go to review before `core/` publication
- workspace notes are allowed when the system-of-record write is pending, but they must be labelled as pending

## Runtime rule
If a tool can cause a high-impact side effect, Iris should propose or escalate rather than acting directly.
