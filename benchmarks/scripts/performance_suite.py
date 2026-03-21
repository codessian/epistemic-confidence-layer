from __future__ import annotations

import argparse
import gc
import json
import math
import os
import statistics
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from src.claims.extract import heuristic_extract
from src.consensus.score import score_consensus
from src.similarity import classify_similarity
from src.synthesis.report import markdown_summary


def _baseline_extract(prompt: str):
    claims = []
    texts = [prompt.strip()] if prompt.strip().endswith("?") else [t.strip() for t in prompt.split(".") if t.strip()]
    for idx, t in enumerate(texts):
        cid = f"c_{idx:08x}"
        claim_hash = format(abs(hash(t)) % (16**16), "016x")
        claims.append({"id": cid, "text": t, "hash": claim_hash, "provenance": {"source": "baseline"}})
    return claims


def _baseline_summary(claims, consensus):
    lines = ["# ECL Report", ""]
    for claim in claims:
        lines.append(f"- **Claim**: {claim['text']} (`{claim['hash']}`)")
        for candidate in consensus:
            if candidate["claim_id"] == claim["id"]:
                lines.append(f"  - ECS: {candidate['ecs']:.2f}")
    return "\n".join(lines)


@dataclass
class BenchStat:
    operation: str
    mode: str
    iterations: int
    elapsed_ms_mean: float
    elapsed_ms_p95: float
    cpu_ms_mean: float
    peak_kib_mean: float
    throughput_ops_per_s: float
    ci95_low_ms: float
    ci95_high_ms: float

    def as_dict(self) -> dict:
        return {
            "operation": self.operation,
            "mode": self.mode,
            "iterations": self.iterations,
            "elapsed_ms_mean": self.elapsed_ms_mean,
            "elapsed_ms_p95": self.elapsed_ms_p95,
            "cpu_ms_mean": self.cpu_ms_mean,
            "peak_kib_mean": self.peak_kib_mean,
            "throughput_ops_per_s": self.throughput_ops_per_s,
            "ci95_low_ms": self.ci95_low_ms,
            "ci95_high_ms": self.ci95_high_ms,
        }


def _ci95(values: list[float]) -> tuple[float, float]:
    if len(values) < 2:
        return values[0], values[0]
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    margin = 1.96 * (stdev / math.sqrt(len(values)))
    return mean - margin, mean + margin


def _run_benchmark(operation: str, mode: str, func: Callable[[], object], iterations: int) -> BenchStat:
    elapsed_samples: list[float] = []
    cpu_samples: list[float] = []
    peak_samples: list[float] = []
    for _ in range(iterations):
        gc.collect()
        tracemalloc.start()
        t0 = time.perf_counter()
        c0 = time.process_time()
        _ = func()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        cpu_ms = (time.process_time() - c0) * 1000.0
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        _ = current
        elapsed_samples.append(elapsed_ms)
        cpu_samples.append(cpu_ms)
        peak_samples.append(peak / 1024.0)
    mean_elapsed = statistics.mean(elapsed_samples)
    ci_low, ci_high = _ci95(elapsed_samples)
    return BenchStat(
        operation=operation,
        mode=mode,
        iterations=iterations,
        elapsed_ms_mean=mean_elapsed,
        elapsed_ms_p95=sorted(elapsed_samples)[max(0, int(iterations * 0.95) - 1)],
        cpu_ms_mean=statistics.mean(cpu_samples),
        peak_kib_mean=statistics.mean(peak_samples),
        throughput_ops_per_s=(1000.0 / mean_elapsed) if mean_elapsed > 0 else float("inf"),
        ci95_low_ms=ci_low,
        ci95_high_ms=ci_high,
    )


def _benchmark_plan(mode: str, load_factor: int) -> list[tuple[str, Callable[[], object]]]:
    prompt = ("The Earth orbits the Sun. " * load_factor).strip()
    claims = [{"id": f"c{i}", "text": f"claim-{i}", "hash": f"h{i}"} for i in range(1, 20 * load_factor + 1)]
    consensus = [
        {"claim_id": f"c{i}", "ecs": 0.7, "agreement_score": 0.8, "diversity_score": 0.6}
        for i in range(1, 20 * load_factor + 1)
    ]
    extract_func = heuristic_extract if mode == "optimized" else _baseline_extract
    summary_func = markdown_summary if mode == "optimized" else _baseline_summary
    return [
        ("claims_extract", lambda: extract_func(prompt)),
        ("consensus_score", lambda: score_consensus([c["text"] for c in claims], router_meta={"diversity_score": 0.4})),
        ("synthesis_report", lambda: summary_func(claims, consensus)),
        ("similarity_classify", lambda: classify_similarity(prompt, prompt[::-1])),
    ]


def run_suite(mode: str, iterations: int, load_factor: int) -> list[BenchStat]:
    results: list[BenchStat] = []
    for operation, func in _benchmark_plan(mode, load_factor):
        results.append(_run_benchmark(operation, mode, func, iterations))
    return results


def compare_results(baseline: list[dict], optimized: list[dict], min_improvement: float) -> dict:
    baseline_by_op = {row["operation"]: row for row in baseline}
    optimized_by_op = {row["operation"]: row for row in optimized}
    comparisons = []
    regressions = []
    for operation, base_row in baseline_by_op.items():
        opt_row = optimized_by_op[operation]
        before = float(base_row["elapsed_ms_mean"])
        after = float(opt_row["elapsed_ms_mean"])
        improvement = ((before - after) / before) * 100.0 if before > 0 else 0.0
        comparison = {"operation": operation, "before_ms": before, "after_ms": after, "improvement_pct": improvement}
        comparisons.append(comparison)
        if improvement < min_improvement:
            regressions.append(comparison)
    aggregate_improvement = statistics.mean([row["improvement_pct"] for row in comparisons]) if comparisons else 0.0
    return {"comparisons": comparisons, "aggregate_improvement_pct": aggregate_improvement, "regressions": regressions}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=40)
    parser.add_argument("--load-factor", type=int, default=3)
    parser.add_argument("--mode", choices=["baseline", "optimized", "both"], default="both")
    parser.add_argument("--output", type=str, default="benchmarks/results/performance-suite.json")
    parser.add_argument("--min-improvement-pct", type=float, default=30.0)
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload: dict[str, object] = {
        "timestamp": int(time.time()),
        "iterations": args.iterations,
        "load_factor": args.load_factor,
        "python": os.sys.version,
    }

    if args.mode in {"baseline", "both"}:
        baseline = [row.as_dict() for row in run_suite("baseline", args.iterations, args.load_factor)]
        payload["baseline"] = baseline
    if args.mode in {"optimized", "both"}:
        optimized = [row.as_dict() for row in run_suite("optimized", args.iterations, args.load_factor)]
        payload["optimized"] = optimized

    if "baseline" in payload and "optimized" in payload:
        analysis = compare_results(payload["baseline"], payload["optimized"], args.min_improvement_pct)
        payload["analysis"] = analysis
        payload["pass"] = len(analysis["regressions"]) == 0
    else:
        payload["analysis"] = None
        payload["pass"] = True

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if payload["analysis"] is not None and payload["pass"] is False:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
