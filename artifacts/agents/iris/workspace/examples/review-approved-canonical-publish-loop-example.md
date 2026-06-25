# Example — Review-Approved Canonical Publish Loop

This example uses the same **temporary review store** from the router dry run so the live queue stays clean.

## Candidate used
- candidate id: `rq-20260625-document-the-current-runtime-contextual-layer-ar-b2b3d4`
- destination: `gbrain:canonical`
- topic: current runtime contextual-layer architecture snapshot

## Actual transition sequence

### Step 1 — Approved
```bash
python3 contextual_layer/review_queue.py \
  --store /tmp/iris-router-dry-run/review_store.json \
  status rq-20260625-document-the-current-runtime-contextual-layer-ar-b2b3d4 \
  --status approved \
  --actor Iris \
  --note 'Dry-run approval for V1 publish workflow example'
```

Result:
- status became `approved`
- decision note was added with actor, timestamp, and note

### Step 2 — Published
```bash
python3 contextual_layer/review_queue.py \
  --store /tmp/iris-router-dry-run/review_store.json \
  status rq-20260625-document-the-current-runtime-contextual-layer-ar-b2b3d4 \
  --status published \
  --actor Iris \
  --note 'Dry-run publish completion for V1 workflow example'
```

Result:
- status became `published`
- a second decision note was added

## Actual final queue state
- final status: `published`
- proposed destination: `gbrain:canonical`
- review owner: `Iris`

## Why this example matters
- It proves the review queue can carry a candidate from `new` -> `approved` -> `published`.
- It gives Iris a concrete closure pattern instead of leaving candidates hanging at approval.
- It keeps queue state and publication state conceptually paired.
