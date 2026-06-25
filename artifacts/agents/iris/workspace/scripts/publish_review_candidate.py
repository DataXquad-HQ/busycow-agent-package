#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from contextual_layer.review_queue import DEFAULT_STORE, add_note, find_candidate, load_store, now_iso, save_store  # type: ignore


def resolve_target(repo_root: Path, canonical_slug: str | None, canonical_file: str | None) -> tuple[str, Path]:
    if canonical_file:
        path = Path(canonical_file)
        if not path.is_absolute():
            path = repo_root / path
        slug = canonical_slug or path.relative_to(repo_root).as_posix().removesuffix('.md')
        return slug, path
    if not canonical_slug:
        raise SystemExit('Provide --canonical-slug or --canonical-file')
    return canonical_slug, repo_root / f"{canonical_slug}.md"


def cmd_approve(args: argparse.Namespace) -> int:
    candidates = load_store(args.store)
    c = find_candidate(candidates, args.candidate_id)
    c.status = 'approved'
    c.updated_at = now_iso()
    add_note(c, args.actor, args.note or 'Approved for canonical publication', 'approved')
    save_store(candidates, args.store)
    print(json.dumps({'candidate_id': c.candidate_id, 'status': c.status}, ensure_ascii=False, indent=2))
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root)
    slug, path = resolve_target(repo_root, args.canonical_slug, args.canonical_file)
    if not path.exists():
        raise SystemExit(f'Canonical file not found: {path}')

    candidates = load_store(args.store)
    c = find_candidate(candidates, args.candidate_id)
    if c.status not in {'approved', 'published'}:
        raise SystemExit(f'Candidate must be approved before publish. Current status: {c.status}')

    c.status = 'published'
    c.updated_at = now_iso()
    note = args.note or f'Canonical publication verified at {slug}'
    add_note(c, args.actor, note, 'published')
    save_store(candidates, args.store)
    print(json.dumps({
        'candidate_id': c.candidate_id,
        'status': c.status,
        'canonical_slug': slug,
        'canonical_file': str(path),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_close_loop(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root)
    slug, path = resolve_target(repo_root, args.canonical_slug, args.canonical_file)
    if not path.exists():
        raise SystemExit(f'Canonical file not found: {path}')

    candidates = load_store(args.store)
    c = find_candidate(candidates, args.candidate_id)
    if c.status == 'new':
        c.status = 'approved'
        c.updated_at = now_iso()
        add_note(c, args.actor, args.approve_note or 'Approved for canonical publication', 'approved')
    if c.status != 'approved' and c.status != 'published':
        raise SystemExit(f'Unexpected status before publish: {c.status}')
    c.status = 'published'
    c.updated_at = now_iso()
    add_note(c, args.actor, args.publish_note or f'Canonical publication verified at {slug}', 'published')
    save_store(candidates, args.store)
    print(json.dumps({
        'candidate_id': c.candidate_id,
        'status': c.status,
        'canonical_slug': slug,
        'canonical_file': str(path),
    }, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Iris helper for closing the review-queue -> canonical publish loop.')
    p.add_argument('--store', type=Path, default=DEFAULT_STORE)
    p.add_argument('--repo-root', default='{{GBRAIN_REPO_ROOT}}')
    sub = p.add_subparsers(dest='command', required=True)

    approve = sub.add_parser('approve')
    approve.add_argument('candidate_id')
    approve.add_argument('--actor', default='Iris')
    approve.add_argument('--note', default='')
    approve.set_defaults(func=cmd_approve)

    publish = sub.add_parser('publish')
    publish.add_argument('candidate_id')
    publish.add_argument('--canonical-slug')
    publish.add_argument('--canonical-file')
    publish.add_argument('--actor', default='Iris')
    publish.add_argument('--note', default='')
    publish.set_defaults(func=cmd_publish)

    close_loop = sub.add_parser('close-loop')
    close_loop.add_argument('candidate_id')
    close_loop.add_argument('--canonical-slug')
    close_loop.add_argument('--canonical-file')
    close_loop.add_argument('--actor', default='Iris')
    close_loop.add_argument('--approve-note', default='')
    close_loop.add_argument('--publish-note', default='')
    close_loop.set_defaults(func=cmd_close_loop)
    return p


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))
