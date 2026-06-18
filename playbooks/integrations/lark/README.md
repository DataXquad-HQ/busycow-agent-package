# Lark / Feishu

## What it is

Lark (international) / Feishu (China) is the team workspace. It is the
primary communication and coordination layer for the agent team.

In the packaged BusyCow deployment, **Lark CLI is a required companion to the
Lark integration**. It is not optional glue code. It is the operational surface
used to bind the app, enforce identity policy, troubleshoot permission issues,
and cover actions that are awkward or unavailable through Hermes gateway / MCP
alone.

---

## Role in the stack

| Layer | Role |
|---|---|
| Hermes gateway | Messaging runtime — the agent receives and sends chat messages |
| Lark app | The bot identity and app-level permission container |
| `lark-cli` | App binding, identity policy, auth inspection, permission troubleshooting, and direct operational access |

---

## Packaging policy

### Default mode

For a standard BusyCow deployment, bind `lark-cli` to the **same Lark app used
by the Hermes runtime**, then operate it in **bot-default, bot-restricted** mode.

This avoids repeated user OAuth prompts and makes the operational model easier
to reason about.

### Why

- The app identity is stable and centrally managed
- Bot-mode behavior is easier to package and reproduce
- User OAuth prompts are removed from normal operations
- Agents can still send messages, update operational records, and manage docs
  that the app already has permission to access

### What this means

- Normal package behavior assumes **bot identity first**
- `--as user` is an **exception path**, not the default
- If a deployment needs user-level actions later, the operator can explicitly
  relax the policy and run user auth as a conscious decision

---

## Key settings

Record these settings in the target deployment:

| Setting | Required value / pattern | Why it matters |
|---|---|---|
| Lark app binding | Same app as Hermes runtime | Keeps CLI and agent runtime on one permission surface |
| Workspace | Shared deployment workspace name (for example `hermes`) | Makes all agents read the same `lark-cli` config / token store |
| `default-as` | `bot` | Makes bot the default identity for direct CLI use |
| `strict-mode` | `bot` | Prevents accidental user-mode auth and user-only command drift |
| App scopes | Must include the bot-level scopes the workflow needs | App permission is the real gate in bot mode |
| Resource access | Bot must be added to required chats / docs / bases | Bot mode cannot access resources it was never granted |

---

## Required setup sequence

### 1. Create or select the deployment app

Create one Lark app for the deployment, or select the already-approved app that
Hermes will use.

### 2. Bind `lark-cli` to that app

```bash
lark-cli config init --new
```

Bind it into the shared workspace used by the deployment.

### 3. Enforce bot-default operation

```bash
lark-cli config default-as bot
lark-cli config strict-mode bot
```

### 4. Verify the policy landed

```bash
lark-cli config default-as
lark-cli config strict-mode
lark-cli auth status --verify
lark-cli config show
```

Expected outcomes:
- `default-as: bot`
- `strict-mode: bot`
- bot identity is `ready`
- the config is stored in the intended shared workspace

---

## Operational rule

**Use `lark-cli` as the package's operator-facing control plane for Lark.**

Use it for:
- binding the Lark app
- checking bot readiness
- inspecting scopes
- diagnosing permission failures
- enforcing identity policy
- direct operational actions when Hermes gateway / MCP is not the right surface

Do not assume Hermes messaging alone replaces `lark-cli`.

---

## Break-glass exception: temporary user mode

If a deployment truly needs user-level actions later:

1. explicitly relax policy
2. run user auth
3. complete the task
4. return the deployment to bot-restricted mode

Example:

```bash
lark-cli config strict-mode off
# perform explicit user auth only if the operator wants this
# lark-cli auth login --scope "..."

# after the exceptional task is complete
lark-cli config default-as bot
lark-cli config strict-mode bot
```

This should be treated as an exception workflow, not the default package model.

---

## Common failure modes in bot-default deployments

| Symptom | Likely cause | Fix |
|---|---|---|
| CLI asks for user auth | strict mode not set to bot, or command is being run as a user workflow | re-check `default-as` and `strict-mode`; avoid user-only commands |
| Bot cannot access a doc / base / chat | Resource not shared with the app / bot | add the bot or grant the app access |
| Permission denied despite bot mode | Missing app scope | add scope in developer console and publish the app update |
| Different agents see different CLI state | They are not sharing the same workspace | standardize the deployment workspace name |

---

## What this package assumes

This package assumes:

- Lark is part of the deployment's operating system
- `lark-cli` is installed and used intentionally
- the CLI is bound to the same app as Hermes
- bot mode is the default and protected operating posture

If a client wants a different policy, document that as a deployment-specific
override rather than silently drifting from the package default.
