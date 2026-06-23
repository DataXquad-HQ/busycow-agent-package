# Hermes AI Colleague Package Guidelines

This folder is the human-readable architecture and design layer for the Hermes AI colleague package.

Use it to understand:

- what this package installs
- how the infrastructure layers fit together
- how Contextual Layer, Agent Layer, Workspace Layer, and Governance Layer are separated
- how to design a new AI colleague
- which AI colleagues are currently represented in the package

If Default Hermes needs to perform setup or migration work, use `../playbooks/`.
If a file should be copied or adapted into a live runtime, use `../artifacts/`.

---

## Reading Order

| File | What it covers |
|---|---|
| `00-system-architecture.md` | Four-layer system architecture: Contextual, Agent, Workspace, Operations/Governance |
| `01-infrastructure-spec.md` | Core runtime infrastructure after base Hermes exists |
| `02-contextual-layer-spec.md` | Contextual Layer rules for GBrain, Hindsight, structured state, and workspace context |
| `03-gbrain-and-hindsight-spec.md` | Current GBrain and Hindsight architecture without legacy assumptions |
| `04-ai-colleague-design-spec-template.md` | Human-facing seven-layer template for designing a new AI colleague |
| `05-mandatory-skills.md` | Cross-agent skill requirements and installation expectations |
| `06-ai-colleague-catalog.md` | Human-facing catalog of designed, packaged, testing, or active AI colleagues |

---

## Design Stack

Every AI colleague should be designed through seven layers:

1. Identity Layer
2. Context Layer
3. Capability Layer
4. Authority Layer
5. Autonomy Layer
6. Evaluation Layer
7. Governance Layer

Do not start by writing a long prompt. Start by defining the colleague's role, context, authority, autonomy, evaluation, and runtime artifacts.

---

## Infrastructure Layers

| Layer | What it owns |
|---|---|
| Contextual Layer | GBrain canonical, GBrain evidence, Hindsight, structured systems, workspace context |
| AI Colleague Agent Layer | Hermes profiles, SOUL.md, skills, cron, profile-local config |
| Workspace & Collaboration Layer | Lark/Feishu collaboration, agent workspaces, drafts, queues, human-agent interaction |
| Operations & Governance Layer | playbooks, approvals, logs, evaluation, audit, stop conditions |

V1 is Lark/Feishu-first. Slack can be added later when Slack-specific artifacts and playbooks exist.

---

## Relationship to Other Layers

| Layer | Purpose |
|---|---|
| `guidelines/` | human-facing architecture, design model, and catalog |
| `playbooks/` | Default Hermes setup, migration, and verification instructions |
| `artifacts/` | files that get installed, copied, or adapted into runtime |

Keep rationale, instructions, and runtime assets separate so another team can understand the package and let Hermes execute it safely.