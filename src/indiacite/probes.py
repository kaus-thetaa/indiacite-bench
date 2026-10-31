from indiacite.metrics import auroc


def _lr():
    try:
        from sklearn.linear_model import LogisticRegression
    except ImportError as e:
        raise ImportError("install extras with pip install -e .[ml]") from e
    return LogisticRegression


def fit_probe(x, y, seed: int = 0, c: float = 1.0):
    return _lr()(max_iter=1000, C=c, random_state=seed).fit(x, y)


def probe_auroc(model, x, y) -> float:
    return auroc(list(y), list(model.predict_proba(x)[:, 1]))


def leave_one_group_out(x, y, groups, seed: int = 0) -> dict:
    out = {}
    for g in sorted(set(groups)):
        tr = [i for i, k in enumerate(groups) if k != g]
        te = [i for i, k in enumerate(groups) if k == g]
        model = fit_probe([x[i] for i in tr], [y[i] for i in tr], seed)
        out[g] = probe_auroc(model, [x[i] for i in te], [y[i] for i in te])
    return out


def cross_transfer(xs: dict, ys: dict, seed: int = 0) -> dict:
    out = {}
    for a in xs:
        model = fit_probe(xs[a], ys[a], seed)
        for b in xs:
            if a != b:
                out[(a, b)] = probe_auroc(model, xs[b], ys[b])
    return out
