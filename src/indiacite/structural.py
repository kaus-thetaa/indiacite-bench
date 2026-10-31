import random
import re

from indiacite.citations import MIN_YEAR, Citation, extract_citations
from indiacite.metrics import auroc

SCHEMES = list(MIN_YEAR)


def featurize(c: Citation) -> list[float]:
    nums = [int(x) for x in re.findall(r"\d+", c.raw)]
    first = nums[1] if len(nums) > 1 else 0
    last = nums[-1]
    onehot = [1.0 if c.scheme == s else 0.0 for s in SCHEMES]
    return onehot + [c.year, c.year - MIN_YEAR[c.scheme], first, last, float(len(nums))]


def make_negative(c: Citation, rng: random.Random) -> Citation | None:
    spans = list(re.finditer(r"\d+", c.raw))
    if not spans:
        return None
    m = rng.choice(spans)
    old = m.group(0)
    for _ in range(10):
        new = str(rng.randint(10 ** (len(old) - 1) if len(old) > 1 else 0, 10 ** len(old) - 1))
        if new != old:
            raw = c.raw[: m.start()] + new + c.raw[m.end() :]
            parsed = extract_citations(raw)
            if parsed:
                return parsed[0]
    return None


def fit_structural(real: list[Citation], seed: int = 0):
    from sklearn.ensemble import RandomForestClassifier

    from indiacite.splits import group_split

    rng = random.Random(seed)
    negs = [n for n in (make_negative(c, rng) for c in real) if n is not None]
    cites = real + negs
    labels = [0] * len(real) + [1] * len(negs)
    groups = [c.raw for c in real] + [c.raw for c in real[: len(negs)]]
    train, test = group_split(groups, 0.3, seed)
    x = [featurize(c) for c in cites]
    model = RandomForestClassifier(n_estimators=200, random_state=seed)
    model.fit([x[i] for i in train], [labels[i] for i in train])
    scores = model.predict_proba([x[i] for i in test])[:, 1]
    return model, auroc([labels[i] for i in test], list(scores))
