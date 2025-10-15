from __future__ import annotations
import numpy as np
from sklearn.linear_model import LogisticRegression

class PlattCalibrator:
    def __init__(self) -> None:
        self._lr = LogisticRegression(solver="lbfgs")
        self._fitted = False

    def fit(self, scores: np.ndarray | list[float], labels: np.ndarray | list[int]) -> "PlattCalibrator":
        xs = np.asarray(scores, dtype=np.float32).reshape(-1, 1)
        ys = np.asarray(labels, dtype=np.int32)
        self._lr.fit(xs, ys)
        self._fitted = True
        return self

    def predict(self, scores: np.ndarray | list[float]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("PlattCalibrator not fitted")
        xs = np.asarray(scores, dtype=np.float32).reshape(-1, 1)
        proba = self._lr.predict_proba(xs)[:, 1]
        return proba.astype(np.float32)