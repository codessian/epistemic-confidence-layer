import pytest

from src.metrics.calibration import ece, reliability_diagram


def test_metrics_ece_basic():
    out = ece([0.2, 0.7, 0.9], [0, 1, 1], n_bins=3)
    assert 0.0 <= out <= 1.0


def test_metrics_ece_rejects_mismatch():
    with pytest.raises(ValueError):
        ece([0.1], [1, 0], n_bins=10)


def test_metrics_ece_rejects_out_of_range_probability():
    with pytest.raises(ValueError):
        ece([1.1], [1], n_bins=10)


def test_metrics_ece_rejects_non_binary_label():
    with pytest.raises(ValueError):
        ece([0.1], [3], n_bins=10)


def test_reliability_diagram_empty():
    assert reliability_diagram([], [], n_bins=10) == ([], [], [], [])


def test_reliability_diagram_outputs_expected_shapes():
    centers, accs, confs, counts = reliability_diagram([0.0, 0.5, 1.0], [0, 1, 1], n_bins=5)
    assert len(centers) == len(accs) == len(confs) == len(counts) == 5
    assert counts[-1] >= 1
