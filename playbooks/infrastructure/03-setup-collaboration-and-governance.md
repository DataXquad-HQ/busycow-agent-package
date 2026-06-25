# Setup Collaboration and Governance

## Goal
Prepare the collaboration surface, approval path, and governance expectations used by agents.

## Required artifacts
- `artifacts/infrastructure/collaboration/README.md`
- `artifacts/infrastructure/governance/README.md`
- `artifacts/infrastructure/governance/approval-policy-template.md`
- `artifacts/infrastructure/governance/logging-policy-template.md`

## Steps
1. Confirm the collaboration surface for V1.
2. If using Lark/Feishu first, review:
   - `playbooks/integrations/lark/README.md`
3. Establish where:
   - human-readable ops summaries go
   - machine logs go
   - approval requests go
4. Adapt the approval and logging policy templates for the target org.
5. Confirm that dangerous actions have a human approval owner.

## Stop conditions
Stop and report if:
- no collaboration surface is selected
- no approval owner exists
- no logging location exists for routine or tool action evidence

## Verify
- delivery channel choice is documented
- approval owner is named
- logging policy exists in at least draft form
