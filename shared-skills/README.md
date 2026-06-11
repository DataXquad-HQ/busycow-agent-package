# Shared Skills

Hermes skills available to **every agent profile** — not tied to any single agent.

Each `.md` file here is a Hermes `SKILL.md` that can be dropped into any profile's
`~/.hermes/skills/` directory and loaded automatically.

---

## Skills Index

| Skill file | What it does | Load when |
|-----------|-------------|-----------|
| `twenty-crm.md` | Read, write, and configure Twenty CRM via GraphQL | Any agent needs to query or update CRM data |

---

## Installation

Copy each skill you want into the Hermes skills directory:

```bash
# Single skill
cp twenty-crm.md ~/.hermes/skills/core/twenty-crm/SKILL.md

# All shared skills at once
for f in *.md; do
  name="${f%.md}"
  mkdir -p ~/.hermes/skills/core/$name
  cp "$f" ~/.hermes/skills/core/$name/SKILL.md
done
```

After copying, the skill appears in `hermes skills list` on the next session.

---

## Conventions

- One `.md` file = one Hermes skill = one `SKILL.md`
- All sensitive values use `{{PLACEHOLDER}}` — fill in after copying
- Skills here are **universalized** (no client names, no hardcoded IDs)
- When a skill is updated on the live VM, sync the update back here
