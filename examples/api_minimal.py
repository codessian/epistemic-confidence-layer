import requests
import json

def main():
    payload = {
        "prompt": "Is Knysna in the Western Cape of South Africa?",
        "models": ["stub:gpt", "stub:claude"]
    }
    r = requests.post("http://127.0.0.1:8000/verify", json=payload, timeout=30)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    main()