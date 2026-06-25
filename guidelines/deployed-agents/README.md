# Deployed Agents

This folder contains the design specs for packaged AI colleagues.

These specs are the human-readable record of what each agent does, why it exists, and how it maps to runtime artifacts. They are not the runtime configuration itself.

## Active packaged agents

| Agent | Title | The Number It Owns | Status |
|---|---|---|---|
| [Iris](iris-spec.md) | Chief of Staff | Operating integrity across ownership, context, and system health | ✅ Packaged / testing |
| [Leo](leo-spec.md) | BD Lead Agent | Pipeline progression, follow-up integrity, and conversion support | ✅ Packaged |

## Pending packaged agents

| Agent | Title | Notes |
|---|---|---|
| Maya | Growth Lead Agent | Packaged artifacts exist but the full runtime should be re-verified before activation |
| Rex | Customer Success Agent | Runtime package not yet fully audited in this repo |
| Steve | Development Lead Agent | Still treated as a future or partial runtime in the package |

## How to read these specs

Each spec follows the deployed-agent template. The spec is the hiring brief: it explains why the agent exists, what it does, and how it maps to actual build artifacts such as `SOUL.md`, skills, workspace docs, and cron expectations.
