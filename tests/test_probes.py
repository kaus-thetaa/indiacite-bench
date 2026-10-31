import pytest

from indiacite.probes import cross_transfer, fit_probe, leave_one_group_out, probe_auroc

np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")


def toy(seed, n=60, shift=2.0):
    rng = np.random.default_rng(seed)
    y = np.array([0, 1] * (n // 2))
    x = rng.normal(size=(n, 4))
    x[:, 0] += y * shift
    return x, y


def test_probe_learns_separable_signal():
    x, y = toy(0)
    model = fit_probe(x, y)
    assert probe_auroc(model, x, y) > 0.9


def test_leave_one_group_out_returns_each_group():
    x, y = toy(1, n=90)
    groups = ["a", "b", "c"] * 30
    out = leave_one_group_out(x, y, groups)
    assert set(out) == {"a", "b", "c"}
    assert all(v > 0.8 for v in out.values())


def test_cross_transfer_pairs():
    xa, ya = toy(2)
    xb, yb = toy(3)
    out = cross_transfer({"name": xa, "year": xb}, {"name": ya, "year": yb})
    assert set(out) == {("name", "year"), ("year", "name")}
