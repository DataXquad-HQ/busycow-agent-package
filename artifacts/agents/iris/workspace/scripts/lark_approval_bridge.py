#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any


def run(args: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main() -> int:
    p = argparse.ArgumentParser(description="Iris bridge for Lark approvals.")
    p.add_argument("--topic", default="1", help="Approval topic: 1=todo, 2=done, 17=unread, 18=read")
    args = p.parse_args()
    code, out, err = run(["lark-cli", "approval", "tasks", "query", "--params", json.dumps({"topic": args.topic}), "--as", "user"])
    text = out.strip() or err.strip()
    try:
        payload: dict[str, Any] = json.loads(text)
    except Exception:
        print(text)
        return code
    if not payload.get("ok") and (payload.get("error") or {}).get("subtype") == "missing_scope":
        print(json.dumps({
            "status": "blocked",
            "reason": "missing_scope",
            "missing_scopes": payload["error"].get("missing_scopes", []),
            "hint": payload["error"].get("hint"),
        }, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(payload.get("data") or payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
