# Verify Infrastructure

## Goal
Do a final check before installing any agent package.

## Checklist
| Area | Pass condition |
|---|---|
| Hermes runtime | CLI works and doctor is acceptable |
| Contextual layer | GBrain path and Hindsight plan exist |
| Collaboration | selected surface and delivery channels are known |
| Governance | approval owner and logging policy exist |

## Commands
```bash
hermes doctor
hermes profile list
```

## Output
Produce a table with:
- pass / warn / fail
- blocker note if any

## Rule
If any blocking infrastructure item is still unresolved, stop before `playbooks/agents/`.
