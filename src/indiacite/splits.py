import random


def group_split(groups: list[str], test_frac: float = 0.2, seed: int = 0):
    uniq = sorted(set(groups))
    rng = random.Random(seed)
    rng.shuffle(uniq)
    n_test = max(1, round(len(uniq) * test_frac))
    test_groups = set(uniq[:n_test])
    train = [i for i, g in enumerate(groups) if g not in test_groups]
    test = [i for i, g in enumerate(groups) if g in test_groups]
    return train, test
