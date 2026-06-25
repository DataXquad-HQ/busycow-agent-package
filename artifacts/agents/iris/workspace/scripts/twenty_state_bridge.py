#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import requests

DEFAULT_BASE = 'http://localhost:3001'


def gql(base: str, token: str, query: str) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(f"{base}/graphql", json={"query": query}, headers=headers, timeout=20)
    return r.json()


def load_token(path: str | None) -> str:
    if not path:
        raise SystemExit('Provide --token-file with a valid Twenty API token file.')
    return Path(path).read_text(encoding='utf-8').strip()


def main() -> int:
    p = argparse.ArgumentParser(description='Iris bridge for Twenty CRM current-state reads.')
    p.add_argument('command', choices=['health', 'companies', 'opportunities'])
    p.add_argument('--base-url', default=DEFAULT_BASE)
    p.add_argument('--token-file')
    p.add_argument('--limit', type=int, default=5)
    args = p.parse_args()

    if args.command == 'health':
        r = requests.get(f"{args.base_url}/healthz", timeout=10)
        print(json.dumps({'status_code': r.status_code, 'body': r.json()}, ensure_ascii=False, indent=2))
        return 0

    token = load_token(args.token_file)
    if args.command == 'companies':
        q = f'{{ companies(first: {args.limit}) {{ edges {{ node {{ id name }} }} }} }}'
    else:
        q = f'{{ opportunities(first: {args.limit}) {{ edges {{ node {{ id name stage }} }} }} }}'
    print(json.dumps(gql(args.base_url, token, q), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
