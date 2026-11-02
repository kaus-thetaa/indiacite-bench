import json

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")

from indiacite.features_io import (  # noqa: E402
    evaluate_layers,
    join_labels,
    load_features,
    save_features,
)


def toy_rows(n=80, seed=0):
    rng = np.random.default_rng(seed)
    rows, y = [], []
    for i in range(n):
        label = i % 2
        rows.append({"query_id": f"c{i}-citation", "case_id": f"c{i}", "raw": "r", "layer": 1})
        y.append(label)
    x = rng.normal(size=(n, 6))
    x[:, 0] += np.array(y) * 3.0
    labels = {r["query_id"]: ("wrong" if yy else "correct") for r, yy in zip(rows, y, strict=True)}
    return rows, x, labels


def test_roundtrip(tmp_path):
    rows, x, _ = toy_rows(10)
    save_features(tmp_path / "f.npz", tmp_path / "i.jsonl", rows, {1: x, 2: x * 2})
    rows2, layers = load_features(tmp_path / "f.npz", tmp_path / "i.jsonl")
    assert rows2 == rows
    assert set(layers) == {1, 2}
    assert layers[2].shape == (10, 6)
    assert json.loads((tmp_path / "i.jsonl").read_text().splitlines()[0])["case_id"] == "c0"


def test_join_labels_skips_no_answer():
    rows = [{"query_id": "a"}, {"query_id": "b"}, {"query_id": "c"}]
    keep, y = join_labels(rows, {"a": "correct", "b": "no_answer", "c": "wrong"})
    assert keep == [0, 2] and y == [0, 1]


def test_evaluate_layers_finds_signal():
    rows, x, labels = toy_rows(80)
    out = evaluate_layers(rows, {1: x, 2: np.random.default_rng(5).normal(size=x.shape)}, labels)
    assert out[1] > 0.9
    assert out[2] < out[1]
