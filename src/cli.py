import argparse
import json
import requests

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", type=str, help="Prompt to verify")
    ap.add_argument("--models", type=str, default="stub:gpt,stub:claude")
    ap.add_argument("--host", type=str, default="http://127.0.0.1:8000")
    args = ap.parse_args()

    payload = {
        "prompt": args.prompt,
        "models": [m.strip() for m in args.models.split(",") if m.strip()]
    }
    r = requests.post(f"{args.host}/verify", json=payload, timeout=30)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    main()