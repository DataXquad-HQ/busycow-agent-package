# Iris Workspace Package

This directory packages the **workspace harness** for the Iris Chief-of-Staff agent.

It is the operating layer that sits next to `SOUL.md` and the skill folders.

## What is included

- operating instructions (`AGENTS.md`)
- authority / approval / memory / routing rules
- runbooks for daily operations and governance loops
- examples, templates, schemas, evaluators, and anti-examples
- lightweight validation and bridge scripts under `scripts/`

## Install target

Copy this whole directory into the runtime workspace path expected by the agent, for example:

```text
{{HERMES_INSTALL_ROOT}}/workspaces/iris/
```

The packaged scripts assume this same relative workspace depth when they look upward to the Hermes install root.

## Placeholder notes

- `{{HERMES_INSTALL_ROOT}}` → local Hermes install root
- `{{GBRAIN_REPO_ROOT}}` → local checked-out GBrain / knowledge-base repository
- `{{LARK_USER_OPEN_ID}}` → user identity for Lark tasklist setup examples
- `[Founder 1]` / `[Founder 2]` / `[Portfolio Company]` / `[Org]` → replace with local deployment values if needed
