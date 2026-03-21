from __future__ import annotations
import os
import pickle
import numpy as np
from typing import Iterable, List
try:
    from sklearn.isotonic import IsotonicRegression
except Exception:
    IsotonicRegression = None

class IsotonicCalibrator:
    def __init__(self) -> None:
        self._iso = IsotonicRegression(out_of_bounds="clip") if IsotonicRegression else None
        self._fitted = False

    def fit(self, scores: np.ndarray | list[float], labels: np.ndarray | list[int]) -> "IsotonicCalibrator":
        xs = np.asarray(scores, dtype=np.float32)
        ys = np.asarray(labels, dtype=np.float32)
        if self._iso is not None:
            self._iso.fit(xs, ys)
        self._fitted = True
        return self

    def predict(self, scores: np.ndarray | list[float]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("IsotonicCalibrator not fitted")
        xs = np.asarray(scores, dtype=np.float32)
        if self._iso is not None:
            return self._iso.predict(xs)
        # Fallback: identity mapping
        return xs

# --- Function-style API for v0.2 bundle compatibility ---
def fit_isotonic(y_score: Iterable[float], y_true: Iterable[int]):
    xs = np.asarray(list(y_score), dtype=np.float32)
    ys = np.asarray(list(y_true), dtype=np.float32)
    if IsotonicRegression is None:
        class _StubIso:
            def fit(self, *_args, **_kwargs):
                return self
            def predict(self, x):
                arr = np.asarray(x, dtype=np.float32)
                return arr
        iso = _StubIso()
        iso.fit(xs, ys)
        return iso
    iso = IsotonicRegression(out_of_bounds="clip")
    iso.fit(xs, ys)
    return iso

def save_calibrator(cal, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(cal, f)

def load_calibrator(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return pickle.load(f)

def calibrate_with(iso, scores: Iterable[float]) -> List[float]:
    xs = np.asarray(list(scores), dtype=np.float32)
    return list(iso.predict(xs))