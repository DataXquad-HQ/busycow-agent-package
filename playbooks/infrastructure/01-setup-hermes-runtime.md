# Setup Hermes Runtime

## Goal
Prepare the target Hermes environment so later contextual-layer and agent steps have a stable base.

## Inputs required
- target machine already reachable
- Hermes CLI installed
- human owner known
- package repo readable

## Steps
1. Confirm Hermes works:
   ```bash
   hermes --version
   hermes doctor
   hermes profile list
   ```
2. Create the expected runtime directories if they do not already exist:
   ```bash
   mkdir -p {{HERMES_INSTALL_ROOT}}/workspaces
   mkdir -p {{HERMES_INSTALL_ROOT}}/shared
   mkdir -p {{HERMES_INSTALL_ROOT}}/logs
   ```
3. Read and adapt:
   - `artifacts/infrastructure/hermes/config.template.yaml`
   - `artifacts/infrastructure/hermes/shared.env.example`
4. Record the target values that later steps will need:
   - `{{ORG_SLUG}}`
   - `{{HERMES_INSTALL_ROOT}}`
   - `{{GBRAIN_REPO_ROOT}}`
   - `{{HINDSIGHT_BASE_URL}}`
   - collaboration surface choice

## Stop conditions
Stop and report if:
- Hermes doctor fails in a way that blocks normal sessions
- the installer cannot determine the target org slug
- no approved secret process exists

## Verify
- Hermes CLI responds
- default profile is visible
- target runtime directories exist
