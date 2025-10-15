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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    probs, labels = load_toy(args.input)
    xs, ys = reliability_curve(probs, labels)
    plt.figure()
    plt.plot([0,1],[0,1], linestyle="--")
    plt.scatter(xs, ys)
    plt.title("Reliability (Toy)")
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    plt.savefig(args.output, bbox_inches="tight")

if __name__ == "__main__":
    main()