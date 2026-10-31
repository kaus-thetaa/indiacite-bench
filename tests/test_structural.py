import pytest

from indiacite.citations import extract_citations
from indiacite.structural import featurize, fit_structural, make_negative

pytest.importorskip("sklearn")


def real_citations():
    out = []
    for year in range(1995, 2021):
        for vol in range(1, 8):
            raw = f"({year}) {vol} SCC {vol * 100 + 10}"
            out.extend(extract_citations(raw))
    return out


def test_featurize_length_is_stable():
    cites = real_citations()
    assert len({len(featurize(c)) for c in cites}) == 1


def test_negative_differs_and_parses():
    import random

    c = real_citations()[0]
    neg = make_negative(c, random.Random(1))
    assert neg is not None and neg.raw != c.raw


def test_fit_structural_runs_and_is_deterministic():
    model, auc1 = fit_structural(real_citations(), seed=3)
    _, auc2 = fit_structural(real_citations(), seed=3)
    assert auc1 == auc2
    assert 0.5 < auc1 <= 1.0
    assert hasattr(model, "predict_proba")
