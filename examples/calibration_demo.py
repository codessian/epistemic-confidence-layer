from random import random

from ecl.metrics import ece, reliability_diagram


def synthetic_data(n: int = 1000):
    # Generate synthetic probabilities and binary labels
    probs = [random() for _ in range(n)]
    labels = [1 if p > 0.5 and random() < p else 0 for p in probs]
    return probs, labels


def main():
    probs, labels = synthetic_data(200)
    value = ece(probs, labels, n_bins=10)
    centers, accs, confs, counts = reliability_diagram(probs, labels, n_bins=10)

    print(f"ECE: {value:.4f}")
    print("Bin center | accuracy | confidence | count")
    for c, a, f, n in zip(centers, accs, confs, counts):
        print(f"{c:0.2f}\t\t{a:0.2f}\t\t{f:0.2f}\t\t{n}")


if __name__ == "__main__":
    main()