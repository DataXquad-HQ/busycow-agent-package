# Setup Entrypoint

This is the first file a human operator or Default Hermes should read after base Hermes is available in a target environment.

This repository assumes the human has already completed host-level bootstrap:

- VM or host exists
- base Hermes is installed and runnable
- Default Hermes has access to this repository
- required credentials can be provided through the target environment's approved secret process

Do not start by installing individual AI colleagues. Install the core infrastructure layers first, then install selected colleague profiles.

---

## Choose the Right Layer

| Need | Start here |
|---|---|
| Understand the architecture | `guidelines/README.md` |
| Let Default Hermes perform setup | `playbooks/README.md` |
| Install or copy runtime files | `artifacts/README.md` |

---

## Default Install Flow

### Phase 0: Confirm Human Bootstrap

Default Hermes should confirm, not perform, these host-level items:

- VM or host exists
- base Hermes CLI works
- package repo is readable
- operator has identified the target organization name
- credential handoff process is defined
- human approval owner is known

### Phase 1: Install Core Infrastructure

Run:

```text
playbooks/bootstrap/install-core-infrastructure.md
```

This phase prepares:

- Contextual Layer: GBrain, Hindsight, structured systems, workspace context rules
- AI Colleague Agent Layer: Hermes profile conventions and shared runtime assumptions
- Workspace & Collaboration Layer: Lark/Feishu-first collaboration and workspace setup
- Operations & Governance Layer: logging, audit, approval, and tool policy expectations

### Phase 2: Install Selected AI Colleagues

Run:

```text
playbooks/bootstrap/install-ai-colleague.md
```

This phase installs role-owning colleagues from `artifacts/agents/`.

Each installed colleague should get:

- one Hermes profile
- one `SOUL.md`
- one agent workspace
- workspace `AGENTS.md` and operating docs
- selected skills
- memory policy
- authority policy
- routine and evaluation policy
- credentials through the target environment's secret process

### Phase 3: Verify Before Activation

Before calling an AI colleague active, verify:

- profile can start
- required context sources are readable
- source priority and conflict rules are documented
- Hindsight personal bank works
- shared/domain memory write rules are governed
- structured data writes are gated where needed
- Lark/Feishu delivery works if required
- dangerous external actions require approval
- routine logs and tool action logs are written
- evaluator or human review path exists

---

## Human Reading Path

1. `guidelines/00-system-architecture.md`
2. `guidelines/01-infrastructure-spec.md`
3. `guidelines/02-contextual-layer-spec.md`
4. `guidelines/04-ai-colleague-design-spec-template.md`
5. `guidelines/06-ai-colleague-catalog.md`
6. `artifacts/README.md`

## Agent Execution Path

1. `playbooks/README.md`
2. `playbooks/bootstrap/install-core-infrastructure.md`
3. `playbooks/bootstrap/install-ai-colleague.md`
4. integration playbooks under `playbooks/integrations/`
5. selected files under `artifacts/`

---

## Safety Rule

If the package lacks an artifact, credential, approval rule, or data source for a requested AI colleague, Default Hermes should record the gap and stop before activation. It may draft missing files, but it should not pretend the colleague is production-ready.