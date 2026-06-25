#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any


def run(args: list[str]) -> dict[str, Any]:
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr.strip() or p.stdout.strip() or f"command failed: {' '.join(args)}")
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Non-JSON output from lark-cli: {e}\n{p.stdout}")


def cmd_ensure_tasklist(args: argparse.Namespace) -> int:
    found = run(["lark-cli", "task", "+tasklist-search", "--query", args.name, "--as", "user"])
    items = (((found.get("data") or {}).get("items")) or [])
    for item in items:
        if item.get("name") == args.name:
            print(json.dumps({"status": "exists", "guid": item.get("guid"), "url": item.get("url")}, ensure_ascii=False, indent=2))
            return 0
    created = run(["lark-cli", "task", "+tasklist-create", "--name", args.name, "--member", args.member, "--as", "user"])
    data = created.get("data") or {}
    print(json.dumps({"status": "created", "guid": data.get("guid"), "url": data.get("url")}, ensure_ascii=False, indent=2))
    return 0


def cmd_create_task(args: argparse.Namespace) -> int:
    cli = [
        "lark-cli", "task", "+create",
        "--tasklist-id", args.tasklist_id,
        "--summary", args.summary,
        "--description", args.description,
        "--assignee", args.assignee,
        "--as", "user",
    ]
    if args.due:
        cli += ["--due", args.due]
    out = run(cli)
    print(json.dumps(out.get("data") or out, ensure_ascii=False, indent=2))
    return 0


def cmd_query_my_tasks(args: argparse.Namespace) -> int:
    cli = ["lark-cli", "task", "+get-my-tasks", "--as", "user"]
    if args.query:
        cli += ["--query", args.query]
    out = run(cli)
    print(json.dumps(out.get("data") or out, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Iris bridge for Lark default Tasks.")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("ensure-tasklist")
    a.add_argument("--name", required=True)
    a.add_argument("--member", required=True)
    a.set_defaults(func=cmd_ensure_tasklist)

    b = sub.add_parser("create-task")
    b.add_argument("--tasklist-id", required=True)
    b.add_argument("--summary", required=True)
    b.add_argument("--description", required=True)
    b.add_argument("--assignee", required=True)
    b.add_argument("--due")
    b.set_defaults(func=cmd_create_task)

    c = sub.add_parser("query-my-tasks")
    c.add_argument("--query")
    c.set_defaults(func=cmd_query_my_tasks)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
