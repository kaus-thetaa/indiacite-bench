from indiacite.splits import group_split


def test_groups_never_cross_the_split():
    groups = ["a", "a", "b", "b", "c", "d", "d", "e"]
    train, test = group_split(groups, 0.4, seed=1)
    assert set(train).isdisjoint(test)
    assert {groups[i] for i in train}.isdisjoint({groups[i] for i in test})
    assert len(train) + len(test) == len(groups)


def test_deterministic():
    groups = [str(i % 7) for i in range(40)]
    assert group_split(groups, 0.3, seed=5) == group_split(groups, 0.3, seed=5)
