# Shared Skills

Skills in this directory are available to **all agent profiles**.

Each entry is a folder containing a `SKILL.md` (and optionally `references/`, `scripts/`, `assets/`).

---

## Installation

For each skill you want to share across agents, place the skill folder under:

```
~/.hermes/skills/<category>/<skill-name>/
```

Then register it in `shared_skills/` and symlink it into each agent profile's `_shared/` folder.

**Use the Python script pattern** — bash `ln -sf` loops inside heredocs produce circular symlinks. Always use Python's `os.symlink()` directly.

```python
# /tmp/link_shared_skills.py
import os

HOME = os.path.expanduser("~")
SKILLS_ROOT = HOME + "/.hermes/skills"
SHARED = HOME + "/.hermes/shared_skills"

# Map: skill_name → absolute path to skill folder
skill_targets = {
    "my-skill": SKILLS_ROOT + "/category/my-skill",
    # add more here
}

os.makedirs(SHARED, exist_ok=True)

for skill, target in skill_targets.items():
    # 1. Register in shared_skills/ (the shared registry)
    link = SHARED + "/" + skill
    if os.path.lexists(link):
        os.unlink(link)
    os.symlink(target, link)

    # 2. Symlink into each agent profile _shared/ (point directly to source)
    for agent in ["leo", "maya", "rex"]:
        agent_link = HOME + f"/.hermes/profiles/{agent}/skills/_shared/{skill}"
        if os.path.lexists(agent_link):
            os.unlink(agent_link)
        os.symlink(target, agent_link)
        ok = os.path.isdir(agent_link)
        print(f"  {'OK' if ok else 'FAIL'} {agent}/{skill}")
```

Run: `python3 /tmp/link_shared_skills.py`

---

## Three-Tier Architecture

```
~/.hermes/skills/                          ← Iris private (default profile only)
~/.hermes/shared_skills/                   ← Shared registry (symlinks → real skill dirs)

~/.hermes/profiles/leo/skills/
    _shared/my-skill  → ~/.hermes/skills/category/my-skill   ← shared (symlink)
    my-private-skill/                                          ← Leo private (real dir)

~/.hermes/profiles/maya/skills/_shared/my-skill  → (same real dir)
~/.hermes/profiles/rex/skills/_shared/my-skill   → (same real dir)
```

| Tier | Location | Visible to |
|---|---|---|
| **Iris private** | `~/.hermes/skills/` | Iris (default profile) only |
| **Shared** | `~/.hermes/shared_skills/` + agent `_shared/` symlinks | All agents + Iris |
| **Agent private** | `~/.hermes/profiles/<name>/skills/<skill>/` (real dir) | That agent only |

---

## Key Rules

- **Never copy** skill folders into agent profiles — symlinks only. One update to the source propagates to all agents instantly.
- **`_shared/` entries point directly to the real skill dir**, not via `shared_skills/`. `shared_skills/` is a registry/reference, not the link target for agents.
- **Circular symlink pitfall**: `ln -sf $SHARED/$skill $SHARED/$skill` is self-referential. Always use absolute target paths pointing to the actual skill directory.
- **Agent private skills** are real directories. If a skill starts in an agent profile and becomes broadly useful, move it to `~/.hermes/skills/` and re-symlink.

---

## Current Shared Skills

| Skill | Category | Purpose |
|---|---|---|
| `capturing-to-gbrain` | core | Capture intel from conversation into GBrain |
| `creating-shared-skill` | core | SOP for creating and sharing a new skill |
| `github-core-repos` | core | Read/write internal GitHub repos |
| `hermes-agent` | core | Hermes Agent CLI and config guide |
| `managing-cron-jobs` | core | Create/manage Hermes cron jobs |
| `managing-tasks` | internal-ops | Create/update tasks in Lark task board |
| `planning-next-actions` | internal-ops | Daily planning and prioritisation |
| `reviewing-tasks` | internal-ops | Query and summarise task board |
| `reading-lark-files` | lark-ops | Download and read files from Lark |
| `lark-base` | lark | Lark Bitable operations |
| `lark-calendar` | lark | Lark Calendar operations |
| `lark-contact` | lark | Lark contact lookup |
| `lark-doc` | lark | Read/edit Lark documents |
| `lark-drive` | lark | Lark Drive file management |
| `lark-im` | lark | Lark IM messaging |
| `lark-shared` | lark | Shared Lark auth/setup |
| `lark-task` | lark | Lark task management |
| `lark-workflow-standup-report` | lark | Daily standup report workflow |
