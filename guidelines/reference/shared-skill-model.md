# Shared Skill Model

This document explains how shared skills work in the BusyCow agent package.

## Why this exists

A multi-agent deployment needs some skills to be reused across agents, but not every skill should be installed everywhere.

The package therefore separates skills into three categories:

1. **Shared Canonical Core** — centrally governed, copied into multiple active agent profiles
2. **Shared Infra / Selective Install** — governed centrally, but only installed where the role actually needs them
3. **Agent-local Skills** — owned by one agent domain and not treated as shared by default

---

## The Three Layers

### 1. Canonical shared source

The maintained source of truth lives in the Hermes shared governance layer:

```text
~/.hermes/skills/<category>/<skill-name>/
```

This is where Iris updates the skill first.

### 2. Runtime profile copy

Agents do not load a single global shared directory at runtime.
Instead, each active agent gets a concrete copy inside its own profile:

```text
~/.hermes/profiles/<agent>/skills/<skill-name>/
```

This preserves runtime isolation.

### 3. Package artifact copy

When a shared skill should be distributed to clients, the package stores it as a real artifact under:

```text
artifacts/shared-skills/<skill-name>/
```

If an agent also needs an agent-local runtime copy inside the package, that goes under:

```text
artifacts/agents/<agent>/skills/<skill-name>/
```

---

## Category 1 — Shared Canonical Core

These are the current shared-core skills for active agents:

- `skill-creator`
- `managing-skills`
- `managing-shared-skills`
- `capturing-to-gbrain`
- `routing-report-delivery` — shared dual-mode report contract + cron recovery / resume handling

### What makes a skill shared core

A skill belongs here when:
- more than one agent should use it
- the logic should stay centrally maintained
- the workflow defines governance, capture, or common operating behavior
- profile-specific differences are minor or temporary

### Current active rollout

The current active shared-core baseline is copied into:
- `leo`
- `maya`
- `rex`

---

## Category 2 — Shared Infra / Selective Install

These skills are shared-capable, but should only be installed where the role actually needs them.

Examples:
- `twenty-crm`
- `openmail`
- `reading-lark-files`
- `google-workspace`
- `managing-lark-cli-identity`
- `operating-lark-cli-identity`
- internal ops family such as `managing-tasks` or `reviewing-tasks`
- knowledge maintenance family such as `extracting-lark-to-gbrain`, `maintaining-gbrain`, `syncing-brain-memory`

### Rule

Do not copy these everywhere by habit.
Selective install is intentional.

---

## Category 3 — Agent-local Skills

These skills stay local to one role unless repeated reuse proves otherwise.

Examples:
- Leo's CRM / pipeline workflow skills
- Rex's support / remote-debug workflows
- Maya-local content or framework skills

### Rule

Agent-local does not mean low quality.
It only means the skill should not yet be governed as a shared skill.

---

## Route separation

A major governance rule is that **external package publication** and **internal knowledge writing** are separate routes.

### External reusable artifact route
Use:
- `packaging-to-github`

Use this when the destination is:
- `busycow-agent-package`
- client-installable artifacts
- generalized shared skills
- generalized agent artifacts

### Internal durable knowledge route
Use:
- `capturing-to-gbrain`
- `operating-dx-gbrain-vault`

Use this when the destination is:
- `dx-gbrain`
- GBrain MCP operations
- internal company knowledge
- durable entity / decision / intel storage

### Important consequence

Do **not** publish internal-only operating skills into the package repo just because they are canonical locally.
For example:
- `operating-dx-gbrain-vault` is canonical internally
- but it is **not** a client package artifact

---

## Rollout rule

When a shared canonical skill changes:

1. update the canonical source first
2. decide whether the change should propagate to all active profiles
3. if yes, re-copy it into the relevant profiles
4. if it is package-facing, update `artifacts/shared-skills/` too
5. update the shared registry / rollout docs if classification changed

---

## What not to do

- do not rely on runtime symlinks as the default pattern
- do not edit only one profile copy and forget the canonical source
- do not install every shared-capable skill into every profile
- do not confuse internal operating skills with client package artifacts
- do not mix package publication workflows with dx-gbrain internal knowledge workflows

---

## Where to look next

- `guidelines/05-mandatory-skills.md` — mandatory cross-agent baseline
- `artifacts/shared-skills/README.md` — package artifact entrypoint for shared skills
- `artifacts/shared-skills/managing-shared-skills/references/shared-skill-registry.md` — current classification
- `artifacts/shared-skills/managing-shared-skills/references/shared-skill-rollout-plan.md` — current rollout state
