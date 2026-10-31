from indiacite.baselines import DictResolver, ExistenceChecker, FormatChecker


def test_format_flags_impossible_year():
    fc = FormatChecker()
    assert fc.flag("(1900) 99 SCC 999")
    assert not fc.flag("(2004) 7 SCC 528")
    assert not fc.flag("Section 302 of the Indian Penal Code")


def test_existence_checker_unknown_policy():
    resolver = DictResolver({"(2004) 7 SCC 528": "fictional canonical"})
    strict = ExistenceChecker(resolver)
    assert not strict.flag("(2004) 7 SCC 528")
    assert strict.flag("(2005) 1 SCC 1")
