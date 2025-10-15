from __future__ import annotations
# Skeleton isotonic calibration API; plug real sklearn later.

class IsotonicCalibrator:
    def __init__(self):
        self._fitted = False

    def fit(self, y_pred: list[float], y_true: list[int]) -> "IsotonicCalibrator":
        # TODO: replace with sklearn.IsotonicRegression
        self._fitted = True
        return self

    def predict(self, y_pred: list[float]) -> list[float]:
        if not self._fitted:
            return y_pred
        # trivial shrink-toward-0.5 stub
        return [0.5 + 0.5 * (p - 0.5) * 0.8 for p in y_pred]