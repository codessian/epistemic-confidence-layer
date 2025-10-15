from __future__ import annotations
import os, time, json, statistics as stats
from typing import List, Dict
from src.ecl.adapters.base import registry, generate_with_cache
from src.ecl.cache import stats as cache_stats

PROMPT = "Say 'ok' (no preamble)."
N = int(os.getenv("ECL_SMOKE_N", "3"))
TIMEOUT = float(os.getenv("ECL_SMOKE_TIMEOUT_S", "6.0"))

def run_once(adapter_name: str) -> float:
    adapter = registry.get(adapter_name)
    start = time.time()
    # Minimal deterministic call; real providers later
    _ = generate_with_cache(adapter, PROMPT, temperature=0.0, max_tokens=8)
    return time.time() - start

def run_for(name: str) -> Dict:
    try:
        adapter = registry.get(name)
    except ValueError:
        return {"name": name, "status": "missing", "runs": []}
    if not adapter.available():
        return {"name": name, "status": "skipped_no_key", "runs": []}
    durations: List[float] = []
    for _ in range(N):
        t = run_once(name)
        durations.append(min(t, TIMEOUT))
    payload = {
        "name": name,
        "status": "ok",
        "runs": durations,
        "latency_ms": {
            "p50": round(stats.median(durations) * 1000, 2),
            "p95": round((sorted(durations)[max(0, int(0.95 * (len(durations)-1)))] * 1000), 2),
        },
    }
    return payload

def main() -> None:
    targets = os.getenv("ECL_SMOKE_TARGETS", "stub,openai,anthropic").split(",")
    available = list(registry.list().keys())
    targets = [t for t in targets if t in available] + [t for t in available if t.startswith("stub")]
    results = [run_for(t) for t in sorted(set(targets))]
    out = {
        "summary": {
            "providers_total": len(results),
            "ok": sum(1 for r in results if r["status"] == "ok"),
            "skipped": sum(1 for r in results if str(r["status"]).startswith("skipped")),
        },
        "cache": cache_stats(),
        "results": results,
    }
    print(json.dumps(out, indent=2))
    # Write artifacts
    os.makedirs("benchmarks/smoke", exist_ok=True)
    with open("benchmarks/smoke/providers.json", "w") as f:
        json.dump(out, f, indent=2)
    # Also emit a tiny markdown summary for the job summary
    lines = ["# Providers Smoke Report", "", f"*Cache*: `{out['cache']}`", ""]
    for r in out["results"]:
        if r["status"] == "ok":
            lines.append(f"- **{r['name']}**: p50={r['latency_ms']['p50']}ms, p95={r['latency_ms']['p95']}ms")
        else:
            lines.append(f"- **{r['name']}**: _{r['status']}_")
    with open("benchmarks/smoke/summary.md", "w") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()