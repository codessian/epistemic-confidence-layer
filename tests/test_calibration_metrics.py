import pytest

from src.calibration.metrics import brier_score, ece


def test_brier_score_happy_path():
    score = brier_score([0.0, 0.5, 1.0], [0, 1, 1])
    assert score == pytest.approx((0.0 + 0.25 + 0.0) / 3.0)


def test_brier_score_rejects_length_mismatch():
    with pytest.raises(ValueError):
        brier_score([0.1], [0, 1])


def test_brier_score_rejects_empty_input():
    with pytest.raises(ValueError):
        brier_score([], [])


def test_ece_happy_path():
    val = ece([0.1, 0.4, 0.8, 1.0], [0, 0, 1, 1], bins=5)
    assert 0.0 <= val <= 1.0


def test_ece_rejects_invalid_bins():
    with pytest.raises(ValueError):
        ece([0.5], [1], bins=0)


def test_ece_rejects_invalid_probability():
    with pytest.raises(ValueError):
        ece([1.2], [1], bins=10)


def test_ece_rejects_invalid_label():
    with pytest.raises(ValueError):
        ece([0.2], [2], bins=10)


def test_ece_empty_returns_zero():
    assert ece([], [], bins=10) == 0.0
