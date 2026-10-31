import pytest

from indiacite.metrics import bootstrap_ci, cohen_kappa, prf


def test_prf_perfect():
    y = ["a", "b", "a"]
    assert prf(y, y, "a") == (1.0, 1.0, 1.0)


def test_prf_known():
    t = ["a", "a", "b", "b"]
    p = ["a", "b", "a", "b"]
    prec, rec, f1 = prf(t, p, "a")
    assert (prec, rec, f1) == (0.5, 0.5, 0.5)


def test_kappa_identical_is_one():
    assert cohen_kappa(["a", "b", "a"], ["a", "b", "a"]) == 1.0


def test_kappa_known_value():
    assert cohen_kappa(["a", "a", "b", "b"], ["a", "b", "b", "b"]) == pytest.approx(0.5)


def test_kappa_length_mismatch():
    with pytest.raises(ValueError):
        cohen_kappa(["a"], ["a", "b"])


def test_bootstrap_deterministic_and_bounded():
    t = ["a", "b"] * 10
    p = ["a", "b"] * 10
    lo, hi = bootstrap_ci(t, p, "a", n=200, seed=1)
    assert (lo, hi) == bootstrap_ci(t, p, "a", n=200, seed=1)
    assert lo == 1.0 and hi == 1.0


def test_auroc_perfect_and_tied():
    from indiacite.metrics import auroc

    assert auroc([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]) == 1.0
    assert auroc([0, 1], [0.5, 0.5]) == 0.5


def test_auroc_needs_both_classes():
    from indiacite.metrics import auroc

    with pytest.raises(ValueError):
        auroc([1, 1], [0.1, 0.9])


def test_paired_bootstrap_identical_predictions_give_zero():
    from indiacite.metrics import paired_bootstrap_diff

    t = ["a", "b"] * 10
    d, lo, hi = paired_bootstrap_diff(t, t, t, "a", n=100, seed=2)
    assert (d, lo, hi) == (0.0, 0.0, 0.0)
