from typing import Iterable, List, Tuple


def ece(probabilities: Iterable[float], labels: Iterable[int], n_bins: int = 10) -> float:
    """
    Compute Expected Calibration Error (ECE).

    Parameters:
        probabilities: iterable of predicted confidences in [0, 1]
        labels: iterable of true labels as 0/1 (binary)
        n_bins: number of equal-width bins across [0, 1]

    Returns:
        ECE value in [0, 1].
    """
    probs = list(probabilities)
    y_true = list(labels)

    if len(probs) != len(y_true):
        raise ValueError("probabilities and labels must have same length")
    if len(probs) == 0:
        return 0.0

    bins: List[List[int]] = [[] for _ in range(n_bins)]
    bin_totals: List[List[float]] = [[] for _ in range(n_bins)]

    for p, y in zip(probs, y_true):
        if not (0.0 <= p <= 1.0):
            raise ValueError("probabilities must be within [0, 1]")
        if y not in (0, 1):
            raise ValueError("labels must be 0 or 1 for binary ECE")
        # Bin index: include p=1.0 in last bin
        idx = min(int(p * n_bins), n_bins - 1)
        bins[idx].append(y)
        bin_totals[idx].append(p)

    total_count = len(probs)
    ece_value = 0.0
    for ys, ps in zip(bins, bin_totals):
        if not ys:
            continue
        acc = sum(ys) / len(ys)
        conf = sum(ps) / len(ps)
        weight = len(ys) / total_count
        ece_value += weight * abs(acc - conf)

    return ece_value


def reliability_diagram(
    probabilities: Iterable[float], labels: Iterable[int], n_bins: int = 10
) -> Tuple[List[float], List[float], List[float], List[int]]:
    """
    Compute reliability diagram bin stats.

    Returns:
        (bin_centers, accuracies, confidences, counts)
    """
    probs = list(probabilities)
    y_true = list(labels)

    if len(probs) != len(y_true):
        raise ValueError("probabilities and labels must have same length")
    if len(probs) == 0:
        return [], [], [], []

    bins: List[List[int]] = [[] for _ in range(n_bins)]
    bin_totals: List[List[float]] = [[] for _ in range(n_bins)]

    for p, y in zip(probs, y_true):
        if not (0.0 <= p <= 1.0):
            raise ValueError("probabilities must be within [0, 1]")
        if y not in (0, 1):
            raise ValueError("labels must be 0 or 1 for binary reliability diagram")
        idx = min(int(p * n_bins), n_bins - 1)
        bins[idx].append(y)
        bin_totals[idx].append(p)

    centers: List[float] = []
    accuracies: List[float] = []
    confidences: List[float] = []
    counts: List[int] = []

    width = 1.0 / n_bins
    for i, (ys, ps) in enumerate(zip(bins, bin_totals)):
        left = i * width
        right = (i + 1) * width
        centers.append((left + right) / 2.0)
        if ys:
            accuracies.append(sum(ys) / len(ys))
            confidences.append(sum(ps) / len(ps))
            counts.append(len(ys))
        else:
            accuracies.append(0.0)
            confidences.append(0.0)
            counts.append(0)

    return centers, accuracies, confidences, counts