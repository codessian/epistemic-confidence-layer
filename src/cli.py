import argparse
import json
import sys

import requests


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", type=str, help="Prompt to verify")
    ap.add_argument("--host", type=str, default="http://127.0.0.1:8000")
    ap.add_argument("--contains-pii", action="store_true")
    ap.add_argument("--timeout-s", type=float, default=8.0)
    ap.add_argument("--api-key", type=str, default="")
    args = ap.parse_args()

    payload = {
        "prompt": args.prompt,
        "contains_pii": bool(args.contains_pii),
        "timeout_s": float(args.timeout_s),
    }
    headers = {"Content-Type": "application/json"}
    if args.api_key:
        headers["X-API-Key"] = args.api_key
    try:
        response = requests.post(f"{args.host}/verify", json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
        return 0
    except requests.RequestException as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
