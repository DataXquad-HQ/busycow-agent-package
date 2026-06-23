# Install Core Infrastructure

> Audience: Default Hermes or an operator running commands with Default Hermes guidance.
> Scope: prepare the shared infrastructure layers after base Hermes already exists.

Run this before installing individual AI colleagues.

---

## 0. Stop Conditions

Stop and report the gap if any of these are true:

- base Hermes CLI is not available
- package repository is not readable
- no human owner or approval owner is known
- credentials are required but no approved credential handoff exists
- target organization name is unknown
- a requested external write would happen without an approval rule

---

## 1. Confirm Base Hermes

```bash
hermes --version
hermes doctor
hermes profile list
```

Record Hermes version, current default profile, doctor warnings, and package repository path.

---

## 2. Confirm Deployment Metadata

| Field | Required? | Notes |
|---|---|---|
| organization slug | yes | used for paths, banks, logs, and naming |
| human owner | yes | accountable owner |
| approval owner | yes | approves high-risk actions |
| workspace root | yes | default: `/srv/ai-colleagues/workspaces/` |
| collaboration surface | yes | V1 default: Lark/Feishu |
| GBrain sources | yes, may be missing | mark missing if not ready |
| Hindsight endpoint/banks | yes, may be missing | mark missing if not ready |
| structured systems | yes, may be empty | CRM, Plane, approvals, logs |

If values are missing, create an install gap report rather than guessing.

---

## 3. Prepare Workspace & Collaboration Layer

Default filesystem paths:

```bash
sudo mkdir -p /srv/ai-colleagues/workspaces
sudo mkdir -p /srv/ai-colleagues/shared
sudo mkdir -p /srv/ai-colleagues/logs/routine-runs
sudo mkdir -p /srv/ai-colleagues/logs/tool-actions
sudo mkdir -p /srv/ai-colleagues/logs/evaluations
```

V1 collaboration target: Lark/Feishu.

If Lark/Feishu is used, continue with:

```text
playbooks/integrations/lark/README.md
```

Minimum checks, if `lark-cli` exists:

```bash
lark-cli auth status --verify
lark-cli config default-as bot
```

If collaboration delivery is not ready, record it as a delivery gap and do not enable routines that require outbound delivery.

---

## 4. Configure Contextual Layer Assumptions

### GBrain

Record:

- endpoint or MCP name
- sources
- schema pack
- source-level access rules
- home write source convention
- canonical/evidence separation

Recommended V1 sources:

```text
shared
customers
partners
product-eng
internal
```

### Hindsight

Record:

- endpoint
- personal bank naming convention
- shared/domain bank naming convention
- write governance rules

Recommended naming pattern:

```text
{{org_slug}}/agents/{{profile_name}}
{{org_slug}}/shared/{{domain}}
```

### Structured systems

Identify systems that own operational truth:

- CRM or account system
- task or project system
- approval state system
- routine run log
- tool action log
- evaluation log

---

## 5. Configure AI Colleague Agent Layer Assumptions

Define profile conventions before installing colleagues:

```text
~/.hermes/profiles/{{profile_name}}/
  SOUL.md
  config.yaml
  .env
  skills/
  cron/
```

Rules:

- one durable role-owning colleague maps to one Hermes profile
- secrets are never committed
- profile `SOUL.md` stays short
- full operating docs belong in the agent workspace

---

## 6. Configure Operations & Governance Layer

Confirm or create placeholders for:

```text
/srv/ai-colleagues/shared/approval-policy.md
/srv/ai-colleagues/shared/tool-action-log-policy.md
/srv/ai-colleagues/shared/context-routing-policy.md
```

Do not claim the stack is complete unless approval, logging, and stop-condition policies exist or are explicitly accepted as gaps.

---

## 7. Verify Core Infrastructure

Run or confirm:

```bash
hermes doctor
hermes skills list
hermes mcp list
```

Produce a status summary:

| Area | Status | Notes |
|---|---|---|
| Hermes runtime | pass / warn / fail | |
| workspace root | pass / warn / fail | |
| Lark/Feishu | pass / missing / partial | |
| GBrain | pass / missing / partial | |
| Hindsight | pass / missing / partial | |
| structured systems | pass / missing / partial | |
| approvals | pass / missing / partial | |
| logs | pass / missing / partial | |

---

## 8. Next Step

If the core infrastructure is ready or explicitly accepted as partial by the human owner, continue with:

```text
playbooks/bootstrap/install-ai-colleague.md
```

Do not activate role-owning colleagues until core gaps are fixed or explicitly accepted for draft-only install.