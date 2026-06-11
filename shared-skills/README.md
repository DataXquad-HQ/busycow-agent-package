# Shared Skills

Hermes skills available to **every agent profile** — not tied to any single agent.

Each entry is a Hermes skill (a `SKILL.md` file, optionally with `scripts/` and `references/`)
that can be installed into any profile's `~/.hermes/skills/` directory.

---

## Skills Index

| Skill | Directory | What it does |
|-------|-----------|-------------|
| `twenty-crm` | `twenty-crm/` | Read, write, and configure Twenty CRM via GraphQL |
| `google-workspace` | `google-workspace/` | Gmail, Calendar, Drive, Sheets, Docs via gws CLI |
| `cloudflare-tunnels` | `cloudflare-tunnels/` | Set up and manage Cloudflare Tunnels for self-hosted tools |

---

## Installation

Each skill is a directory. Copy the whole directory into Hermes skills:

```bash
# Single skill
cp -r twenty-crm ~/.hermes/skills/core/twenty-crm

# All shared skills at once
for skill_dir in */; do
  skill="${skill_dir%/}"
  mkdir -p ~/.hermes/skills/core/$skill
  cp -r $skill_dir/. ~/.hermes/skills/core/$skill/
done
```

After copying, the skill appears in `hermes skills list` on the next session.

---

## Conventions

- Each skill is a **folder** containing at minimum a `SKILL.md`
- Supporting files go in `scripts/` (executable), `references/` (context docs), `templates/`
- All sensitive values use `{{PLACEHOLDER}}` — fill in after copying to your instance
- Skills here are **universalized** — no client names, no hardcoded IDs
- When a skill is updated on the live VM, sync the change back here
