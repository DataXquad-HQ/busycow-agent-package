# Example — Publish Worker Usage

## Correct CLI pattern
Global flags must come before the subcommand.

```bash
python3 scripts/publish_review_candidate.py \
  --store /tmp/iris-router-dry-run/review_store.json \
  close-loop rq-20260625-document-the-current-runtime-contextual-layer-ar-b2b3d4 \
  --canonical-slug core/strategy/how-we-do-a-better-execution-with-less-people-and-ai-agents \
  --actor Iris
```

## Why this matters
- `--store` and `--repo-root` are top-level flags.
- Put them before `approve`, `publish`, or `close-loop`.
- This avoids the argparse error that appears when `--store` is placed after the subcommand.
