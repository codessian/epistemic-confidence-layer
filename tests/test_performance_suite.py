import json
from pathlib import Path

from benchmarks.scripts.performance_suite import compare_results, run_suite


def test_run_suite_returns_all_operations():
    rows = run_suite("optimized", iterations=3, load_factor=1)
    names = {row.operation for row in rows}
    assert names == {"claims_extract", "consensus_score", "synthesis_report", "similarity_classify"}


def test_compare_results_detects_regressions():
    baseline = [{"operation": "op", "elapsed_ms_mean": 10.0}]
    optimized = [{"operation": "op", "elapsed_ms_mean": 9.0}]
    out = compare_results(baseline, optimized, min_improvement=30.0)
    assert len(out["regressions"]) == 1


def test_compare_results_passes_when_improved():
    baseline = [{"operation": "op", "elapsed_ms_mean": 10.0}]
    optimized = [{"operation": "op", "elapsed_ms_mean": 6.0}]
    out = compare_results(baseline, optimized, min_improvement=30.0)
    assert out["aggregate_improvement_pct"] >= 30.0
    assert out["regressions"] == []
