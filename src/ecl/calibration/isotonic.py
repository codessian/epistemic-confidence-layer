from __future__ import annotations
import numpy as np
from sklearn.isotonic import IsotonicRegression

class IsotonicCalibrator:
    def __init__(self) -> None:
        self._iso = IsotonicRegression(out_of_bounds="clip")
        self._fitted = False

    def fit(self, scores: np.ndarray | list[float], labels: np.ndarray | list[int]) -> "IsotonicCalibrator":
        xs = np.asarray(scores, dtype=np.float32)
        ys = np.asarray(labels, dtype=np.float32)
        self._iso.fit(xs, ys)
        self._fitted = True
        return self

    def predict(self, scores: np.ndarray | list[float]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("IsotonicCalibrator not fitted")
        xs = np.asarray(scores, dtype=np.float32)
        return self._iso.predict(xs)