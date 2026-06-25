#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding='utf-8')
    return sys.stdin.read()


def bullets(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if re.match(r"^[-*]\s+", line.strip())]


def check_operating_brief(text: str) -> tuple[bool, list[str]]:
    notes: list[str] = []
    primary = text.split("## Why this is good", 1)[0]
    lines = [l.strip() for l in primary.splitlines() if l.strip()]
    first = lines[0] if lines else ""
    if first:
        notes.append("ok: executive takeaway present")
    else:
        notes.append("missing: executive takeaway")
    b = bullets(primary)
    if 2 <= len(b) <= 5:
        notes.append(f"ok: bullet count {len(b)} within target")
    else:
        notes.append(f"revise: bullet count {len(b)} outside 2-5 target")
    joined = " ".join(b).lower()
    if any(k in joined for k in ["owner", "deadline", "approval", "risk", "blocked", "decision"]):
        notes.append("ok: bullets reference execution/decision signals")
    else:
        notes.append("revise: bullets may be too generic")
    if "recommendation" in text.lower() and "verified" in text.lower():
        notes.append("ok: facts and recommendations are separated")
    else:
        notes.append("warn: explicit fact/recommendation labels not found")
    passed = sum(n.startswith("ok:") for n in notes) >= 3 and not any(n.startswith("missing:") or n.startswith("revise:") for n in notes[:2])
    return passed, notes


def check_required_labels(text: str, labels: list[str]) -> tuple[bool, list[str]]:
    notes: list[str] = []
    lowered = text.lower()
    missing = []
    for label in labels:
        if label.lower() in lowered:
            notes.append(f"ok: found `{label}`")
        else:
            missing.append(label)
            notes.append(f"missing: `{label}`")
    return len(missing) == 0, notes


def check_review_item(text: str) -> tuple[bool, list[str]]:
    return check_required_labels(text, [
        "title:",
        "type:",
        "current_source:",
        "why_it_matters:",
        "recommended_action:",
        "owner_or_approver:",
        "evidence_links:",
    ])


def check_handoff(text: str) -> tuple[bool, list[str]]:
    return check_required_labels(text, [
        "task_title:",
        "receiver:",
        "why_receiver:",
        "current_status:",
        "timing_expectation:",
        "why_it_matters:",
        "relevant_decision_or_policy:",
        "evidence_links:",
        "expected_output:",
        "approval_boundary:",
        "escalation_trigger:",
    ])


def main() -> int:
    p = argparse.ArgumentParser(description="Validate Iris runtime outputs against lightweight workspace contracts.")
    p.add_argument("mode", choices=["operating-brief", "review-item", "handoff"])
    p.add_argument("--file", help="Path to markdown/text file. Omit to read stdin.")
    args = p.parse_args()
    text = read_text(args.file)

    if args.mode == "operating-brief":
        ok, notes = check_operating_brief(text)
    elif args.mode == "review-item":
        ok, notes = check_review_item(text)
    else:
        ok, notes = check_handoff(text)

    print(f"RESULT: {'PASS' if ok else 'REVISE'}")
    for note in notes:
        print(f"- {note}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
