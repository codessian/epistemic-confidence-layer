import os, json, base64, requests
from pathlib import Path

def _resolve_pr_number() -> int:
    # Prefer event payload for reliability
    evt_path = os.getenv("GITHUB_EVENT_PATH")
    if evt_path and Path(evt_path).exists():
        evt = json.loads(Path(evt_path).read_text())
        if "number" in evt:
            return int(evt["number"])
        if "pull_request" in evt and "number" in evt["pull_request"]:
            return int(evt["pull_request"]["number"])
    # Fallback (best effort)
    ref = os.getenv("GITHUB_REF_NAME", "")
    try:
        return int(ref.split("/")[-1])
    except Exception:
        raise SystemExit("Unable to resolve PR number")

def main():
    owner_repo = os.getenv("GITHUB_REPOSITORY", "")
    if "/" not in owner_repo:
        raise SystemExit("GITHUB_REPOSITORY not set")
    owner, repo = owner_repo.split("/")

    metrics_path = Path("benchmarks/results/metrics.json")
    curve_path = Path("benchmarks/results/reliability.png")

    if not metrics_path.exists():
        raise SystemExit("metrics.json not found; did `make evaluate` run?")
    if not curve_path.exists():
        raise SystemExit("reliability.png not found; did `make evaluate` run?")

    metrics = json.loads(metrics_path.read_text())
    ece_before = metrics.get("ece_before", None)
    ece_after  = metrics.get("ece_after", None)
    delta = None if (ece_before is None or ece_after is None) else (ece_after - ece_before)

    img_b64 = base64.b64encode(curve_path.read_bytes()).decode()

    body_lines = [
        "## 📈 ECL Verify — Reliability Report",
        f"**ECE (before):** `{ece_before:.3f}`" if ece_before is not None else "**ECE (before):** `n/a`",
        f"**ECE (after):**  `{ece_after:.3f}`"  if ece_after  is not None else "**ECE (after):**  `n/a`",
    ]
    if delta is not None:
        body_lines.append(f"**Δ ECE:** `{delta:+.3f}`")
    body_lines.append("")
    body_lines.append("<details><summary>Reliability curve</summary>")
    body_lines.append(f'<img src="data:image/png;base64,{img_b64}" alt="reliability" />')
    body_lines.append("</details>")
    body_lines.append("")
    body_lines.append("— _ECL-Verify Bot_ · [docs](https://codessian.github.io/epistemic-confidence-layer/calibration/)")

    pr_number = _resolve_pr_number()
    api = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        raise SystemExit("GITHUB_TOKEN not available")
    r = requests.post(
        api,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        json={"body": "\n".join(body_lines)},
        timeout=30,
    )
    r.raise_for_status()
    print("Comment posted.")

if __name__ == "__main__":
    main()