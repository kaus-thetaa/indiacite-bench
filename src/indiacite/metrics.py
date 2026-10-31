import random


def prf(y_true: list[str], y_pred: list[str], label: str):
    if len(y_true) != len(y_pred):
        raise ValueError("label lists must be equal length")
    tp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p == label)
    fp = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t != label and p == label)
    fn = sum(1 for t, p in zip(y_true, y_pred, strict=True) if t == label and p != label)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return prec, rec, f1


def cohen_kappa(a: list[str], b: list[str]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("label lists must be equal length and non empty")
    n = len(a)
    po = sum(1 for x, y in zip(a, b, strict=True) if x == y) / n
    pe = sum((a.count(k) / n) * (b.count(k) / n) for k in set(a) | set(b))
    if pe == 1:
        return 1.0 if po == 1 else 0.0
    return (po - pe) / (1 - pe)


def bootstrap_ci(y_true, y_pred, label, n=1000, seed=0, alpha=0.05):
    rng = random.Random(seed)
    idx = range(len(y_true))
    scores = []
    for _ in range(n):
        s = [rng.choice(idx) for _ in idx]
        scores.append(prf([y_true[i] for i in s], [y_pred[i] for i in s], label)[2])
    scores.sort()
    lo = scores[int((alpha / 2) * n)]
    hi = scores[int((1 - alpha / 2) * n) - 1]
    return lo, hi


def auroc(y_true: list[int], scores: list[float]) -> float:
    pos = [s for t, s in zip(y_true, scores, strict=True) if t == 1]
    neg = [s for t, s in zip(y_true, scores, strict=True) if t == 0]
    if not pos or not neg:
        raise ValueError("need both classes")
    wins = 0.0
    for p in pos:
        for n in neg:
            wins += 1.0 if p > n else 0.5 if p == n else 0.0
    return wins / (len(pos) * len(neg))


def paired_bootstrap_diff(y_true, pred_a, pred_b, label, n=1000, seed=0, alpha=0.05):
    rng = random.Random(seed)
    idx = range(len(y_true))
    point = prf(y_true, pred_a, label)[2] - prf(y_true, pred_b, label)[2]
    diffs = []
    for _ in range(n):
        s = [rng.choice(idx) for _ in idx]
        t = [y_true[i] for i in s]
        fa = prf(t, [pred_a[i] for i in s], label)[2]
        fb = prf(t, [pred_b[i] for i in s], label)[2]
        diffs.append(fa - fb)
    diffs.sort()
    return point, diffs[int((alpha / 2) * n)], diffs[int((1 - alpha / 2) * n) - 1]
