# Skills — Iris

## Purpose

This folder contains the **Iris runtime skill layer** for [Org] use.

The goal is simple:
- Iris should not rely only on a shared registry
- the package should explicitly carry the skills Iris is expected to use
- the package should make it obvious which parts of the Iris spec are already backed by real artifacts

## Package-local Iris skills currently present

### Iris-specific governance skills
| Skill | Purpose |
|---|---|
| `capturing-operating-changes` | capture structural or operating decisions across GBrain, Hindsight, and the task layer |
| `reviewing-operating-state` | determine what is actively true now, what is stale, and what systems must change |
| `routing-founder-decisions` | route founder direction into the correct durable system layer |
| `governing-okr-and-task-state` | keep objectives, KRs, and execution tasks aligned to current company reality |
| `openmail` | read the BD inbox when Iris needs pipeline visibility |

### Packaged capability skills copied into Iris
These are included here so Iris is package-complete for [Org] use, even when they also exist in a broader shared runtime layer.

#### C1 — Operations, Team & Agent Management
- `managing-tasks`
- `reviewing-tasks`
- `planning-next-actions`
- `generating-task-briefing`
- `generating-daily-ops-briefing`

#### C2 — Infrastructure Management
- `checking-context-health`
- `managing-cron-jobs`
- `packaging-to-github`
- `managing-skills`

#### C3 — Context, Memory & Knowledge Management
- `extracting-lark-to-gbrain`
- `ingesting-sessions-to-hindsight`
- `capturing-to-gbrain`
- `maintaining-gbrain`
- `syncing-brain-memory`
- `managing-team-knowledge`

## Tool dependencies that are NOT package-local skills
These are still part of Iris's operating surface, but they are integration dependencies rather than Iris-local skill folders in this package.

- task system / task board integration
- knowledge-base / GBrain integration
- hot-memory / Hindsight integration
- messaging integration

## Coverage against the current Iris package

| Package area | Status |
|---|---|
| capability skills | packaged |
| governance skills | packaged |
| workspace harness | packaged under `../workspace/` |
| C4 Financial Analysis | intentionally not built yet |

## Practical meaning

Iris is not only:
- a `SOUL.md`
- plus a reference spec
- plus an assumption that shared tools exist elsewhere

Iris now has an explicit package skill layer **and** an explicit packaged workspace harness that cover the active non-financial scope in the spec.
