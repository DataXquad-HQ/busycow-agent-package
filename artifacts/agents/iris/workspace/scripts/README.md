# Iris validation scripts

These scripts are lightweight executable checks and bridge helpers for the workspace runtime contracts.

## Available
- `validate_runtime_output.py`
  - `operating-brief` — checks takeaway + bullet count + signal quality
  - `review-item` — checks required review-item labels
  - `handoff` — checks required handoff labels
- `publish_review_candidate.py`
  - `approve` / `publish` / `close-loop` for governed canonical publication
- `lark_default_task_bridge.py`
  - ensure default tasklist
  - create a default Lark Task
  - query my tasks
- `lark_approval_bridge.py`
  - query approvals
  - report missing approval scopes cleanly
- `twenty_state_bridge.py`
  - `health` without auth
  - `companies` / `opportunities` with `--token-file`

## Example usage
```bash
python3 scripts/validate_runtime_output.py operating-brief --file examples/daily-operating-brief-example.md
python3 scripts/validate_runtime_output.py review-item --file examples/review-item-filled-example.md
python3 scripts/validate_runtime_output.py handoff --file examples/handoff-packet-filled-example.md
python3 scripts/publish_review_candidate.py --store /tmp/review_store.json close-loop <candidate_id> --canonical-slug core/strategy/example
python3 scripts/lark_default_task_bridge.py ensure-tasklist --name 'Iris Operating Loop' --member {{LARK_USER_OPEN_ID}}
python3 scripts/lark_approval_bridge.py --topic 1
python3 scripts/twenty_state_bridge.py health
```

These are intentionally lightweight. They do not replace human judgment, but they make Iris V1 more executable than docs-only validation.
