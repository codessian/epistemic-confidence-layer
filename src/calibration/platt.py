from __future__ import annotations
import os
import pickle
import numpy as np
from typing import Iterable, List
try:
    from sklearn.linear_model import LogisticRegression
except Exception:
    LogisticRegression = None

class PlattCalibrator:
    def __init__(self) -> None:
        self._lr = LogisticRegression(solver="lbfgs") if LogisticRegression else None
        self._fitted = False

    def fit(self, scores: np.ndarray | list[float], labels: np.ndarray | list[int]) -> "PlattCalibrator":
        xs = np.asarray(scores, dtype=np.float32).reshape(-1, 1)
        ys = np.asarray(labels, dtype=np.int32)
        if self._lr is not None:
            self._lr.fit(xs, ys)
        self._fitted = True
        return self

    def predict(self, scores: np.ndarray | list[float]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("PlattCalibrator not fitted")
        xs = np.asarray(scores, dtype=np.float32).reshape(-1, 1)
        if self._lr is not None:
            proba = self._lr.predict_proba(xs)[:, 1]
            return proba.astype(np.float32)
        # Fallback: simple sigmoid transformation as a stand-in
        # to keep outputs in [0,1] without sklearn
        import math
        return np.array([1.0/(1.0+math.exp(-4*(float(s)-0.5))) for s in xs], dtype=np.float32)

# --- Function-style API for v0.2 bundle compatibility ---
def fit_platt(y_score: Iterable[float], y_true: Iterable[int]):
    X = np.asarray(list(y_score), dtype=np.float32).reshape(-1, 1)
    y = np.asarray(list(y_true), dtype=np.int32)
    if LogisticRegression is None:
        class _StubLR:
            def fit(self, *_args, **_kwargs):
                return self
            def predict_proba(self, X):
                import math
                # return 2-column probas where [:,1] is sigmoid stand-in
                xs = [float(v[0]) for v in X.tolist()]
                ps = [1.0/(1.0+math.exp(-4*(x-0.5))) for x in xs]
                return np.column_stack([1.0-np.array(ps), np.array(ps)])
        lr = _StubLR()
        lr.fit(X, y)
        return lr
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X, y)
    return lr

def save_calibrator(cal, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(cal, f)

def load_calibrator(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return pickle.load(f)

def calibrate_with(lr, scores: Iterable[float]) -> List[float]:
    X = np.asarray(list(scores), dtype=np.float32).reshape(-1, 1)
    proba = lr.predict_proba(X)[:, 1]
    return list(proba.astype(np.float32))