import pytest

np = pytest.importorskip("numpy")

from indiacite.spans import char_span_to_tokens, citation_rows, confidence_stats, pool_rows  # noqa: E402

OFFSETS = [(0, 2), (2, 6), (6, 7), (7, 14), (14, 20), (0, 0)]


def test_span_to_tokens_overlap_and_special_tokens():
    assert char_span_to_tokens(OFFSETS, 7, 20) == [3, 4]
    assert char_span_to_tokens(OFFSETS, 3, 8) == [1, 2, 3]
    assert char_span_to_tokens(OFFSETS, 30, 40) == []


def test_pool_modes():
    h = np.arange(12, dtype=float).reshape(6, 2)
    assert list(pool_rows(h, [1, 2], "last")) == [4.0, 5.0]
    assert list(pool_rows(h, [1, 2], "first")) == [2.0, 3.0]
    assert list(pool_rows(h, [1, 2], "mean")) == [3.0, 4.0]
    with pytest.raises(ValueError):
        pool_rows(h, [], "last")
    with pytest.raises(ValueError):
        pool_rows(h, [1], "median")


def test_citation_rows_per_layer():
    hidden = {2: np.ones((6, 3)), 4: np.full((6, 3), 2.0)}
    cites = [{"raw": "abc", "start": 7, "end": 20}, {"raw": "none", "start": 90, "end": 99}]
    rows = citation_rows("x" * 20, cites, OFFSETS, hidden, [2, 4], "last")
    assert [(r["layer"], r["n_tokens"]) for r in rows] == [(2, 2), (4, 2)]
    assert rows[1]["vector"] == [2.0, 2.0, 2.0]


def test_confidence_stats_confident_vs_uncertain():
    vocab = 5
    confident = np.full((4, vocab), -10.0)
    confident[:, 2] = 10.0
    ids = [0, 2, 2, 2]
    c = confidence_stats(confident, ids, [1, 2, 3])
    assert c["mean_logprob"] > -0.01 and c["mean_entropy"] < 0.01
    flat = np.zeros((4, vocab))
    u = confidence_stats(flat, ids, [1, 2, 3])
    assert u["mean_logprob"] == pytest.approx(-np.log(vocab))
    assert u["mean_entropy"] == pytest.approx(np.log(vocab))
    assert u["min_logprob"] < c["min_logprob"]


def test_confidence_stats_first_token_has_no_context():
    out = confidence_stats(np.zeros((2, 3)), [0, 1], [0])
    assert out["mean_logprob"] is None
