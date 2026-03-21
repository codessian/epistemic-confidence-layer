from pathlib import Path

import numpy as np
import pytest

from src.calibration.isotonic import (
    IsotonicCalibrator,
    calibrate_with as iso_calibrate_with,
    fit_isotonic,
    load_calibrator as iso_load,
    save_calibrator as iso_save,
)
from src.calibration.platt import (
    PlattCalibrator,
    calibrate_with as platt_calibrate_with,
    fit_platt,
    load_calibrator as platt_load,
    save_calibrator as platt_save,
)


def test_isotonic_calibrator_predict_requires_fit():
    cal = IsotonicCalibrator()
    with pytest.raises(RuntimeError):
        cal.predict([0.1, 0.2])


def test_isotonic_fit_predict_and_persistence(tmp_path: Path):
    cal = IsotonicCalibrator().fit([0.1, 0.9], [0, 1])
    preds = cal.predict([0.2, 0.8])
    assert len(preds) == 2
    path = tmp_path / "iso.pkl"
    iso_save(cal, str(path))
    loaded = iso_load(str(path))
    assert loaded is not None


def test_isotonic_function_api():
    iso = fit_isotonic([0.1, 0.9], [0, 1])
    out = iso_calibrate_with(iso, [0.2, 0.8])
    assert len(out) == 2


def test_platt_calibrator_predict_requires_fit():
    cal = PlattCalibrator()
    with pytest.raises(RuntimeError):
        cal.predict([0.1, 0.2])


def test_platt_fit_predict_and_persistence(tmp_path: Path):
    cal = PlattCalibrator().fit([0.1, 0.9, 0.2, 0.8], [0, 1, 0, 1])
    preds = cal.predict([0.2, 0.8])
    assert isinstance(preds, np.ndarray)
    assert preds.shape[0] == 2
    path = tmp_path / "platt.pkl"
    platt_save(cal, str(path))
    loaded = platt_load(str(path))
    assert loaded is not None


def test_platt_function_api():
    lr = fit_platt([0.1, 0.9, 0.2, 0.8], [0, 1, 0, 1])
    out = platt_calibrate_with(lr, [0.1, 0.9])
    assert len(out) == 2
