# Playbooks

This layer is for Default Hermes and other installation agents.

A playbook is an operational runbook that tells an agent how to perform a task against this package and a target environment.

Playbooks answer: what should the agent do, in what order, when should it stop, and how does it verify success?

---

## Rules

- Playbooks are executable instructions, not architecture essays.
- Playbooks may reference files in `artifacts/`.
- Playbooks must include verification and fallback or stop conditions.
- If a file is primarily explanatory, it belongs in `guidelines/`.
- If a file is copied into runtime, it belongs in `artifacts/`.

---

## Structure

```text
playbooks/
├── README.md
├── bootstrap/
│   ├── install-core-infrastructure.md
│   └── install-ai-colleague.md
└── integrations/
    ├── README.md
    ├── hermes/
    ├── gbrain/
    ├── hindsight/
    ├── lark/
    └── twenty-crm/
```

---

## Current Entry Points

| Path | Use when |
|---|---|
| `bootstrap/install-core-infrastructure.md` | preparing Contextual, Agent, Workspace, and Governance layers after base Hermes exists |
| `bootstrap/install-ai-colleague.md` | installing one selected role-owning AI colleague after core infrastructure verification |
| `integrations/` | setting up or understanding a specific system integration |

---

## Expected Execution Order

```text
1. Confirm human bootstrap is complete
2. Run bootstrap/install-core-infrastructure.md
3. Resolve or explicitly accept core gaps
4. Run bootstrap/install-ai-colleague.md for each selected colleague
5. Run relevant integration playbooks
6. Produce install and activation reports
```

---

## Relationship to Artifacts

Playbooks tell the agent what to do.
Artifacts provide the files to install, copy, or adapt.

If an artifact is missing, the playbook should report the gap instead of pretending the runtime is complete.