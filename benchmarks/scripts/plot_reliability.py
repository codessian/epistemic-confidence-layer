import argparse
import json
import os
import matplotlib.pyplot as plt
from typing import List, Tuple

def load_toy(path: str) -> Tuple[List[float], List[int]]:
    probs, labels = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            probs.append(row["prob"])
            labels.append(int(row["label"]))
    return probs, labels

def reliability_curve(probs: List[float], labels: List[int], bins: int = 10):
    buckets = [[] for _ in range(bins)]
    for p, y in zip(probs, labels):
        i = min(bins - 1, int(p * bins))
        buckets[i].append((p, y))
    xs, ys = [], []
    for i, b in enumerate(buckets):
        if not b:
            continue
        mean_conf = sum(p for p, _ in b) / len(b)
        acc = sum(y for _, y in b) / len(b)
        xs.append(mean_conf)
        ys.append(acc)
    return xs, ys

def calculate_ece(probs: List[float], labels: List[int], bins: int = 10) -> float:
    """Calculate Expected Calibration Error."""
    bucket = [[] for _ in range(bins)]
    for p, y in zip(probs, labels):
        i = min(bins - 1, int(p * bins))
        bucket[i].append((p, y))
    total = 0.0
    n = len(probs)
    for b in bucket:
        if not b:
            continue
        acc = sum(y for _, y in b) / len(b)
        conf = sum(p for p, _ in b) / len(b)
        total += (len(b) / n) * abs(acc - conf)
    return total

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    probs, labels = load_toy(args.input)
    xs, ys = reliability_curve(probs, labels)
    
    # Calculate ECE (before calibration - using raw probabilities)
    ece_before = calculate_ece(probs, labels)
    
    # For now, ECE after is the same (no calibration implemented yet)
    ece_after = ece_before
    
    # Create metrics.json for bot consumption
    metrics = {
        "ece_before": ece_before,
        "ece_after": ece_after,
        "n_samples": len(probs)
    }
    
    metrics_path = os.path.join(os.path.dirname(args.output), "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    plt.figure()
    plt.plot([0,1],[0,1], linestyle="--", label="Perfect calibration")
    plt.scatter(xs, ys, label="Actual performance")
    plt.xlabel("Confidence")
    plt.ylabel("Accuracy")
    plt.title(f"Reliability Curve (ECE: {ece_before:.3f})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    plt.savefig(args.output, bbox_inches="tight", dpi=150)
    
    print(f"Reliability curve saved to {args.output}")
    print(f"Metrics saved to {metrics_path}")
    print(f"ECE: {ece_before:.3f}")

if __name__ == "__main__":
    main()